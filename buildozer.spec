[app]

title = SL0TPREDIKSNAPP
package.name = slotprediksnapp
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0.0

requirements = python3,kivy,cython,numpy,scikit-learn

orientation = portrait
fullscreen = 1

icon.filename = icons/app_icon.png
presplash.filename = icons/splash.png
include_patterns = icons/*.png

# Android specifics
android.api = 33
android.minapi = 21
android.build_tools_version = 33.0.0
android.sdk = 24
android.ndk = 25b
p4a.bootstrap = sdl2
android.archs = armeabi-v7a, arm64-v8a

log_level = 2
build_dir = ./.buildozer
copy_mainsource = 1

# Permissions
android.permissions = INTERNET
