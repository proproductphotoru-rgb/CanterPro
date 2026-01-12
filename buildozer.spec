[app]

# (str) Название вашего приложения в телефоне
title = CanterPro

# (str) Техническое имя (без пробелов)
package.name = canterpro

# (str) Уникальный домен приложения
package.domain = org.canter.logs

# (str) Где лежит ваш main.py (. означает текущую папку)
source.dir = .

# (list) Какие расширения файлов включать в сборку
source.include_exts = py,png,jpg,kv,atlas,xlsx

# (str) Версия приложения
version = 0.1

# (list) ЗАВИСИМОСТИ. 
# ВАЖНО: Мы зафиксировали версию flet и добавили базовые библиотеки.
requirements = python3,flet==0.21.0,hostpython3,certifi,pyTelegramBotAPI,geopy,openpyxl

# (str) Ориентация экрана
orientation = portrait

# (bool) Полноэкранный режим
fullscreen = 0

# (list) Архитектуры (arm64-v8a — стандарт для современных смартфонов)
android.archs = arm64-v8a

# (int) Android API (34 — актуальный стандарт Google Play на 2025-2026 гг)
android.api = 34

# (int) Минимальная версия Android (21 — поддержка старых устройств)
android.minapi = 21

# (str) Версия Android NDK, которую мы видели в ваших логах
android.ndk = 25b

# (bool) Автоматическое принятие лицензий SDK (Критически важно!)
android.accept_sdk_license = True

# (list) Разрешения (Интернет для карт/бота и доступ к файлам для Excel)
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (bool) Разрешить сборку под пользователем root (нужно для GitHub)
android.allow_root = 1

# (int) Уровень детализации логов (2 — чтобы видеть ошибки, если они будут)
log_level = 2

[buildozer]
# (int) Делать ли паузу при ошибках
warn_on_root = 0
