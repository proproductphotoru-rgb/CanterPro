[app]
title = CanterPro
package.name = canterpro
package.domain = org.canter
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,xlsx
version = 1.0

# Используем сверхстабильную версию Kivy 2.2.1
requirements = python3,kivy==2.2.1,kivymd==1.2.0,pillow,openpyxl,android,et_xmlfile

orientation = portrait
fullscreen = 0

# Оптимальные настройки для API 33 (Android 13/14)
android.archs = arm64-v8a
android.api = 33
android.minapi = 24
android.ndk = 25b
android.accept_sdk_license = True

# Используем проверенную временем ветку инструментов
p4a.branch = release-2023.09.13

android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.manifest.intent_filters = [ {"action": "android.intent.action.SEND", "category": "android.intent.category.DEFAULT", "data": {"mimeType": "text/plain"}} ]

[buildozer]
log_level = 2
warn_on_root = 1
