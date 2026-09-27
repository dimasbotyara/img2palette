"""
img2palette - Video Processor
Author: dimasbotyara

Покадровая обработка видео с OpenCV.
OpenCV — опциональная зависимость!
"""

import os
import numpy as np
from PIL import Image
from config import is_opencv_available, MAX_VIDEO_DURATION_SECONDS
from processor import process_image


class VideoProcessingError(Exception):
    """Ошибка обработки видео."""
    pass


def check_opencv():
    """Проверка OpenCV. Выбрасывает исключение если не установлен."""
    if not is_opencv_available():
        raise VideoProcessingError(
            "OpenCV is not installed. "
            "Install with: pip install -r requirements-video.txt"
        )


def get_video_info(video_path: str) -> dict:
    """
    Получение информации о видео.

    Returns:
        dict с ключами: fps, frame_count, width, height, duration
    """
    check_opencv()
    import cv2

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise VideoProcessingError(f"Cannot open video: {video_path}")

    info = {
        "fps": cap.get(cv2.CAP_PROP_FPS),
        "frame_count": int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
        "width": int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
    }
    info["duration"] = (
        info["frame_count"] / info["fps"] if info["fps"] > 0 else 0
    )

    cap.release()
    return info


def process_video(
    input_path: str,
    output_path: str,
    palette_colors: list[tuple[int, int, int]],
    progress_callback=None,
    max_duration: int = MAX_VIDEO_DURATION_SECONDS
) -> str:
    """
    Покадровая обработка видео.
    Читаем кадр → PIL → палитра → записываем.
    Минимальное использование ОЗУ!

    Args:
        input_path: путь к входному видео
        output_path: путь для сохранения
        palette_colors: цвета палитры
        progress_callback: функция(current_frame, total_frames)
        max_duration: максимальная длительность в секундах

    Returns:
        Путь к выходному файлу.
    """
    check_opencv()
    import cv2

    # Открываем входное видео
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise VideoProcessingError(f"Cannot open video: {input_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration = total_frames / fps if fps > 0 else 0

    if duration > max_duration:
        cap.release()
        raise VideoProcessingError(
            f"Video too long: {duration:.0f}s "
            f"(max {max_duration}s)"
        )

    # Определяем кодек для выходного видео
    ext = os.path.splitext(output_path)[1].lower()
    fourcc = _get_fourcc(ext)

    # Открываем writer
    writer = cv2.VideoWriter(
        output_path, fourcc, fps, (width, height)
    )

    if not writer.isOpened():
        cap.release()
        raise VideoProcessingError(
            f"Cannot create output video: {output_path}"
        )

    frame_idx = 0

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # BGR → RGB → PIL
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb_frame)

            # Обрабатываем палитрой
            processed = process_image(pil_image, palette_colors)

            # PIL → numpy → BGR
            processed_array = np.array(processed)
            bgr_frame = cv2.cvtColor(processed_array, cv2.COLOR_RGB2BGR)

            writer.write(bgr_frame)

            frame_idx += 1

            if progress_callback:
                progress_callback(frame_idx, total_frames)

            # Явно освобождаем память
            del rgb_frame, pil_image, processed, processed_array, bgr_frame

    finally:
        cap.release()
        writer.release()

    return output_path


def _get_fourcc(ext: str):
    """Получение FourCC кодека по расширению."""
    import cv2

    codecs = {
        '.mp4': 'mp4v',
        '.avi': 'XVID',
        '.mkv': 'X264',
        '.mov': 'mp4v',
        '.webm': 'VP80',
        '.flv': 'FLV1',
        '.wmv': 'WMV2',
    }

    codec_str = codecs.get(ext, 'mp4v')
    return cv2.VideoWriter_fourcc(*codec_str)