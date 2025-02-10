import json
import logging
import os
from functools import wraps
from typing import Any, Callable

log_path = "../logs/views.log"

# Устраняет ошибку отсутствия файла при импорте модуля
if str(os.path.dirname(os.path.abspath(__name__)))[-3:] != "src":
    log_path = log_path[1:]


logger = logging.getLogger("views")
file_handler = logging.FileHandler(log_path, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def create_report(data: dict | list[dict], file_path: str) -> None:
    """Записывает информацию в JSON-файл."""
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        logger.critical(f"Произошла ошибка при записи в файл: {e}")


def save_report(filename: str = "") -> Callable:
    """Декоратор для функций-отчётов, который записывает в файл результат, возвращаемый функциям,
    формирующими отчёты."""

    def my_decorator(func: Callable) -> Callable:

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:

            # Проверка на наличие ошибок
            try:
                func(*args, **kwargs)
            except Exception as e:
                logger.critical(f"Произошла ошибка при выполнении функции {func.__name__}: {e}")

            result = func(*args, **kwargs)

            # Запись в файл
            if filename == "":
                logger.info("Название файла не задано, запись в стандартный файл")
                create_report(result, "../output/report_result.json")
            else:
                create_report(result, filename)

            return func(*args, **kwargs)

        return wrapper

    return my_decorator
