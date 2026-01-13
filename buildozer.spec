[app]
title = CanterPro
package.name = canterpro
package.domain = org.canter
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,xlsx
version = 1.0

# Список зависимостей без лишних пробелов
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow,openpyxl,android,et_xmlfile

orientation = portrait
fullscreen = 0

# Настройки для Google Play (API 34)
android.archs = arm64-v8a
android.api = 34
android.minapi = 24
# NDK 25c наиболее стабилен для текущих версий Kivy
android.ndk = 25c
android.accept_sdk_license = True

# ВАЖНО: Оставляем пустым, чтобы Buildozer использовал стабильную ветку,
# которая корректно работает с Cython 3 и Kivy 2.3.0
p4a.branch = 

android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

android.manifest.intent_filters = [ {"action": "android.intent.action.SEND", "category": "android.intent.category.DEFAULT", "data": {"mimeType": "text/plain"}} ]

[buildozer]
log_level = 2
warn_on_root = 1
