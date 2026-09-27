"""
img2palette - Localization strings
Author: dimasbotyara

Все строки интерфейса на русском и английском.
"""

STRINGS = {
    # ===== ОБЩИЕ =====
    "app_title": {
        "ru": "🎨 img2palette — Превращатель изображений в палитры",
        "en": "🎨 img2palette — Image to Palette Converter"
    },
    "app_subtitle": {
        "ru": "by dimasbotyara",
        "en": "by dimasbotyara"
    },

    # ===== ПЕРВЫЙ ЗАПУСК =====
    "first_run_welcome": {
        "ru": "Добро пожаловать в img2palette! 🎉",
        "en": "Welcome to img2palette! 🎉"
    },
    "choose_language": {
        "ru": "Выбери язык / Choose language:",
        "en": "Выбери язык / Choose language:"
    },
    "lang_option_ru": {
        "ru": "1. 🇷🇺 Русский",
        "en": "1. 🇷🇺 Русский"
    },
    "lang_option_en": {
        "ru": "2. 🇬🇧 English",
        "en": "2. 🇬🇧 English"
    },
    "lang_prompt": {
        "ru": "Введите 1 или 2: ",
        "en": "Enter 1 or 2: "
    },
    "lang_set_ru": {
        "ru": "Язык установлен: Русский 🇷🇺",
        "en": "Language set: Russian 🇷🇺"
    },
    "lang_set_en": {
        "ru": "Язык установлен: English 🇬🇧",
        "en": "Language set: English 🇬🇧"
    },
    "lang_invalid": {
        "ru": "Неверный ввод, попробуйте ещё раз.",
        "en": "Invalid input, try again."
    },

    # ===== ГЛАВНОЕ МЕНЮ =====
    "menu_title": {
        "ru": "📋 Главное меню",
        "en": "📋 Main Menu"
    },
    "menu_single": {
        "ru": "1. 🖼  Обработать одно изображение",
        "en": "1. 🖼  Process single image"
    },
    "menu_batch": {
        "ru": "2. 📁 Обработать папку (batch)",
        "en": "2. 📁 Process folder (batch)"
    },
    "menu_video": {
        "ru": "3. 🎬 Обработать видео",
        "en": "3. 🎬 Process video"
    },
    "menu_gif": {
        "ru": "4. 🎞  Обработать GIF",
        "en": "4. 🎞  Process GIF"
    },
    "menu_collage": {
        "ru": "5. 🧩 Создать коллаж палитр",
        "en": "5. 🧩 Create palette collage"
    },
    "menu_preview": {
        "ru": "6. 👁  Превью палитр в терминале",
        "en": "6. 👁  Preview palettes in terminal"
    },
    "menu_roulette": {
        "ru": "7. 🎰 Рулетка (рандомная палитра)",
        "en": "7. 🎰 Roulette (random palette)"
    },
    "menu_pixel_sort": {
        "ru": "8. 📊 Pixel Sort эффект",
        "en": "8. 📊 Pixel Sort effect"
    },
    "menu_settings": {
        "ru": "9. ⚙️  Настройки",
        "en": "9. ⚙️  Settings"
    },
    "menu_exit": {
        "ru": "0. 🚪 Выход",
        "en": "0. 🚪 Exit"
    },
    "menu_choice": {
        "ru": "Выберите пункт: ",
        "en": "Choose option: "
    },
    "menu_invalid": {
        "ru": "❌ Неверный выбор, попробуйте ещё раз.",
        "en": "❌ Invalid choice, try again."
    },

    # ===== ВИДЕО =====
    "video_not_available": {
        "ru": ("⚠️  OpenCV не установлен! Обработка видео недоступна.\n"
               "   Установите: pip install -r requirements-video.txt"),
        "en": ("⚠️  OpenCV not installed! Video processing unavailable.\n"
               "   Install: pip install -r requirements-video.txt")
    },

    # ===== ВВОД ПУТИ =====
    "enter_image_path": {
        "ru": "Введите путь к изображению: ",
        "en": "Enter image path: "
    },
    "enter_folder_path": {
        "ru": "Введите путь к папке: ",
        "en": "Enter folder path: "
    },
    "enter_video_path": {
        "ru": "Введите путь к видео: ",
        "en": "Enter video path: "
    },
    "enter_gif_path": {
        "ru": "Введите путь к GIF: ",
        "en": "Enter GIF path: "
    },
    "file_not_found": {
        "ru": "❌ Файл не найден: {}",
        "en": "❌ File not found: {}"
    },
    "folder_not_found": {
        "ru": "❌ Папка не найдена: {}",
        "en": "❌ Folder not found: {}"
    },
    "unsupported_format": {
        "ru": "❌ Неподдерживаемый формат: {}",
        "en": "❌ Unsupported format: {}"
    },

    # ===== ВЫБОР ПАЛИТРЫ =====
    "choose_palette_title": {
        "ru": "🎨 Выберите палитру (палитры)",
        "en": "🎨 Choose palette(s)"
    },
    "choose_palette_hint": {
        "ru": ("Введите номера через пробел: 1 2 3\n"
               "Или диапазон: 3-16 18 20\n"
               "Или 'all' для всех, 'random' для рандомной: "),
        "en": ("Enter numbers separated by space: 1 2 3\n"
               "Or range: 3-16 18 20\n"
               "Or 'all' for all, 'random' for random: ")
    },
    "invalid_palette_choice": {
        "ru": "❌ Неверный выбор палитры.",
        "en": "❌ Invalid palette choice."
    },

    # ===== ОБРАБОТКА =====
    "processing_start": {
        "ru": "🚀 Начинаем обработку...",
        "en": "🚀 Starting processing..."
    },
    "processing_image": {
        "ru": "🖼  Обработка: {} → палитра '{}'",
        "en": "🖼  Processing: {} → palette '{}'"
    },
    "processing_video_frame": {
        "ru": "🎬 Кадр {}/{}",
        "en": "🎬 Frame {}/{}"
    },
    "processing_gif_frame": {
        "ru": "🎞  GIF кадр {}/{}",
        "en": "🎞  GIF frame {}/{}"
    },
    "processing_done": {
        "ru": "✅ Готово! Сохранено: {}",
        "en": "✅ Done! Saved: {}"
    },
    "processing_batch_done": {
        "ru": "✅ Batch готов! Обработано файлов: {}",
        "en": "✅ Batch done! Files processed: {}"
    },
    "processing_error": {
        "ru": "❌ Ошибка при обработке: {}",
        "en": "❌ Error during processing: {}"
    },

    # ===== КОЛЛАЖ =====
    "collage_creating": {
        "ru": "🧩 Создаём коллаж...",
        "en": "🧩 Creating collage..."
    },
    "collage_done": {
        "ru": "✅ Коллаж сохранён: {}",
        "en": "✅ Collage saved: {}"
    },

    # ===== РУЛЕТКА =====
    "roulette_spinning": {
        "ru": "🎰 Крутим рулетку...",
        "en": "🎰 Spinning roulette..."
    },
    "roulette_result": {
        "ru": "🎯 Выпала палитра: {}",
        "en": "🎯 Palette selected: {}"
    },
    "roulette_full_random": {
        "ru": "🌈 Генерируем полностью рандомную палитру!",
        "en": "🌈 Generating fully random palette!"
    },
    "roulette_menu_existing": {
        "ru": "1. Рандомная из существующих палитр",
        "en": "1. Random from existing palettes"
    },
    "roulette_menu_random": {
        "ru": "2. Полностью рандомные цвета",
        "en": "2. Fully random colors"
    },
    "roulette_apply": {
        "ru": "Применить к изображению? (y/n): ",
        "en": "Apply to image? (y/n): "
    },

    # ===== PIXEL SORT =====
    "pixel_sort_title": {
        "ru": "📊 Pixel Sort",
        "en": "📊 Pixel Sort"
    },
    "pixel_sort_direction": {
        "ru": "Направление (1-горизонтально, 2-вертикально): ",
        "en": "Direction (1-horizontal, 2-vertical): "
    },
    "pixel_sort_threshold": {
        "ru": "Порог яркости (0-255, по умолчанию 50): ",
        "en": "Brightness threshold (0-255, default 50): "
    },

    # ===== НАСТРОЙКИ =====
    "settings_title": {
        "ru": "⚙️  Настройки",
        "en": "⚙️  Settings"
    },
    "settings_change_lang": {
        "ru": "1. 🌐 Сменить язык (сейчас: Русский)",
        "en": "1. 🌐 Change language (current: English)"
    },
    "settings_back": {
        "ru": "0. ↩️  Назад",
        "en": "0. ↩️  Back"
    },

    # ===== ОБЩИЕ ФРАЗЫ =====
    "press_enter": {
        "ru": "\nНажмите Enter для продолжения...",
        "en": "\nPress Enter to continue..."
    },
    "yes_no": {
        "ru": "(д/н): ",
        "en": "(y/n): "
    },
    "goodbye": {
        "ru": "👋 До встречи, бро!",
        "en": "👋 See ya, bro!"
    },
    "batch_recursive": {
        "ru": "Искать рекурсивно во вложенных папках? (y/n): ",
        "en": "Search recursively in subfolders? (y/n): "
    },
    "found_files": {
        "ru": "📂 Найдено файлов: {}",
        "en": "📂 Files found: {}"
    },
    "no_files_found": {
        "ru": "❌ Файлы не найдены.",
        "en": "❌ No files found."
    },
}