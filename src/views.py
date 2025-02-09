import json
from functools import wraps
from typing import Any, Callable


def create_report(data: dict | list[dict], file_path: str) -> None:
    """Записывает информацию в JSON-файл."""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def save_report(filename: str = "") -> Callable:
    """Декоратор для функций-отчётов, который записывает в файл результат, возвращаемый функциям,
    формирующими отчёты."""

    def my_decorator(func: Callable) -> Callable:

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:

            # Проверка на наличие ошибок
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                result = f"{func.__name__} executed with an error: {e}. "

            # Запись в файл
            if filename == "":
                create_report(result, "../output/report_result.json")
            else:
                create_report(result, filename)

            return func(*args, **kwargs)

        return wrapper

    return my_decorator
