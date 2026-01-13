[app]
title = CanterPro
package.name = canterpro
package.domain = org.canter
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,xlsx
version = 1.0

# Оптимизированный список требований
requirements = python3,kivy==2.2.1,kivymd==1.2.0,pillow,openpyxl,android,et_xmlfile,sqlite3

orientation = portrait
fullscreen = 0

# Настройки для Android 14
android.archs = arm64-v8a
android.api = 34
android.minapi = 24
android.ndk = 25b
android.accept_sdk_license = True

# Ускорение сборки за счет исключения ненужного
android.no_byte_compile_python = False
android.python_optimise = True

p4a.branch = master

android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.manifest.intent_filters = [ {"action": "android.intent.action.SEND", "category": "android.intent.category.DEFAULT", "data": {"mimeType": "text/plain"}} ]

[buildozer]
log_level = 2
warn_on_root = 1
