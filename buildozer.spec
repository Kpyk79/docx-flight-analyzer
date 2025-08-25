[app]
title = Аналіз DOCX польотів
package.name = docx_flight_analyzer
package.domain = org.example
source.dir = .
source.include_exts = py,kv,txt,md,docx
version = 0.1.0
requirements = python3,kivy,python-docx,plyer,lxml,pillow
orientation = portrait
fullscreen = 0
android.api = 35
android.minapi = 24
android.archs = arm64-v8a,armeabi-v7a,x86_64
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 0
