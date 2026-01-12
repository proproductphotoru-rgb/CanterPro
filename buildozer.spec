[app]

# (str) Заголовок вашего приложения
title = Canter Logistics

# (str) Имя пакета (без пробелов)
package.name = canter_calc

# (str) Домен пакета (используется для уникальности)
package.domain = org.canter.logs

# (str) Исходный код в текущей папке
source.dir = .

# (list) Расширения файлов, которые будут включены в APK
source.include_exts = py,png,jpg,kv,atlas,xlsx

# (str) Версия приложения
version = 1.0

# (list) ЗАВИСИМОСТИ. Добавлены geopy для карт и openpyxl для Excel
requirements = python3,flet==0.21.0,hostpython3,geopy,openpyxl,certifi

# (str) Ориентация экрана (только вертикальная для удобства ввода)
orientation = portrait

# (bool) Полноэкранный режим
fullscreen = 0

# (list) Архитектуры. Оставляем только одну современную для скорости и стабильности
android.archs = arm64-v8a

# (str) Иконка (если есть файл icon.png, раскомментируйте)
#icon.filename = %(source.dir)s/icon.png

# (list) ПРАВА ДОСТУПА. Интернет обязателен для карт и работы Flet
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# (int) Target Android API. 34 — требование Google Play в 2024 году
android.api = 34

# (int) Минимальный поддерживаемый Android
android.minapi = 21

# (str) Версия NDK (25b стабильна для Flet)
android.ndk = 25b

# (bool) Автоматически принимать лицензии SDK
android.accept_sdk_license = True

# (bool) Разрешить сборку под root (нужно для GitHub/Colab)
android.allow_root = 1

[buildozer]
# (int) Уровень детализации логов (2 — максимально подробно)
log_level = 2

# (str) Папка для сборки
build_dir = ./.buildozer
