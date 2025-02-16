import datetime
import logging
import os
from collections import defaultdict
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


def get_cards_numbers(transactions_list: list[dict]) -> list[dict]:
    """По каждой карте находит последние 4 цифры, общую сумму расходов за текущий (последний) месяц и кешбэк."""

    cards: dict = defaultdict(int)

    for transaction in transactions_list:
        try:
            if transaction["Сумма операции"] < 0:
                cards[transaction["Номер карты"]] += transaction["Сумма операции с округлением"]
        except KeyError as e:
            logger.warning(f"Передана транзакция без необходимого ключа: {e}")
            continue

    result = []
    for key, value in cards.items():
        if str(key) != "nan":
            result.append(
                {
                    "last_digits": str(key)[1:],
                    "total_spent": round(value, 2),
                    "cashback": round(value / 100, 2),
                }
            )

    logger.info(f"Обнаружены данные по {len(result)} картам")
    return result


def get_top_transactions(transactions_list: list[dict]) -> list[dict]:
    """Находит информацию по 5 наибольшим транзакциям за текущий (последний) месяц."""

    sorted_transactions_list = sorted(transactions_list, key=lambda x: x["Сумма операции"])
    top_transactions = []

    for i in range(5):
        try:
            if sorted_transactions_list[i]["Сумма операции"] < 0:
                top_transactions.append(
                    {
                        "date": sorted_transactions_list[i]["Дата платежа"],
                        "amount": sorted_transactions_list[i]["Сумма операции с округлением"],
                        "category": sorted_transactions_list[i]["Категория"],
                        "description": sorted_transactions_list[i]["Описание"],
                    }
                )
            else:
                # Если пополнения входят в топ 5, то платежей меньше 5
                logger.info(f"За текущий период обнаружено только {i} транз. с расходами")
                return top_transactions

        except IndexError:
            logger.warning("За текущий период передано менее 5 транзакций")
            continue

        except KeyError as e:
            logger.warning(f"Передана транзакция без необходимого ключа: {e}")
            continue

    logger.info("Успешно обнаружены топ 5 транз.")
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
