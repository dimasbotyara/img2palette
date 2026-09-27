"""
img2palette - Utility Functions
Author: dimasbotyara
"""

import os
import shutil
import re
from config import SUPPORTED_IMAGE_FORMATS, SUPPORTED_VIDEO_FORMATS


def generate_output_filename(
    original_path: str,
    palette_name: str,
    suffix: str = ""
) -> str:
    """
    Генерация имени выходного файла.
    Пример: photo.png → photo_catppuccin-mocha.png
    """
    directory = os.path.dirname(original_path)
    basename = os.path.basename(original_path)
    name, ext = os.path.splitext(basename)

    # Очищаем название палитры для использования в имени файла
    safe_palette = sanitize_filename(palette_name)

    if suffix:
        output_name = f"{name}_{safe_palette}_{suffix}{ext}"
    else:
        output_name = f"{name}_{safe_palette}{ext}"

    return os.path.join(directory, output_name)


def sanitize_filename(name: str) -> str:
    """Очистка строки для использования в имени файла."""
    # Заменяем пробелы на дефисы, убираем спецсимволы
    safe = name.lower().replace(" ", "-").replace("+", "plus")
    safe = re.sub(r'[^\w\-.]', '', safe)
    return safe


def is_image_file(path: str) -> bool:
    """Проверка, является ли файл поддерживаемым изображением."""
    ext = os.path.splitext(path)[1].lower()
    return ext in SUPPORTED_IMAGE_FORMATS


def is_video_file(path: str) -> bool:
    """Проверка, является ли файл поддерживаемым видео."""
    ext = os.path.splitext(path)[1].lower()
    return ext in SUPPORTED_VIDEO_FORMATS


def is_gif_file(path: str) -> bool:
    """Проверка, является ли файл GIF."""
    return os.path.splitext(path)[1].lower() == ".gif"


def find_images_in_folder(
    folder_path: str,
    recursive: bool = False
) -> list[str]:
    """Поиск изображений в папке."""
    images = []
    if recursive:
        for root, dirs, files in os.walk(folder_path):
            for f in sorted(files):
                full_path = os.path.join(root, f)
                if is_image_file(full_path):
                    images.append(full_path)
    else:
        for f in sorted(os.listdir(folder_path)):
            full_path = os.path.join(folder_path, f)
            if os.path.isfile(full_path) and is_image_file(full_path):
                images.append(full_path)
    return images


def copy_file(src: str, dst: str) -> str:
    """Копирование файла. Возвращает путь к копии."""
    shutil.copy2(src, dst)
    return dst


def parse_palette_selection(
    user_input: str,
    max_index: int
) -> list[int]:
    """
    Парсинг пользовательского выбора палитр.
    Поддерживает:
      - Одиночные номера: "1 2 3"
      - Диапазоны: "3-16 18 20"
      - "all" — все палитры
      - "random" — одна рандомная

    Возвращает список 1-based индексов.
    """
    user_input = user_input.strip().lower()

    if user_input == "all":
        return list(range(1, max_index + 1))

    if user_input == "random":
        return [-1]  # Специальное значение для "рандом"

    indices = set()
    parts = user_input.split()

    for part in parts:
        part = part.strip()
        if not part:
            continue

        # Проверяем диапазон (например, "3-16")
        range_match = re.match(r'^(\d+)-(\d+)$', part)
        if range_match:
            start = int(range_match.group(1))
            end = int(range_match.group(2))
            if start > end:
                start, end = end, start
            for i in range(start, end + 1):
                if 1 <= i <= max_index:
                    indices.add(i)
        elif part.isdigit():
            idx = int(part)
            if 1 <= idx <= max_index:
                indices.add(idx)

    return sorted(indices)


def format_file_size(size_bytes: int) -> str:
    """Форматирование размера файла."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"


def get_file_info(path: str) -> dict:
    """Информация о файле."""
    stat = os.stat(path)
    return {
        "path": path,
        "name": os.path.basename(path),
        "size": stat.st_size,
        "size_formatted": format_file_size(stat.st_size),
        "extension": os.path.splitext(path)[1].lower(),
    }