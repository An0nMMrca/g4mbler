[app]

title = SL0TPREDIKSNAPP
package.name = slotprediksnapp
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv
version = 1.0.0

requirements = python3,kivy,numpy,cython,scikit-learn

icon.filename = icons/app_icon.png
presplash.filename = icons/splash.png
include_patterns = icons/*.png

orientation = portrait
fullscreen = 1

android.permissions = INTERNET

android.api = 33
android.minapi = 21
android.build_tools_version = 33.0.0
android.ndk = 25b
android.archs = arm64-v8a,armeabi-v7a
android.entrypoint = org.kivy.android.PythonActivity

# Bootstrap
p4a.bootstrap = sdl2

# Logging
log_level = 2

# Optional
copy_mainsource = 1

[buildozer]

log_level = 2
warn_on_root = 1
build_dir = ./.buildozer
