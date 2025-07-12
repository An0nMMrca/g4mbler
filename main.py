import sqlite3
import random
import numpy as np
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from sklearn.linear_model import LogisticRegression


# --- Baza podataka ---
DB_NAME = "predictions.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            last_cards TEXT,
            predicted_color TEXT,
            actual_color TEXT,
            correct INTEGER
        )
    ''')
    conn.commit()
    conn.close()


def insert_prediction(last_cards, predicted_color, actual_color, correct):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO predictions (last_cards, predicted_color, actual_color, correct)
        VALUES (?, ?, ?, ?)
    ''', (last_cards, predicted_color, actual_color, correct))
    conn.commit()
    conn.close()


def get_training_data():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT last_cards, actual_color FROM predictions')
    data = c.fetchall()
    conn.close()
    return data


# --- AI Model ---

class CardPredictor:
    def __init__(self):
        self.model = LogisticRegression()
        self.trained = False

    def preprocess(self, data):
        # Pretvaranje stringova karata u numerički input za model
        X = []
        y = []
        color_map = {'red': 1, 'black': 0}
        suit_map = {'Pik':0, 'Karo':1, 'Herc':2, 'Tref':3}
        for last_cards_str, actual_color in data:
            cards = last_cards_str.split(',')
            features = []
            for card in cards:
                # Format: "Pik-red" ili "Herc-black"
                if '-' in card:
                    suit, color = card.split('-')
                    features.append(suit_map.get(suit, -1))
                    features.append(color_map.get(color, -1))
                else:
                    # fallback ako format nije dobar
                    features.extend([-1, -1])
            X.append(features)
            y.append(color_map.get(actual_color, 0))
        return np.array(X), np.array(y)

    def train(self):
        data = get_training_data()
        if not data:
            return
        X, y = self.preprocess(data)
        if len(X) > 0:
            self.model.fit(X, y)
            self.trained = True

    def predict(self, last_cards):
        if not self.trained:
            return random.choice(['red', 'black'])
        # Pretvori ulaz u features
        suit_map = {'Pik':0, 'Karo':1, 'Herc':2, 'Tref':3}
        color_map = {'red': 1, 'black': 0}
        cards = last_cards.split(',')
        features = []
        for card in cards:
            if '-' in card:
                suit, color = card.split('-')
                features.append(suit_map.get(suit, -1))
                features.append(color_map.get(color, -1))
            else:
                features.extend([-1, -1])
        X = np.array([features])
        pred = self.model.predict(X)
        return 'red' if pred[0] == 1 else 'black'


# --- UI ---

class CardPredictApp(App):

    def build(self):
        init_db()
        self.predictor = CardPredictor()
        self.predictor.train()

        self.last_cards = []  # Lista stringova npr. "Pik-red"

        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.label_prediction = Label(text="Predikcija boje sledeće karte: ---", font_size=20, size_hint=(1, 0.2))
        main_layout.add_widget(self.label_prediction)

        # Polja za unos poslednje 4 karte (npr. Pik-red, Karo-black...)
        input_layout = BoxLayout(size_hint=(1, 0.3), spacing=10)
        self.card_inputs = []
        for i in range(4):
            ti = TextInput(hint_text=f"Poslednja karta {i+1} (npr. Pik-red)", multiline=False)
            self.card_inputs.append(ti)
            input_layout.add_widget(ti)
        main_layout.add_widget(input_layout)

        # Dugme za predikciju
        btn_pred = Button(text="Predvidi sledeću boju", size_hint=(1, 0.2), background_color=[1, 0, 0, 1])
        btn_pred.bind(on_press=self.on_predict)
        main_layout.add_widget(btn_pred)

        # Dugmad za unos stvarne boje sledeće karte (Crveno/Crno)
        colors_layout = BoxLayout(size_hint=(1, 0.2), spacing=20)
        btn_red = Button(text="Crveno", background_color=[1, 0, 0, 1])
        btn_black = Button(text="Crno", background_color=[0, 0, 0, 1])
        btn_red.bind(on_press=lambda x: self.on_actual_color('red'))
        btn_black.bind(on_press=lambda x: self.on_actual_color('black'))
        colors_layout.add_widget(btn_red)
        colors_layout.add_widget(btn_black)
        main_layout.add_widget(colors_layout)

        # Labela za poruku o tačnosti
        self.label_result = Label(text="", font_size=18, size_hint=(1, 0.2))
        main_layout.add_widget(self.label_result)

        return main_layout

    def on_predict(self, instance):
        # Uzmi unose iz polja za poslednje karte
        cards = []
        for ti in self.card_inputs:
            val = ti.text.strip()
            if val == "":
                self.show_popup("Greška", "Popunite sva polja sa poslednjim kartama!")
                return
            cards.append(val)
        last_cards_str = ",".join(cards)
        self.last_cards = last_cards_str
        pred = self.predictor.predict(last_cards_str)
        self.label_prediction.text = f"Predviđena boja sledeće karte: [b]{pred.upper()}[/b]"
        self.label_result.text = ""
        self.predicted_color = pred

    def on_actual_color(self, color):
        if not hasattr(self, 'predicted_color'):
            self.show_popup("Greška", "Prvo napravite predikciju!")
            return

        # Upis u bazu - da li je pogodak?
        correct = 1 if color == self.predicted_color else 0
        insert_prediction(self.last_cards, self.predicted_color, color, correct)

        # Re-treniraj model sa novim podatkom
        self.predictor.train()

        # Prikaži rezultat korisniku
        if correct:
            self.label_result.text = "[color=00ff00]Pogodili ste![/color]"
        else:
            self.label_result.text = "[color=ff0000]Niste pogodili.[/color]"

        # Resetuj predikciju
        self.label_prediction.text = "Predikcija boje sledeće karte: ---"
        self.predicted_color = None
        self.last_cards = None
        for ti in self.card_inputs:
            ti.text = ""

    def show_popup(self, title, message):
        popup = Popup(title=title,
                      content=Label(text=message),
                      size_hint=(0.6, 0.4))
        popup.open()


if __name__ == '__main__':
    CardPredictApp().run()

