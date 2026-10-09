"""
Модуль для работы с API crates.io.
Получение информации о зависимостях Rust-пакетов.
"""

import json
import urllib.request
import urllib.error


CRATES_API_URL = "https://crates.io/api/v1/crates"


def fetch_dependencies(package, version, repo_url=None):
    """
    Получить список прямых зависимостей пакета.

    :param package: имя пакета (например, 'serde')
    :param version: версия пакета (например, '1.0.0')
    :param repo_url: базовый URL репозитория (по умолчанию crates.io)
    :return: список словарей с информацией о зависимостях
    """
    base_url = repo_url.rstrip("/") if repo_url else CRATES_API_URL
    url = f"{base_url}/{package}/{version}/dependencies"

    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "config-management-tool/1.0"}
        )
        with urllib.request.urlopen(request, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
        return data.get("dependencies", [])
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise ValueError(
                f"Пакет '{package}' версии '{version}' не найден."
            )
        raise ValueError(f"Ошибка HTTP: {e.code} {e.reason}")
    except urllib.error.URLError as e:
        raise ValueError(f"Ошибка соединения: {e.reason}")
    except json.JSONDecodeError:
        raise ValueError("Не удалось разобрать ответ от сервера.")
