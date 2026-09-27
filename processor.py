"""
img2palette - Image Processor (Core)
Author: dimasbotyara

Замена пикселей изображения на ближайшие цвета из палитры.
Использует numpy для скорости + экономии ОЗУ.
"""

import numpy as np
from PIL import Image


def build_palette_array(colors: list[tuple[int, int, int]]) -> np.ndarray:
    """
    Преобразование списка цветов в numpy массив для быстрого поиска.
    Возвращает массив shape (N, 3) dtype uint8.
    """
    return np.array(colors, dtype=np.uint8)


def find_nearest_colors(
    pixels: np.ndarray,
    palette: np.ndarray
) -> np.ndarray:
    """
    Для каждого пикселя находит ближайший цвет в палитре.
    Евклидово расстояние в RGB пространстве.

    pixels: shape (H*W, 3) или (N, 3)
    palette: shape (P, 3)

    Обработка чанками для экономии ОЗУ.
    """
    result = np.empty_like(pixels)
    chunk_size = 50000  # Обрабатываем по 50к пикселей за раз

    palette_float = palette.astype(np.float32)

    for start in range(0, len(pixels), chunk_size):
        end = min(start + chunk_size, len(pixels))
        chunk = pixels[start:end].astype(np.float32)

        # Расстояние от каждого пикселя до каждого цвета палитры
        # chunk: (chunk_size, 3), palette: (P, 3)
        # Разность: (chunk_size, P, 3)
        diff = chunk[:, np.newaxis, :] - palette_float[np.newaxis, :, :]
        distances = np.sum(diff ** 2, axis=2)  # (chunk_size, P)

        # Индексы ближайших цветов
        nearest_indices = np.argmin(distances, axis=1)  # (chunk_size,)

        result[start:end] = palette[nearest_indices]

    return result


def process_image(
    image: Image.Image,
    palette_colors: list[tuple[int, int, int]],
    preserve_alpha: bool = True
) -> Image.Image:
    """
    Обработка одного изображения: замена всех пикселей на ближайшие
    цвета из палитры.

    Args:
        image: PIL Image
        palette_colors: список (R, G, B) кортежей
        preserve_alpha: сохранять альфа-канал если есть

    Returns:
        Новое PIL Image с заменёнными цветами
    """
    has_alpha = image.mode == "RGBA"

    if has_alpha and preserve_alpha:
        # Отделяем альфа-канал
        r, g, b, a = image.split()
        rgb_image = Image.merge("RGB", (r, g, b))
    elif image.mode != "RGB":
        rgb_image = image.convert("RGB")
        has_alpha = False
    else:
        rgb_image = image
        has_alpha = False

    # Преобразуем в numpy
    img_array = np.array(rgb_image)
    original_shape = img_array.shape  # (H, W, 3)
    h, w = original_shape[0], original_shape[1]

    # Плоский массив пикселей
    flat_pixels = img_array.reshape(-1, 3)

    # Палитра
    palette_array = build_palette_array(palette_colors)

    # Замена цветов
    new_pixels = find_nearest_colors(flat_pixels, palette_array)

    # Обратно в форму изображения
    new_array = new_pixels.reshape(h, w, 3)
    new_image = Image.fromarray(new_array.astype(np.uint8), "RGB")

    # Возвращаем альфа-канал
    if has_alpha and preserve_alpha:
        new_image = new_image.convert("RGBA")
        new_image.putalpha(a)

    return new_image


def process_image_file(
    input_path: str,
    output_path: str,
    palette_colors: list[tuple[int, int, int]]
) -> str:
    """
    Обработка файла изображения.
    Открывает → обрабатывает → сохраняет.

    Returns:
        Путь к выходному файлу.
    """
    image = Image.open(input_path)

    # Для ICO и некоторых форматов может быть несколько фреймов
    # Берём первый фрейм
    if hasattr(image, 'n_frames') and image.n_frames > 1:
        image.seek(0)

    result = process_image(image, palette_colors)

    # Определяем формат для сохранения
    save_kwargs = _get_save_kwargs(output_path, image)
    result.save(output_path, **save_kwargs)

    image.close()
    return output_path


def process_gif(
    input_path: str,
    output_path: str,
    palette_colors: list[tuple[int, int, int]],
    progress_callback=None
) -> str:
    """
    Покадровая обработка GIF.
    Читаем кадр за кадром, обрабатываем, собираем обратно.

    Args:
        progress_callback: функция(current_frame, total_frames)

    Returns:
        Путь к выходному файлу.
    """
    gif = Image.open(input_path)

    frames = []
    durations = []
    n_frames = getattr(gif, 'n_frames', 1)

    for i in range(n_frames):
        gif.seek(i)
        frame = gif.copy().convert("RGBA")

        # Обрабатываем кадр
        processed = process_image(frame, palette_colors, preserve_alpha=True)
        frames.append(processed)

        # Длительность кадра
        duration = gif.info.get('duration', 100)
        durations.append(duration)

        if progress_callback:
            progress_callback(i + 1, n_frames)

    # Сохраняем GIF
    if frames:
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=durations,
            loop=gif.info.get('loop', 0),
            disposal=2,
            optimize=False,
        )

    gif.close()

    # Освобождаем память
    for f in frames:
        f.close()
    del frames

    return output_path


def _get_save_kwargs(output_path: str, original_image=None) -> dict:
    """Параметры сохранения для разных форматов."""
    import os
    ext = os.path.splitext(output_path)[1].lower()

    kwargs = {}

    if ext in ('.jpg', '.jpeg'):
        kwargs['format'] = 'JPEG'
        kwargs['quality'] = 95
    elif ext == '.png':
        kwargs['format'] = 'PNG'
    elif ext == '.webp':
        kwargs['format'] = 'WEBP'
        kwargs['quality'] = 95
    elif ext == '.bmp':
        kwargs['format'] = 'BMP'
    elif ext == '.tiff' or ext == '.tif':
        kwargs['format'] = 'TIFF'
    elif ext == '.ico':
        kwargs['format'] = 'ICO'
    elif ext == '.tga':
        kwargs['format'] = 'TGA'
    elif ext in ('.ppm', '.pgm', '.pbm'):
        kwargs['format'] = 'PPM'

    return kwargs