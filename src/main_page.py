import datetime
import logging
import os

import pandas as pd

from src.api_search import get_currency_rate, get_stock_exchange

log_path = "../logs/main_page.log"

# Устраняет ошибку отсутствия файла при импорте модуля
if str(os.path.dirname(os.path.abspath(__name__)))[-3:] != "src":
    log_path = log_path[1:]

logger = logging.getLogger("main_page")
file_handler = logging.FileHandler(log_path, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def greet_user(date: str) -> str:
    """Приветствует пользователя в зависимости от текущего времени суток.
    00:00-05:59: ночь
    06:00-11:59: утро
    12:00-17:59: день
    18:00-23:59: вечер"""

    date_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    current_time = date_obj.replace(year=1, month=1, day=1)

    logger.info(f"Программа приветствует пользователя в {date_obj}")

    if current_time >= datetime.datetime(1, 1, 1, 18, 0, 0):
        return "Добрый вечер"
    elif current_time >= datetime.datetime(1, 1, 1, 12, 0, 0):
        return "Добрый день"
    elif current_time >= datetime.datetime(1, 1, 1, 6, 0, 0):
        return "Доброе утро"
    else:
        return "Доброй ночи"


def get_cards_numbers(transactions_list: pd.DataFrame) -> dict:
    """По каждой карте находит последние 4 цифры, общую сумму расходов за текущий (последний) месяц и кешбэк."""

    total_spending = {}

    try:
        transactions_list_sorted = transactions_list.loc[
            (transactions_list["Сумма операции"] < 0) & ((transactions_list["Номер карты"]) != "nan")
        ]
        cards = transactions_list_sorted.groupby("Номер карты")["Сумма операции с округлением"].agg("sum")

        cards_dict = cards.to_dict()

        for number, spending in cards_dict.items():
            total_spending[str(number)[1:]] = round(spending, 2)

        logger.info(f"Обнаружены данные по {len(total_spending)} картам")

    except Exception as e:
        logger.warning(f"Произошла ошибка: {e}")

    return total_spending


def get_top_transactions(transactions: pd.DataFrame) -> list[dict]:
    """Находит информацию по 5 наибольшим транзакциям за текущий (последний) месяц."""

    sorted_transactions_list = transactions.loc[
        (transactions["Статус"] == "OK") & (transactions["Сумма операции"] < 0)
    ].sort_values("Сумма операции с округлением", ascending=False, ignore_index=True)
    top_transactions = []

    try:
        for index, transaction in sorted_transactions_list.iterrows():
            if int(index) < 5:
                top_transactions.append(
                    {
                        "date": transaction["Дата платежа"],
                        "amount": transaction["Сумма операции с округлением"],
                        "category": transaction["Категория"],
                        "description": transaction["Описание"],
                    }
                )
            else:
                break

    except Exception as e:
        logger.warning(f"Произошла ошибка: {e}")

    logger.info(f"Обнаружены топ {len(top_transactions)} транз.")
    return top_transactions


def main_page_func(
    date: str, transactions_list: list[dict], currencies: list[str], stocks: list[str], usd_rate: float = 1
) -> dict:
    """Основная функция страницы "Главная"."""

    result = {
        "greeting": greet_user(date),
        "cards": get_cards_numbers(transactions_list),
        "top_transactions": get_top_transactions(transactions_list),
        "currency_rates": get_currency_rate(currencies),
        "stock_prices": get_stock_exchange(stocks, usd_rate),
    }

    return result
