[app]
title = CanterPro
package.name = canterpro
package.domain = org.canter
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,xlsx
version = 1.6

# Фиксация Cython предотвращает ошибки компиляции на сервере
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow,openpyxl,android,et_xmlfile,certifi,cython==0.29.33

orientation = portrait
fullscreen = 0

# Настройки стабильности для Android 14/15
android.archs = arm64-v8a
android.api = 34
android.minapi = 24
android.ndk = 25b
android.accept_sdk_license = True
android.enable_androidx = True
p4a.branch = master

# Права доступа (в Android 15 это минимум)
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

[buildozer]
log_level = 2
warn_on_root = 1
