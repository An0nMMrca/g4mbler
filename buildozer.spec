[app]

# Osnovne informacije o aplikaciji
title = SL0TPREDIKSNAPP
package.name = slotprediksnapp
package.domain = org.example
source.dir = .
version = 1.0.0

# Koje fajlove uključiti (python, slike itd.)
source.include_exts = py,png,jpg,kv,atlas

# Zahtevi za Python pakete
requirements = python3,kivy,cython,numpy,scikit-learn

# Ikonica i splash screen
icon.filename = icons/app_icon.png
presplash.filename = icons/splash.png
include_patterns = icons/*.png

# Orijentacija i fullscreen
orientation = portrait
fullscreen = 1

# Android podešavanja
android.api = 33
android.minapi = 21
android.build_tools_version = 33.0.0

# Koristi SDL2 bootstrap
p4a.bootstrap = sdl2

# Arhitekture koje podržavamo
android.archs = armeabi-v7a, arm64-v8a

# Dozvole koje aplikacija traži
android.permissions = INTERNET

# Ostalo
log_level = 2
copy_mainsource = 1
build_dir = ./.buildozer
