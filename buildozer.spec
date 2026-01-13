[app]
title = CanterPro
package.name = canterpro
package.domain = org.canter
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,xlsx
version = 1.7.1

requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow,openpyxl,android,certifi,cython>=3.0.0

orientation = portrait
fullscreen = 0

android.archs = arm64-v8a
android.api = 34
android.minapi = 24
android.ndk = 25b
android.accept_sdk_license = True
android.enable_androidx = True
p4a.branch = master

android.permissions = INTERNET

[buildozer]
log_level = 2
warn_on_root = 1
