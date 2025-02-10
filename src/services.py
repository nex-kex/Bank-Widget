import logging
import os
from collections import defaultdict

from src.sorting import sort_by_period

log_path = "../logs/services.log"

# Устраняет ошибку отсутствия файла при импорте модуля
if str(os.path.dirname(os.path.abspath(__name__)))[-3:] != "src":
    log_path = log_path[1:]


logger = logging.getLogger("services")
file_handler = logging.FileHandler(log_path, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def get_category_cashback(transactions_list: list[dict]) -> dict:
    """Принимает список транзакций, возвращает кешбэк по категориям."""
    category_cashback: dict = defaultdict(int)

    for transaction in transactions_list:
        if transaction.get("Категория") and str(transaction["Категория"]) != "nan":
            if transaction.get("Кешбэк") and str(transaction["Кэшбэк"]) != "nan":
                category_cashback[transaction["Категория"]] += transaction["Кэшбэк"]

    if len(category_cashback) == 0:
        logger.warning("За текущий период не получено кешбэка по найденным категориям.")

    # Сортировка названий категорий по убыванию суммы кешбэка в них
    sorted_categories = sorted(category_cashback, key=lambda x: category_cashback[x], reverse=True)

    sorted_cashback = {}

    for category in sorted_categories:
        sorted_cashback[category] = round(category_cashback[category], 2)

    return sorted_cashback


def count_investments(transactions_list: list[dict], limit: int) -> float:
    """Функция возвращает сумму, которую удалось бы отложить в «Инвесткопилку»."""

    investments = 0.0

    try:
        for transaction in transactions_list:
            # Проверка на то, что это расход и он был успешно выполнен
            if transaction["Статус"] == "OK" and transaction["Сумма операции"] < 0:
                investments += transaction["Сумма операции"] % limit

    except KeyError as e:
        logger.critical(f"Получена транзакция без необходимого ключа: {e}")

    return investments


def services_cashback(data: list[dict], year: str, month: str) -> dict:
    """Принимает список транзакций и месяц, возвращает кешбэк по категориям за этот месяц."""
    date = f"{year}-{month}-01 00:00:00"
    transactions_list = sort_by_period(data, date)
    return get_category_cashback(transactions_list)


def services_investments(month: str, transactions: list[dict], limit: int) -> float:
    """Функция возвращает сумму, которую удалось бы отложить в «Инвесткопилку» за этот месяц."""
    date = f"{month}-01 00:00:00"
    transactions_list = sort_by_period(transactions, date)
    return count_investments(transactions_list, limit)
