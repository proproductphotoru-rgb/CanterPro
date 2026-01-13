[app]
title = CanterPro
package.name = canterpro
package.domain = org.canter
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,xlsx
version = 1.1

# Включаем certifi для безопасности сетевых соединений в Android 15
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow,openpyxl,android,et_xmlfile,certifi

orientation = portrait
fullscreen = 0

# Настройки архитектуры и системы для Android 15
android.archs = arm64-v8a
android.api = 35
android.minapi = 24
android.ndk = 26b
android.accept_sdk_license = True

# Поддержка современных библиотек Android
android.enable_androidx = True
android.python_optimise = True

# Используем ветку develop для лучшей совместимости с API 35
p4a.branch = develop

# Разрешения (Android 15 требует более точных разрешений для файлов)
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, READ_MEDIA_IMAGES

[buildozer]
log_level = 2
warn_on_root = 1
