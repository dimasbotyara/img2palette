"""
img2palette - Effects (Pixel Sort)
Author: dimasbotyara
"""

import numpy as np
from PIL import Image


def pixel_sort(
    image: Image.Image,
    direction: str = "horizontal",
    threshold: int = 50,
    progress_callback=None
) -> Image.Image:
    """
    Pixel Sort эффект — сортировка пикселей по яркости.

    Args:
        image: входное PIL Image
        direction: "horizontal" или "vertical"
        threshold: порог яркости (0-255). Пиксели темнее порога —
                   начало/конец «зон» сортировки.
        progress_callback: функция(current, total)

    Returns:
        Новое изображение с pixel sort эффектом.
    """
    img = image.convert("RGB")
    arr = np.array(img)

    if direction == "vertical":
        arr = np.transpose(arr, (1, 0, 2))  # Поворачиваем

    h, w, _ = arr.shape

    for row_idx in range(h):
        row = arr[row_idx]
        # Вычисляем яркость каждого пикселя
        brightness = (
            0.299 * row[:, 0] +
            0.587 * row[:, 1] +
            0.114 * row[:, 2]
        )

        # Находим зоны для сортировки
        # Зона = непрерывный отрезок пикселей ярче порога
        mask = brightness > threshold

        # Ищем начала и концы зон
        zones = _find_zones(mask)

        for start, end in zones:
            if end - start < 2:
                continue
            segment = row[start:end].copy()
            seg_brightness = brightness[start:end]
            sort_indices = np.argsort(seg_brightness)
            arr[row_idx, start:end] = segment[sort_indices]

        if progress_callback and row_idx % 50 == 0:
            progress_callback(row_idx, h)

    if direction == "vertical":
        arr = np.transpose(arr, (1, 0, 2))

    result = Image.fromarray(arr.astype(np.uint8))
    return result


def _find_zones(mask: np.ndarray) -> list[tuple[int, int]]:
    """
    Находит непрерывные зоны True в маске.
    Возвращает список (start, end) пар.
    """
    zones = []
    in_zone = False
    start = 0

    for i, val in enumerate(mask):
        if val and not in_zone:
            start = i
            in_zone = True
        elif not val and in_zone:
            zones.append((start, i))
            in_zone = False

    if in_zone:
        zones.append((start, len(mask)))

    return zones


def pixel_sort_file(
    input_path: str,
    output_path: str,
    direction: str = "horizontal",
    threshold: int = 50,
    progress_callback=None
) -> str:
    """
    Pixel Sort для файла.
    """
    image = Image.open(input_path)
    result = pixel_sort(
        image, direction, threshold, progress_callback
    )
    result.save(output_path)
    image.close()
    return output_path