#!/usr/bin/env python3
"""
Инструмент визуализации графа зависимостей для менеджера пакетов.
Вариант 15. Этап 1: минимальный прототип с конфигурацией.
"""

import argparse
import sys


def parse_arguments():
    """Разбор аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Инструмент визуализации графа зависимостей пакетов",
        add_help=True
    )

    parser.add_argument(
        "--package", "-p",
        type=str,
        required=True,
        help="Имя анализируемого пакета"
    )

    parser.add_argument(
        "--repo", "-r",
        type=str,
        required=True,
        help="URL-адрес репозитория или путь к файлу тестового репозитория"
    )

    parser.add_argument(
        "--test-mode", "-t",
        action="store_true",
        help="Режим работы с тестовым репозиторием (флаг)"
    )

    parser.add_argument(
        "--output", "-o",
        type=str,
        default="graph.png",
        help="Имя файла с изображением графа (по умолчанию: graph.png)"
    )

    parser.add_argument(
        "--ascii-tree", "-a",
        action="store_true",
        help="Режим вывода зависимостей в формате ASCII-дерева (флаг)"
    )

    parser.add_argument(
        "--filter", "-f",
        type=str,
        default="",
        help="Подстрока для фильтрации пакетов"
    )

    return parser.parse_args()


def validate_arguments(args):
    """Проверка корректности аргументов."""
    errors = []

    if not args.package or not args.package.strip():
        errors.append("Ошибка: имя пакета не может быть пустым.")

    if not args.repo or not args.repo.strip():
        errors.append("Ошибка: URL репозитория или путь не может быть пустым.")

    if not args.output or not args.output.strip():
        errors.append("Ошибка: имя выходного файла не может быть пустым.")

    if not args.output.endswith((".png", ".svg")):
        errors.append("Ошибка: имя файла должно заканчиваться на .png или .svg.")

    if errors:
        for err in errors:
            print(err, file=sys.stderr)
        sys.exit(1)


def print_parameters(args):
    """Вывод всех параметров в формате ключ-значение."""
    print("=" * 50)
    print("Параметры запуска:")
    print("=" * 50)
    print(f"package      = {args.package}")
    print(f"repo         = {args.repo}")
    print(f"test_mode    = {args.test_mode}")
    print(f"output       = {args.output}")
    print(f"ascii_tree   = {args.ascii_tree}")
    print(f"filter       = '{args.filter}'")
    print("=" * 50)


def main():
    args = parse_arguments()
    validate_arguments(args)
    print_parameters(args)


if __name__ == "__main__":
    main()
