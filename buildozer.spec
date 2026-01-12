[app]
title = CanterPro
package.name = canterpro
package.domain = org.canter
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,xlsx
version = 1.0

requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow,openpyxl,android

android.manifest.intent_filters = [ {"action": "android.intent.action.SEND", "category": "android.intent.category.DEFAULT", "data": {"mimeType": "text/plain"}} ]

orientation = portrait
android.archs = arm64-v8a
android.api = 34
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.allow_root = 1

[buildozer]
log_level = 2
