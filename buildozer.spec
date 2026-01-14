[app]

title = CanterPro
package.name = canterpro
package.domain = org.canter

source.dir = .
source.include_exts = py,kv,png,jpg,ttf

requirements = python3,kivy,kivymd,openpyxl

version = 1.7

android.api = 34
android.minapi = 26
android.ndk = 26b
android.sdk = 34
android.archs = arm64-v8a

android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.allow_backup = False

fullscreen = 0
orientation = portrait

log_level = 2

# 🔴 КРИТИЧНО для Android 15
p4a.branch = develop
