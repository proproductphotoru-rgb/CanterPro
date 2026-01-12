[app]
title = CanterPro
package.name = canterpro
package.domain = org.canter
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# Оставляем только базовый Flet и certifi для работы интернета
requirements = python3,flet==0.21.0,hostpython3,certifi

orientation = portrait
fullscreen = 0
android.archs = arm64-v8a
android.api = 34
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.permissions = INTERNET
android.allow_root = 1

[buildozer]
log_level = 2
