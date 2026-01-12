[app]

# (str) Название приложения в меню телефона
title = CanterPro

# (str) Техническое имя (без пробелов и спецсимволов)
package.name = canterpro

# (str) Домен (нужен для уникальности ID приложения)
package.domain = org.logistic.canter

# (str) Где лежит main.py (. означает в текущей папке)
source.dir = .

# (list) Какие файлы включать в APK
source.include_exts = py,png,jpg,kv,atlas,xlsx

# (str) Версия
version = 0.1

# (list) ЗАВИСИМОСТИ. Указаны конкретные версии для стабильности на GitHub
requirements = python3,flet==0.21.0,hostpython3,pyTelegramBotAPI,geopy,openpyxl,certifi,chardet,idna,urllib3

# (str) Ориентация
orientation = portrait

# (list) Архитектуры. Оставляем ТОЛЬКО arm64-v8a (самая быстрая сборка)
android.archs = arm64-v8a

# (int) Android API (34 — стандарт 2024/2025 года)
android.api = 34
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

# (list) Разрешения. Интернет нужен для карт, Storage — для Excel
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (bool) Использовать инсталлер (True помогает избежать некоторых ошибок)
android.skip_update = False

# (bool) Разрешить сборку под root (обязательно для GitHub Actions)
android.allow_root = 1

[buildozer]
# Уровень логов 2 позволит нам увидеть точную причину, если упадет снова
log_level = 2
warn_on_root = 0
