"""Тесты для CLI-приложения."""
import subprocess
import sys


def run_cli(args):
    result = subprocess.run(
        [sys.executable, "src/main.py"] + args,
        capture_output=True,
        text=True
    )
    return result


def test_correct_run():
    result = run_cli(["-p", "serde", "-r", "https://crates.io"])
    assert result.returncode == 0
    assert "package      = serde" in result.stdout
    print("OK: test_correct_run")


def test_missing_package():
    result = run_cli(["-r", "https://crates.io"])
    assert result.returncode != 0
    print("OK: test_missing_package")


def test_wrong_extension():
    result = run_cli(["-p", "serde", "-r", "https://crates.io", "-o", "graph.txt"])
    assert result.returncode != 0
    assert "png" in result.stderr or "svg" in result.stderr
    print("OK: test_wrong_extension")


if __name__ == "__main__":
    test_correct_run()
    test_missing_package()
    test_wrong_extension()
    print("")
    print("All tests passed!")
