"""Тесты для CLI-приложения."""
import os
import subprocess
import sys


FIXTURES = "tests/fixtures"


def run_cli(args):
    result = subprocess.run(
        [sys.executable, "src/main.py"] + args,
        capture_output=True,
        text=True,
        cwd="."
    )
    return result


def test_correct_run():
    result = run_cli([
        "-p", "serde", "-v", "1.0.0",
        "-r", "https://crates.io/api/v1/crates"
    ])
    assert result.returncode == 0
    assert "package      = serde" in result.stdout
    print("OK: test_correct_run")


def test_missing_package():
    result = run_cli([
        "-v", "1.0.0",
        "-r", "https://crates.io/api/v1/crates"
    ])
    assert result.returncode != 0
    print("OK: test_missing_package")


def test_wrong_extension():
    result = run_cli([
        "-p", "serde", "-v", "1.0.0",
        "-r", "https://crates.io/api/v1/crates",
        "-o", "graph.txt"
    ])
    assert result.returncode != 0
    print("OK: test_wrong_extension")


def test_simple_graph():
    path = os.path.join(FIXTURES, "simple.json")
    result = run_cli(["-p", "A", "-v", "1.0.0", "-r", path, "-t"])
    assert result.returncode == 0
    assert "Всего пакетов: 5" in result.stdout
    print("OK: test_simple_graph")


def test_cyclic_graph():
    path = os.path.join(FIXTURES, "cyclic.json")
    result = run_cli(["-p", "A", "-v", "1.0.0", "-r", path, "-t"])
    assert result.returncode == 0
    assert "Всего пакетов: 5" in result.stdout
    print("OK: test_cyclic_graph")


def test_filter():
    path = os.path.join(FIXTURES, "filter.json")
    result = run_cli([
        "-p", "A", "-v", "1.0.0", "-r", path, "-t", "-f", "skip"
    ])
    assert result.returncode == 0
    assert "Всего пакетов: 4" in result.stdout
    print("OK: test_filter")


def test_max_depth():
    path = os.path.join(FIXTURES, "simple.json")
    result = run_cli([
        "-p", "A", "-v", "1.0.0", "-r", path, "-t", "-d", "1"
    ])
    assert result.returncode == 0
    assert "Всего пакетов: 3" in result.stdout
    print("OK: test_max_depth")


if __name__ == "__main__":
    test_correct_run()
    test_missing_package()
    test_wrong_extension()
    test_simple_graph()
    test_cyclic_graph()
    test_filter()
    test_max_depth()
    print("")
    print("All tests passed!")
