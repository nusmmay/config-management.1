"""Тесты для CLI-приложения."""
import subprocess
import sys


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
    assert "version      = 1.0.0" in result.stdout
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
    assert "png" in result.stderr or "svg" in result.stderr
    print("OK: test_wrong_extension")


def test_package_not_found():
    result = run_cli([
        "-p", "this_package_does_not_exist_xyz",
        "-v", "0.0.1",
        "-r", "https://crates.io/api/v1/crates"
    ])
    assert result.returncode != 0
    print("OK: test_package_not_found")


if __name__ == "__main__":
    test_correct_run()
    test_missing_package()
    test_wrong_extension()
    test_package_not_found()
    print("")
    print("All tests passed!")
