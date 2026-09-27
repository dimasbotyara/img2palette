"""
img2palette - User Interface (Rich)
Author: dimasbotyara
"""

import os
import random
import time

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.progress import (
    Progress, BarColumn, TextColumn,
    TimeRemainingColumn, SpinnerColumn, MofNCompleteColumn
)
from rich.columns import Columns
from rich.prompt import Prompt
from rich import box

from locale_manager import locale
from palettes import PALETTES, get_palette_count, get_palette_by_index
from config import (
    is_opencv_available, COLLAGE_THUMB_SIZE, COLLAGE_MAX_COLUMNS
)
from utils import (
    parse_palette_selection, generate_output_filename,
    find_images_in_folder, is_image_file, is_gif_file,
    is_video_file, get_file_info
)
from processor import process_image_file, process_gif
from effects import pixel_sort_file

console = Console()


# =============================================================
# ПЕРВЫЙ ЗАПУСК — ВЫБОР ЯЗЫКА
# =============================================================
def first_run_setup():
    """Экран первого запуска — выбор языка."""
    console.clear()
    console.print()
    console.print(
        Panel(
            "[bold cyan]🎨 img2palette[/bold cyan]\n"
            "[dim]by dimasbotyara[/dim]",
            box=box.DOUBLE,
            border_style="bright_magenta",
        ),
        justify="center"
    )
    console.print()
    console.print("  1. 🇷🇺 Русский")
    console.print("  2. 🇬🇧 English")
    console.print()

    while True:
        choice = Prompt.ask(
            "  Выбери язык / Choose language",
            choices=["1", "2"],
            default="1"
        )
        if choice == "1":
            locale.language = "ru"
            console.print(
                "\n  ✅ Язык установлен: Русский 🇷🇺\n",
                style="bold green"
            )
            break
        elif choice == "2":
            locale.language = "en"
            console.print(
                "\n  ✅ Language set: English 🇬🇧\n",
                style="bold green"
            )
            break

    time.sleep(1)


# =============================================================
# ЗАГОЛОВОК
# =============================================================
def show_header():
    """Показать заголовок приложения."""
    title = locale.get("app_title")
    subtitle = locale.get("app_subtitle")

    console.print()
    console.print(
        Panel(
            f"[bold bright_cyan]{title}[/bold bright_cyan]\n"
            f"[dim]{subtitle}[/dim]",
            box=box.HEAVY,
            border_style="bright_magenta",
            padding=(1, 4),
        ),
        justify="center"
    )


# =============================================================
# ГЛАВНОЕ МЕНЮ
# =============================================================
def show_main_menu() -> str:
    """Показать главное меню. Возвращает выбор пользователя."""

    video_available = is_opencv_available()
    video_suffix = "" if video_available else " [dim red](N/A)[/dim red]"

    menu_items = [
        ("1", locale.get("menu_single")),
        ("2", locale.get("menu_batch")),
        ("3", locale.get("menu_video") + video_suffix),
        ("4", locale.get("menu_gif")),
        ("5", locale.get("menu_collage")),
        ("6", locale.get("menu_preview")),
        ("7", locale.get("menu_roulette")),
        ("8", locale.get("menu_pixel_sort")),
        ("9", locale.get("menu_settings")),
        ("0", locale.get("menu_exit")),
    ]

    table = Table(
        box=box.ROUNDED,
        border_style="bright_blue",
        title=locale.get("menu_title"),
        title_style="bold bright_yellow",
        show_header=False,
        padding=(0, 2),
    )
    table.add_column("", style="bold cyan", width=4)
    table.add_column("")

    for key, label in menu_items:
        table.add_row(f"[{key}]", label)

    console.print()
    console.print(table, justify="center")
    console.print()

    choice = Prompt.ask(
        f"  {locale.get('menu_choice')}",
        choices=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
        default="0"
    )
    return choice


# =============================================================
# ПРЕВЬЮ ПАЛИТР В ТЕРМИНАЛЕ
# =============================================================
def show_palette_preview(palette_indices: list[int] | None = None):
    """
    Показать цветные блоки палитр в терминале.
    Если palette_indices=None, показывает все.
    """
    if palette_indices is None:
        palette_indices = list(range(1, get_palette_count() + 1))

    for idx in palette_indices:
        pal = get_palette_by_index(idx)
        if not pal:
            continue

        lang = locale.language or "en"
        name = pal.get("name_ru", pal["name"]) if lang == "ru" else pal["name"]

        # Строка цветных блоков
        color_blocks = Text()
        for r, g, b in pal["colors"]:
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            color_blocks.append("██", style=hex_color)

        panel = Panel(
            color_blocks,
            title=f"[bold]{idx}. {name}[/bold]",
            title_align="left",
            subtitle=f"[dim]{len(pal['colors'])} colors | {pal['category']}[/dim]",
            subtitle_align="right",
            border_style="bright_blue",
            width=min(console.width - 4, 80),
        )
        console.print(panel)


# =============================================================
# ВЫБОР ПАЛИТРЫ
# =============================================================
def choose_palettes() -> list[int]:
    """
    Интерактивный выбор палитр.
    Возвращает список 1-based индексов.
    """
    console.print()
    show_palette_list_compact()
    console.print()

    hint = locale.get("choose_palette_hint")
    console.print(f"  {hint}")

    user_input = console.input("  > ").strip()

    if not user_input:
        return []

    indices = parse_palette_selection(user_input, get_palette_count())

    # Обработка "random"
    if indices == [-1]:
        idx = random.randint(1, get_palette_count())
        pal = get_palette_by_index(idx)
        lang = locale.language or "en"
        name = pal.get("name_ru", pal["name"]) if lang == "ru" else pal["name"]
        console.print(
            f"\n  🎲 {locale.get('roulette_result', name)}",
            style="bold bright_green"
        )
        return [idx]

    if not indices:
        console.print(
            f"  {locale.get('invalid_palette_choice')}",
            style="bold red"
        )
        return []

    return indices


def show_palette_list_compact():
    """Компактный список всех палитр (таблица)."""
    table = Table(
        box=box.SIMPLE_HEAVY,
        border_style="bright_blue",
        title=locale.get("choose_palette_title"),
        title_style="bold bright_yellow",
    )
    table.add_column("#", style="bold cyan", justify="right", width=4)
    table.add_column(
        "Palette" if locale.language == "en" else "Палитра",
        style="bold white", min_width=25
    )
    table.add_column(
        "Category" if locale.language == "en" else "Категория",
        style="dim", min_width=12
    )
    table.add_column(
        "Colors" if locale.language == "en" else "Цвета",
        justify="center", width=8
    )
    table.add_column(
        "Preview" if locale.language == "en" else "Превью",
        min_width=20
    )

    for i, pal in enumerate(PALETTES, 1):
        lang = locale.language or "en"
        name = pal.get("name_ru", pal["name"]) if lang == "ru" else pal["name"]

        # Мини-превью (первые 10 цветов)
        preview = Text()
        for r, g, b in pal["colors"][:10]:
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            preview.append("█", style=hex_color)
        if len(pal["colors"]) > 10:
            preview.append("…", style="dim")

        table.add_row(
            str(i),
            name,
            pal["category"],
            str(len(pal["colors"])),
            preview
        )

    console.print(table)


# =============================================================
# ОБРАБОТКА ОДНОГО ИЗОБРАЖЕНИЯ
# =============================================================
def handle_single_image():
    """Обработка одного изображения."""
    console.print()
    path = console.input(f"  {locale.get('enter_image_path')}").strip()
    path = path.strip('"').strip("'")

    if not os.path.isfile(path):
        console.print(
            f"  {locale.get('file_not_found', path)}", style="bold red"
        )
        return

    if not is_image_file(path):
        console.print(
            f"  {locale.get('unsupported_format', path)}", style="bold red"
        )
        return

    # Показываем инфо о файле
    info = get_file_info(path)
    console.print(
        f"\n  📄 {info['name']} ({info['size_formatted']})",
        style="bright_cyan"
    )

    # Выбор палитр
    palette_indices = choose_palettes()
    if not palette_indices:
        return

    console.print(f"\n  {locale.get('processing_start')}", style="bold green")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=30),
        MofNCompleteColumn(),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        task = progress.add_task(
            "Processing...", total=len(palette_indices)
        )

        for idx in palette_indices:
            pal = get_palette_by_index(idx)
            if not pal:
                continue

            output_path = generate_output_filename(path, pal["name"])

            lang = locale.language or "en"
            name = (
                pal.get("name_ru", pal["name"])
                if lang == "ru" else pal["name"]
            )
            progress.update(
                task,
                description=f"🎨 {name}"
            )

            try:
                process_image_file(path, output_path, pal["colors"])
                console.print(
                    f"  {locale.get('processing_done', output_path)}",
                    style="green"
                )
            except Exception as e:
                console.print(
                    f"  {locale.get('processing_error', str(e))}",
                    style="bold red"
                )

            progress.advance(task)

    _press_enter()


# =============================================================
# BATCH ОБРАБОТКА
# =============================================================
def handle_batch():
    """Обработка папки с изображениями."""
    console.print()
    folder = console.input(f"  {locale.get('enter_folder_path')}").strip()
    folder = folder.strip('"').strip("'")

    if not os.path.isdir(folder):
        console.print(
            f"  {locale.get('folder_not_found', folder)}", style="bold red"
        )
        return

    # Рекурсивный поиск?
    recursive_input = console.input(
        f"  {locale.get('batch_recursive')}"
    ).strip().lower()
    recursive = recursive_input in ("y", "д", "yes", "да", "1")

    images = find_images_in_folder(folder, recursive)

    if not images:
        console.print(f"  {locale.get('no_files_found')}", style="bold red")
        return

    console.print(
        f"  {locale.get('found_files', len(images))}",
        style="bright_cyan"
    )

    # Выбор палитр
    palette_indices = choose_palettes()
    if not palette_indices:
        return

    total_ops = len(images) * len(palette_indices)

    console.print(f"\n  {locale.get('processing_start')}", style="bold green")

    processed = 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=30),
        MofNCompleteColumn(),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Batch...", total=total_ops)

        for img_path in images:
            for idx in palette_indices:
                pal = get_palette_by_index(idx)
                if not pal:
                    continue

                output_path = generate_output_filename(
                    img_path, pal["name"]
                )

                progress.update(
                    task,
                    description=(
                        f"🎨 {os.path.basename(img_path)} → "
                        f"{pal['name']}"
                    )
                )

                try:
                    process_image_file(
                        img_path, output_path, pal["colors"]
                    )
                    processed += 1
                except Exception as e:
                    console.print(
                        f"  {locale.get('processing_error', str(e))}",
                        style="bold red"
                    )

                progress.advance(task)

    console.print(
        f"\n  {locale.get('processing_batch_done', processed)}",
        style="bold green"
    )
    _press_enter()


# =============================================================
# ВИДЕО
# =============================================================
def handle_video():
    """Обработка видео."""
    if not is_opencv_available():
        console.print(
            f"\n  {locale.get('video_not_available')}",
            style="bold yellow"
        )
        _press_enter()
        return

    console.print()
    path = console.input(f"  {locale.get('enter_video_path')}").strip()
    path = path.strip('"').strip("'")

    if not os.path.isfile(path):
        console.print(
            f"  {locale.get('file_not_found', path)}", style="bold red"
        )
        return

    if not is_video_file(path):
        console.print(
            f"  {locale.get('unsupported_format', path)}", style="bold red"
        )
        return

    from video_processor import get_video_info, process_video

    try:
        info = get_video_info(path)
        console.print(
            f"\n  📹 {os.path.basename(path)}: "
            f"{info['width']}x{info['height']}, "
            f"{info['fps']:.1f} FPS, "
            f"{info['frame_count']} frames, "
            f"{info['duration']:.1f}s",
            style="bright_cyan"
        )
    except Exception as e:
        console.print(
            f"  {locale.get('processing_error', str(e))}",
            style="bold red"
        )
        return

    # Выбор палитры (для видео — только одна за раз)
    palette_indices = choose_palettes()
    if not palette_indices:
        return

    console.print(f"\n  {locale.get('processing_start')}", style="bold green")

    for idx in palette_indices:
        pal = get_palette_by_index(idx)
        if not pal:
            continue

        output_path = generate_output_filename(path, pal["name"])

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=30),
            MofNCompleteColumn(),
            TimeRemainingColumn(),
            console=console,
        ) as progress:
            task = progress.add_task(
                f"🎬 {pal['name']}",
                total=info["frame_count"]
            )

            def video_progress(current, total):
                progress.update(task, completed=current)

            try:
                process_video(
                    path, output_path, pal["colors"],
                    progress_callback=video_progress
                )
                console.print(
                    f"  {locale.get('processing_done', output_path)}",
                    style="green"
                )
            except Exception as e:
                console.print(
                    f"  {locale.get('processing_error', str(e))}",
                    style="bold red"
                )

    _press_enter()


# =============================================================
# GIF
# =============================================================
def handle_gif():
    """Обработка GIF."""
    console.print()
    path = console.input(f"  {locale.get('enter_gif_path')}").strip()
    path = path.strip('"').strip("'")

    if not os.path.isfile(path):
        console.print(
            f"  {locale.get('file_not_found', path)}", style="bold red"
        )
        return

    if not is_gif_file(path):
        console.print(
            f"  {locale.get('unsupported_format', path)}", style="bold red"
        )
        return

    from PIL import Image as PILImage
    gif = PILImage.open(path)
    n_frames = getattr(gif, 'n_frames', 1)
    gif.close()

    info = get_file_info(path)
    console.print(
        f"\n  🎞  {info['name']} ({info['size_formatted']}, "
        f"{n_frames} frames)",
        style="bright_cyan"
    )

    palette_indices = choose_palettes()
    if not palette_indices:
        return

    console.print(f"\n  {locale.get('processing_start')}", style="bold green")

    for idx in palette_indices:
        pal = get_palette_by_index(idx)
        if not pal:
            continue

        output_path = generate_output_filename(path, pal["name"])

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=30),
            MofNCompleteColumn(),
            TimeRemainingColumn(),
            console=console,
        ) as progress:
            task = progress.add_task(
                f"🎞  {pal['name']}", total=n_frames
            )

            def gif_progress(current, total):
                progress.update(task, completed=current)

            try:
                process_gif(
                    path, output_path, pal["colors"],
                    progress_callback=gif_progress
                )
                console.print(
                    f"  {locale.get('processing_done', output_path)}",
                    style="green"
                )
            except Exception as e:
                console.print(
                    f"  {locale.get('processing_error', str(e))}",
                    style="bold red"
                )

    _press_enter()

# =============================================================
# КОЛЛАЖ
# =============================================================
def handle_collage():
    """Создать коллаж — одно фото во всех (или выбранных) палитрах."""
    console.print()
    path = console.input(f"  {locale.get('enter_image_path')}").strip()
    path = path.strip('"').strip("'")

    if not os.path.isfile(path) or not is_image_file(path):
        console.print(
            f"  {locale.get('file_not_found', path)}", style="bold red"
        )
        return

    palette_indices = choose_palettes()
    if not palette_indices:
        return

    console.print(
        f"\n  {locale.get('collage_creating')}", style="bold green"
    )

    from PIL import Image as PILImage, ImageDraw, ImageFont
    from processor import process_image

    original = PILImage.open(path).convert("RGB")

    thumb_w, thumb_h = COLLAGE_THUMB_SIZE
    # Масштабируем с сохранением пропорций
    original.thumbnail((thumb_w, thumb_h), PILImage.Resampling.LANCZOS)
    thumb_w, thumb_h = original.size

    label_height = 30
    cell_w = thumb_w
    cell_h = thumb_h + label_height

    n = len(palette_indices)
    cols = min(n, COLLAGE_MAX_COLUMNS)
    rows = (n + cols - 1) // cols

    collage_w = cols * cell_w
    collage_h = rows * cell_h
    collage = PILImage.new("RGB", (collage_w, collage_h), (30, 30, 30))

    draw = ImageDraw.Draw(collage)

    # Пробуем загрузить шрифт
    try:
        font = ImageFont.truetype("arial.ttf", 14)
    except (IOError, OSError):
        try:
            font = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14
            )
        except (IOError, OSError):
            font = ImageFont.load_default()

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=30),
        MofNCompleteColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("🧩 Collage", total=n)

        for i, idx in enumerate(palette_indices):
            pal = get_palette_by_index(idx)
            if not pal:
                continue

            # Обработка миниатюры
            processed = process_image(original.copy(), pal["colors"])
            processed = processed.resize(
                (thumb_w, thumb_h), PILImage.Resampling.LANCZOS
            )

            # Позиция в коллаже
            col = i % cols
            row = i // cols
            x = col * cell_w
            y = row * cell_h

            collage.paste(processed, (x, y))

            # Подпись
            lang = locale.language or "en"
            name = (
                pal.get("name_ru", pal["name"])
                if lang == "ru" else pal["name"]
            )
            label_y = y + thumb_h + 2
            draw.text(
                (x + 5, label_y), name,
                fill=(255, 255, 255), font=font
            )

            processed.close()
            progress.advance(task)

    # Сохраняем коллаж
    output_path = generate_output_filename(path, "collage")
    # Коллаж всегда PNG
    output_path = os.path.splitext(output_path)[0] + ".png"
    collage.save(output_path, "PNG")
    collage.close()
    original.close()

    console.print(
        f"\n  {locale.get('collage_done', output_path)}",
        style="bold green"
    )
    _press_enter()


# =============================================================
# РУЛЕТКА
# =============================================================
def handle_roulette():
    """Рулетка — рандомная палитра или полный рандом."""
    console.print()
    console.print(f"  {locale.get('roulette_menu_existing')}")
    console.print(f"  {locale.get('roulette_menu_random')}")
    console.print()

    choice = Prompt.ask("  Choice", choices=["1", "2"], default="1")

    if choice == "1":
        # Рандомная существующая
        idx = random.randint(1, get_palette_count())
        pal = get_palette_by_index(idx)

        console.print(
            f"\n  {locale.get('roulette_spinning')}", style="bold yellow"
        )
        time.sleep(1)

        lang = locale.language or "en"
        name = (
            pal.get("name_ru", pal["name"])
            if lang == "ru" else pal["name"]
        )

        console.print(
            f"  {locale.get('roulette_result', name)} (#{idx})",
            style="bold bright_green"
        )

        # Превью
        show_palette_preview([idx])
        selected_colors = pal["colors"]
        selected_name = pal["name"]

    else:
        # Полностью рандомная палитра
        console.print(
            f"\n  {locale.get('roulette_full_random')}",
            style="bold bright_magenta"
        )
        time.sleep(0.5)

        num_colors = random.randint(4, 20)
        random_colors = [
            (random.randint(0, 255),
             random.randint(0, 255),
             random.randint(0, 255))
            for _ in range(num_colors)
        ]

        # Показываем рандомную палитру
        color_blocks = Text()
        for r, g, b in random_colors:
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            color_blocks.append("██", style=hex_color)
            color_blocks.append(" ")

        console.print(
            Panel(
                color_blocks,
                title="[bold]🌈 Random Palette[/bold]",
                border_style="bright_magenta"
            )
        )

        selected_colors = random_colors
        selected_name = "random"

    # Применить?
    console.print()
    apply_input = console.input(
        f"  {locale.get('roulette_apply')}"
    ).strip().lower()

    if apply_input in ("y", "д", "yes", "да", "1"):
        path = console.input(
            f"  {locale.get('enter_image_path')}"
        ).strip().strip('"').strip("'")

        if os.path.isfile(path) and is_image_file(path):
            output_path = generate_output_filename(path, selected_name)
            try:
                process_image_file(path, output_path, selected_colors)
                console.print(
                    f"  {locale.get('processing_done', output_path)}",
                    style="green"
                )
            except Exception as e:
                console.print(
                    f"  {locale.get('processing_error', str(e))}",
                    style="bold red"
                )
        else:
            console.print(
                f"  {locale.get('file_not_found', path)}",
                style="bold red"
            )

    _press_enter()


# =============================================================
# PIXEL SORT
# =============================================================
def handle_pixel_sort():
    """Pixel Sort эффект."""
    console.print()
    console.print(
        Panel(
            locale.get("pixel_sort_title"),
            border_style="bright_magenta"
        )
    )

    path = console.input(f"  {locale.get('enter_image_path')}").strip()
    path = path.strip('"').strip("'")

    if not os.path.isfile(path) or not is_image_file(path):
        console.print(
            f"  {locale.get('file_not_found', path)}", style="bold red"
        )
        return

    # Направление
    dir_input = console.input(
        f"  {locale.get('pixel_sort_direction')}"
    ).strip()
    direction = "vertical" if dir_input == "2" else "horizontal"

    # Порог
    thresh_input = console.input(
        f"  {locale.get('pixel_sort_threshold')}"
    ).strip()
    try:
        threshold = int(thresh_input) if thresh_input else 50
        threshold = max(0, min(255, threshold))
    except ValueError:
        threshold = 50

    output_path = generate_output_filename(
        path, f"pixelsort-{direction}-{threshold}"
    )

    console.print(f"\n  {locale.get('processing_start')}", style="bold green")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=30),
        console=console,
    ) as progress:
        task = progress.add_task("📊 Pixel Sort...", total=100)

        def sort_progress(current, total):
            if total > 0:
                pct = int(current / total * 100)
                progress.update(task, completed=pct)

        try:
            pixel_sort_file(
                path, output_path, direction, threshold, sort_progress
            )
            progress.update(task, completed=100)
            console.print(
                f"\n  {locale.get('processing_done', output_path)}",
                style="green"
            )
        except Exception as e:
            console.print(
                f"  {locale.get('processing_error', str(e))}",
                style="bold red"
            )

    _press_enter()


# =============================================================
# НАСТРОЙКИ
# =============================================================
def handle_settings():
    """Экран настроек."""
    console.print()
    console.print(
        Panel(
            locale.get("settings_title"),
            border_style="bright_yellow"
        )
    )
    console.print(f"  {locale.get('settings_change_lang')}")
    console.print(f"  {locale.get('settings_back')}")
    console.print()

    choice = Prompt.ask("  Choice", choices=["0", "1"], default="0")

    if choice == "1":
        console.print("\n  1. 🇷🇺 Русский")
        console.print("  2. 🇬🇧 English")
        lang_choice = Prompt.ask(
            "  Select", choices=["1", "2"], default="1"
        )
        if lang_choice == "1":
            locale.language = "ru"
            console.print(
                "\n  ✅ Язык: Русский 🇷🇺", style="bold green"
            )
        else:
            locale.language = "en"
            console.print(
                "\n  ✅ Language: English 🇬🇧", style="bold green"
            )
        time.sleep(1)


# =============================================================
# УТИЛИТЫ UI
# =============================================================
def _press_enter():
    """Ожидание нажатия Enter."""
    console.input(f"  {locale.get('press_enter')}")