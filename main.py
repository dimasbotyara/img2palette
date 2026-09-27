#!/usr/bin/env python3
"""
img2palette — Image to Palette Converter
Author: dimasbotyara

Превращает изображения, GIF и видео в палитры из тем
вроде Catppuccin, Dracula, Nord и других (50+ палитр).

Usage:
    python main.py
"""

import sys

from rich.console import Console

console = Console()


def main():
    """Главная функция приложения."""
    # Импорты внутри main для красивой обработки ошибок
    try:
        from locale_manager import locale
        from ui import (
            first_run_setup,
            show_header,
            show_main_menu,
            show_palette_preview,
            handle_single_image,
            handle_batch,
            handle_video,
            handle_gif,
            handle_collage,
            handle_roulette,
            handle_pixel_sort,
            handle_settings,
        )
    except ImportError as e:
        console.print(
            f"[bold red]❌ Missing dependency: {e}[/bold red]"
        )
        console.print(
            "[yellow]Install requirements: "
            "pip install -r requirements.txt[/yellow]"
        )
        sys.exit(1)

    # Первый запуск — выбор языка
    if locale.is_first_run or locale.language is None:
        first_run_setup()

    # Главный цикл
    while True:
        try:
            console.clear()
            show_header()
            choice = show_main_menu()

            if choice == "0":
                console.print(
                    f"\n  {locale.get('goodbye')}\n",
                    style="bold bright_magenta"
                )
                break
            elif choice == "1":
                handle_single_image()
            elif choice == "2":
                handle_batch()
            elif choice == "3":
                handle_video()
            elif choice == "4":
                handle_gif()
            elif choice == "5":
                handle_collage()
            elif choice == "6":
                console.clear()
                show_header()
                show_palette_preview()
                from ui import _press_enter
                _press_enter()
            elif choice == "7":
                handle_roulette()
            elif choice == "8":
                handle_pixel_sort()
            elif choice == "9":
                handle_settings()

        except KeyboardInterrupt:
            console.print(
                f"\n\n  {locale.get('goodbye')}\n",
                style="bold bright_magenta"
            )
            break
        except Exception as e:
            console.print(
                f"\n  [bold red]❌ Unexpected error: {e}[/bold red]"
            )
            console.print("[dim]Press Enter to continue...[/dim]")
            console.input()


if __name__ == "__main__":
    main()