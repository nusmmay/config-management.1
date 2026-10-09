"""
Модуль построения графа зависимостей.
Реализация BFS с рекурсией, обработка циклов, фильтрация.
"""

import json
import os


class DependencyGraph:
    """
    Граф зависимостей пакетов.

    Хранит словарь: пакет -> список зависимостей.
    Позволяет обходить граф через BFS с рекурсией.
    """

    def __init__(self):
        self.graph = {}
        self.visited = set()
        self.order = []

    def add_package(self, name, dependencies=None):
        """Добавить пакет и его прямые зависимости."""
        self.graph[name] = list(dependencies or [])

    def load_from_file(self, path):
        """Загрузить граф из JSON-файла (тестовый режим)."""
        if not os.path.exists(path):
            raise ValueError(f"Файл не найден: {path}")

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            raise ValueError(f"Не удалось разобрать JSON: {path}")

        if not isinstance(data, dict):
            raise ValueError("Файл должен содержать словарь пакетов.")

        self.graph = data

    def bfs_recursive(self, start, max_depth=None, filter_substring="",
                      depth=0):
        """
        Обход графа через BFS с рекурсией.

        :param start: имя стартового пакета
        :param max_depth: максимальная глубина (None — без ограничения)
        :param filter_substring: подстрока для фильтрации пакетов
        :param depth: текущая глубина (для рекурсии)
        """
        if start in self.visited:
            return

        if max_depth is not None and depth > max_depth:
            return

        if filter_substring and filter_substring in start:
            return

        self.visited.add(start)
        self.order.append((start, depth))

        if start not in self.graph:
            return

        for dep in self.graph[start]:
            self.bfs_recursive(
                dep,
                max_depth=max_depth,
                filter_substring=filter_substring,
                depth=depth + 1
            )

    def build(self, start, max_depth=None, filter_substring=""):
        """Построить граф обходом от стартового пакета."""
        self.visited = set()
        self.order = []
        self.bfs_recursive(start, max_depth, filter_substring)
        return self.order

    def to_ascii_tree(self, start):
        """Вывести граф в виде ASCII-дерева."""
        lines = []
        visited_branch = set()

        def _walk(node, prefix="", is_last=True):
            connector = "└── " if is_last else "├── "
            lines.append(f"{prefix}{connector}{node}")
            if node in visited_branch:
                lines.append(f"{prefix}    (цикл)")
                return
            visited_branch.add(node)
            children = self.graph.get(node, [])
            for i, child in enumerate(children):
                _walk(child, prefix + ("    " if is_last else "│   "),
                      i == len(children) - 1)

        lines.append(start)
        visited_branch.add(start)
        children = self.graph.get(start, [])
        for i, child in enumerate(children):
            _walk(child, "", i == len(children) - 1)
        return "\n".join(lines)
