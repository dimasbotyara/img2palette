"""
img2palette - Configuration
Author: dimasbotyara
"""

import json
import os

CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(CONFIG_DIR, "img2palette_config.json")

SUPPORTED_IMAGE_FORMATS = (
    ".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp",
    ".tiff", ".tif", ".ico", ".tga", ".ppm", ".pgm", ".pbm"
)

SUPPORTED_VIDEO_FORMATS = (
    ".mp4", ".avi", ".mkv", ".mov", ".webm", ".flv", ".wmv"
)

MAX_VIDEO_DURATION_SECONDS = 300  # 5 минут макс для безопасности
VIDEO_FRAME_BATCH_SIZE = 10       # кадров за раз (экономия ОЗУ)

COLLAGE_THUMB_SIZE = (320, 240)
COLLAGE_MAX_COLUMNS = 6

DEFAULT_CONFIG = {
    "language": None,  # None = не выбран, "ru" или "en"
    "first_run": True
}


def load_config() -> dict:
    """Загрузка конфигурации из JSON файла."""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            # дополняем отсутствующие ключи дефолтами
            for key, value in DEFAULT_CONFIG.items():
                if key not in data:
                    data[key] = value
            return data
        except (json.JSONDecodeError, IOError):
            return DEFAULT_CONFIG.copy()
    return DEFAULT_CONFIG.copy()


def save_config(cfg: dict) -> None:
    """Сохранение конфигурации в JSON файл."""
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2, ensure_ascii=False)
    except IOError:
        pass


def is_opencv_available() -> bool:
    """Проверка наличия OpenCV без краша."""
    try:
        import cv2  # noqa: F401
        return True
    except ImportError:
        return False