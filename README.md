# 🎥 Mira YouTube Downloader

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D4?style=for-the-badge&logo=windows)

[English](#english) | [Русский](#русский)

---

<a name="english"></a>
## 🇬🇧 English Description

**Mira YouTube Downloader** is a professional-grade GUI utility designed for high-quality video extraction. It focuses on user experience and seamless playback on Windows systems.

### ✨ Key Features
* **Smart Resolution Filtering:** Grouped formats to prevent clutter. Only the best quality for each resolution is shown.
* **Audio Compatibility Fix (AAC):** Automatically transcodes audio from Opus/Vorbis to **AAC**. Guaranteed to play with sound in standard Windows Media Player.
* **Layout-Independent Input:** Custom fix for `Ctrl+V` pasting. Works perfectly even if your keyboard is set to Russian or Spanish layout.
* **Multilingual:** Full support for **English**, **Russian**, and **Spanish**.
* **Modern Interface:** Sleek dark-themed UI powered by `CustomTkinter`.

### 🚀 How to Run
1. Clone: `git clone https://github.com/your-username/MiraYouTubeDownloader.git`
2. Install: `pip install customtkinter yt-dlp`
3. Place `ffmpeg.exe` in the root folder.
4. Launch: `python MiraYouTubeDownloader.py`

---

<a name="русский"></a>
## 🇷🇺 Описание на русском

**Mira YouTube Downloader** — это современная утилита с графическим интерфейсом для скачивания видео. Проект решает основные проблемы стандартных загрузчиков, обеспечивая чистоту файлов и удобство работы.

### ✨ Особенности
* **Умная фильтрация:** Программа анализирует доступные форматы и предлагает только лучшие варианты для каждого разрешения, избавляя от дубликатов.
* **Исправление звука (AAC):** Автоматическая перепаковка звука в формат **AAC**. Ваши видео больше не будут "немыми" в стандартном плеере Windows.
* **Исправленный Ctrl+V:** Вставка ссылок работает корректно при любой раскладке клавиатуры (RU/EN).
* **Многоязычность:** Интерфейс на **русском**, **английском** и **испанском**.
* **Портативность:** Весь функционал и зависимости (включая FFmpeg) упаковываются в один автономный `.exe`.

### 📦 Сборка в EXE (Build)
```bash
pyinstaller --noconsole --onefile --add-data "ffmpeg.exe;." --add-data "icon.ico;." --collect-all customtkinter --icon="icon.ico" MiraYouTubeDownloader.py
