name: Build APK
on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-22.04
    steps:
      - uses: actions/checkout@v4

      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'

      - name: Set up Python 3.10
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      # ИСПРАВЛЕНО: Убраны конфликтные библиотеки (ffmpeg, gstreamer, sdl2).
      # Оставлены только инструменты для компиляции.
      - name: Install Build Tools
        run: |
          sudo apt-get update
          sudo apt-get install -y \
            build-essential git python3-dev \
            libssl-dev libffi-dev \
            zip unzip autoconf libtool pkg-config cmake \
            zlib1g-dev gettext

      - name: Install Buildozer & Cython
        run: |
          pip install --upgrade pip
          pip install "Cython<3.0"
          pip install buildozer

      # yes | ... отвечает "y" на все вопросы установщика Android SDK
      - name: Build with Buildozer
        run: |
          yes | buildozer android debug

      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: CanterPro-APK
          path: bin/*.apk
