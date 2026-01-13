[app]
title = CanterPro
package.name = canterpro
package.domain = org.canter
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,xlsx
version = 1.6

# Фиксируем Cython в требованиях
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow,openpyxl,android,et_xmlfile,certifi,libxml2,libxslt,cython==0.29.33

orientation = portrait
fullscreen = 0

android.archs = arm64-v8a
android.api = 33
android.minapi = 24
android.ndk = 25b
android.accept_sdk_license = True
android.enable_androidx = True
p4a.branch = master

android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, READ_MEDIA_IMAGES

[buildozer]
log_level = 2
warn_on_root = 1
