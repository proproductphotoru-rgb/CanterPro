[app]
title = CanterPro
package.name = canterpro
package.domain = org.canter
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,xlsx
version = 1.7

# Использование Cython 3.0.0 обязательно для Android 15 и NDK 26
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow,openpyxl,android,certifi,cython>=3.0.0

orientation = portrait
fullscreen = 0

android.archs = arm64-v8a
android.api = 35
android.minapi = 24
android.ndk = 26b
android.accept_sdk_license = True
android.enable_androidx = True
# Используем ветку develop, так как в ней исправлены баги API 35
p4a.branch = develop

android.permissions = INTERNET
