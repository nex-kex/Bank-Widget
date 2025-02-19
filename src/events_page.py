import logging
import os
from collections import defaultdict

import pandas as pd

from src.api_search import get_currency_rate, get_stock_exchange

log_path = "../logs/events.log"

# Устраняет ошибку отсутствия файла при импорте модуля
if str(os.path.dirname(os.path.abspath(__name__)))[-3:] != "src":
    log_path = log_path[1:]


logger = logging.getLogger("events")
file_handler = logging.FileHandler(log_path, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def get_expenses(transactions: pd.DataFrame) -> dict:
    """Возвращает словарь вида:

    - Общая сумма расходов.
    - Раздел "Основные", где траты по 7 основным категориям отсортированы по убыванию, остальные траты в "Остальном".
    - Раздел "Переводы и наличные", где сумма по категориям отсортирована по убыванию."""

    transactions_list = transactions.to_dict(orient="records")

    category_expenses: dict = defaultdict(int)
    total_expenses = 0

    for transaction in transactions_list:
        try:
            # Проверка на то, что это расход и он был успешно выполнен
            if transaction["Статус"] == "OK" and transaction["Сумма операции"] < 0:
                total_expenses += transaction["Сумма операции с округлением"]
                category_expenses[transaction["Категория"]] += transaction["Сумма операции с округлением"]

        except KeyError as e:
            logger.warning(f"Передана транзакция без необходимого ключа: {e}")
            continue

    # Сортировка названий категорий по убыванию суммы расходов в них
    sorted_categories = sorted(category_expenses, key=lambda x: category_expenses[x], reverse=True)

    answer = {
        "total_amount": round(total_expenses, 2),
        "main": [],
        "transfers_and_cash": [],
    }
    answer_main = []
    answer_transfers_and_cash = []

    # Заполнение данных по 7 основным категориям
    for i in range(7):
        try:
            answer_main.append(
                {
                    "category": sorted_categories[i],
                    "amount": round(category_expenses[sorted_categories[i]], 2),
                }
            )
        except IndexError:
            logger.warning("За текущий период получено меньше 7 категорий расходов")
            continue
    # Создание категории "Остальное" и добавление в неё остальных расходов
    answer_main.append(
        {
            "category": "Остальное",
            "amount": 0,
        }
    )

    for i in range(7, len(sorted_categories)):
        answer_main[7]["amount"] += category_expenses[sorted_categories[i]]
    answer_main[-1]["amount"] = round(answer_main[-1]["amount"], 2)

    answer["main"] = answer_main

    # Добавление раздела "Наличные и переводы" по убыванию в них суммы расходов
    for category in sorted_categories:
        if category == "Наличные":
            answer_transfers_and_cash.append(
                {
                    "category": "Наличные",
                    "amount": round(category_expenses["Наличные"], 2),
                }
            )
            answer_transfers_and_cash.append(
                {
                    "category": "Переводы",
                    "amount": round(category_expenses["Переводы"], 2),
                }
            )
            break
        elif category == "Переводы":
            answer_transfers_and_cash.append(
                {
                    "category": "Переводы",
                    "amount": round(category_expenses["Переводы"], 2),
                }
            )
            answer_transfers_and_cash.append(
                {
                    "category": "Наличные",
                    "amount": round(category_expenses["Наличные"], 2),
                }
            )
            break

    if len(answer_transfers_and_cash) == 0:
        logger.info("За текущий период не было переводов и трат наличными")

    else:
        logger.info("Успешно получены переводы и траты наличными")
        answer["transfers_and_cash"] = answer_transfers_and_cash

    return answer


def get_incomes(transactions: pd.DataFrame) -> dict:
    """Возвращает словарь вида:

    - Общая сумма поступлений.
    - Раздел "Основные", где поступления по категориям отсортированы по убыванию."""

    transactions_list = transactions.to_dict(orient="records")

    category_incomes: dict = defaultdict(int)
    total_incomes = 0

    for transaction in transactions_list:
        try:

            # Проверка на то, что это поступление и оно было успешно выполнен
            if transaction["Статус"] == "OK" and transaction["Сумма операции"] > 0:
                total_incomes += transaction["Сумма операции с округлением"]
                category_incomes[transaction["Категория"]] += transaction["Сумма операции с округлением"]

        except KeyError as e:
            logger.warning(f"Передана транзакция без необходимого ключа: {e}")
            continue

    # Сортировка названий категорий по убыванию суммы поступлений в них
    sorted_categories = sorted(category_incomes, key=lambda x: category_incomes[x], reverse=True)

    logger.info(f"Получено {len(sorted_categories)} категор. поступлений")

    answer = {
        "total_amount": round(total_incomes, 2),
        "main": [],
    }
    answer_main = []

    # Заполнение данных по категориям
    for i in range(len(sorted_categories)):
        answer_main.append(
            {
                "category": sorted_categories[i],
                "amount": round(category_incomes[sorted_categories[i]], 2),
            }
        )

    answer["main"] = answer_main

    return answer


def events_func(transactions_list: list[dict], currencies: list[str], stocks: list[str], usd_rate: float = 1) -> dict:
    """Основная функция страницы "События"."""
    result = {
        "expenses": get_expenses(transactions_list),
        "income": get_incomes(transactions_list),
        "currency_rates": get_currency_rate(currencies),
        "stock_prices": get_stock_exchange(stocks, usd_rate),
    }

    return result
