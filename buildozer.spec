[app]
title = CanterPro
package.name = canterpro
package.domain = org.canter
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,xlsx
version = 1.0

# Убрали sqlite3 из requirements, так как он встроен в python3
requirements = python3,kivy==2.2.1,kivymd==1.2.0,pillow,openpyxl,android,et_xmlfile

orientation = portrait
fullscreen = 0

# Настройки для Android 14 (API 34)
android.archs = arm64-v8a
android.api = 34
android.minapi = 24
android.ndk = 25b
android.accept_sdk_license = True

# Включаем оптимизацию для уменьшения веса и ускорения сборки
android.python_optimise = True
android.no_byte_compile_python = False

p4a.branch = master

android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

[buildozer]
log_level = 2
warn_on_root = 1
