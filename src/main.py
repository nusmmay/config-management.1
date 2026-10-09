#!/usr/bin/env python3
"""
Инструмент визуализации графа зависимостей для менеджера пакетов.
Вариант 15.
Этап 1: минимальный прототип с конфигурацией.
Этап 2: сбор данных о прямых зависимостях.
Этап 3: основные операции (BFS, циклы, фильтр, тестовый режим).
"""

import argparse
import sys

from cargo_api import fetch_dependencies
from graph import DependencyGraph


def parse_arguments():
    """Разбор аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Инструмент визуализации графа зависимостей пакетов"
    )

    parser.add_argument("--package", "-p", type=str, required=True,
                        help="Имя анализируемого пакета")
    parser.add_argument("--version", "-v", type=str, required=True,
                        help="Версия анализируемого пакета")
    parser.add_argument("--repo", "-r", type=str, required=True,
                        help="URL репозитория или путь к тестовому файлу")
    parser.add_argument("--test-mode", "-t", action="store_true",
                        help="Режим работы с тестовым репозиторием")
    parser.add_argument("--output", "-o", type=str, default="graph.png",
                        help="Имя файла с изображением графа")
    parser.add_argument("--ascii-tree", "-a", action="store_true",
                        help="Вывод зависимостей в формате ASCII-дерева")
    parser.add_argument("--filter", "-f", type=str, default="",
                        help="Подстрока для фильтрации пакетов")
    parser.add_argument("--max-depth", "-d", type=int, default=None,
                        help="Максимальная глубина анализа")

    return parser.parse_args()


def validate_arguments(args):
    """Проверка корректности аргументов."""
    errors = []

    if not args.package or not args.package.strip():
        errors.append("Ошибка: имя пакета не может быть пустым.")
    if not args.version or not args.version.strip():
        errors.append("Ошибка: версия пакета не может быть пустой.")
    if not args.repo or not args.repo.strip():
        errors.append("Ошибка: URL репозитория не может быть пустым.")
    if not args.output.endswith((".png", ".svg")):
        errors.append("Ошибка: имя файла должно заканчиваться на .png или .svg.")
    if args.max_depth is not None and args.max_depth < 0:
        errors.append("Ошибка: максимальная глубина не может быть отрицательной.")

    if errors:
        for err in errors:
            print(err, file=sys.stderr)
        sys.exit(1)


def print_parameters(args):
    """Вывод параметров в формате ключ-значение."""
    print("=" * 50)
    print("Параметры запуска:")
    print("=" * 50)
    print(f"package      = {args.package}")
    print(f"version      = {args.version}")
    print(f"repo         = {args.repo}")
    print(f"test_mode    = {args.test_mode}")
    print(f"output       = {args.output}")
    print(f"ascii_tree   = {args.ascii_tree}")
    print(f"filter       = '{args.filter}'")
    print(f"max_depth    = {args.max_depth}")
    print("=" * 50)


def load_graph_from_crates(args):
    """Загрузка графа через crates.io (обычный режим)."""
    graph = DependencyGraph()
    deps = fetch_dependencies(args.package, args.version, args.repo)
    dep_names = [d.get("crate_id") for d in deps if d.get("crate_id")]
    graph.add_package(args.package, dep_names)
    for name in dep_names:
        graph.add_package(name, [])
    return graph


def load_graph_from_file(args):
    """Загрузка графа из JSON-файла (тестовый режим)."""
    graph = DependencyGraph()
    graph.load_from_file(args.repo)
    return graph


def main():
    args = parse_arguments()
    validate_arguments(args)
    print_parameters(args)

    try:
        if args.test_mode:
            graph = load_graph_from_file(args)
        else:
            graph = load_graph_from_crates(args)

        order = graph.build(
            args.package,
            max_depth=args.max_depth,
            filter_substring=args.filter
        )

        print("")
        print(f"Порядок обхода зависимостей от '{args.package}':")
        print("-" * 50)
        for name, depth in order:
            indent = "  " * depth
            print(f"{indent}{name} (глубина {depth})")
        print("-" * 50)
        print(f"Всего пакетов: {len(order)}")

        if args.ascii_tree:
            print("")
            print("ASCII-дерево зависимостей:")
            print("-" * 50)
            print(graph.to_ascii_tree(args.package))
            print("-" * 50)

    except ValueError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
