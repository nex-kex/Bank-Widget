import logging
import os

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

    try:
        # Проверка на то, что это расход и он был успешно выполнен
        sorted_transactions_list = transactions.loc[
            (transactions["Статус"] == "OK") & (transactions["Сумма операции"] < 0)
        ]

        total_expenses = float(sorted_transactions_list["Сумма операции с округлением"].agg("sum"))

        answer_main = []
        answer_transfers_and_cash = []

        category_expenses = (
            sorted_transactions_list.groupby("Категория")["Сумма операции с округлением"]
            .agg("sum")
            .sort_values(ascending=False)
        )

        index = 0
        for category, amount in category_expenses.items():
            if index < 7:
                answer_main.append(
                    {
                        "category": category,
                        "amount": round(amount, 2),
                    }
                )
                index += 1

            else:
                answer_main.append(
                    {
                        "category": "Остальное",
                        "amount": float(round(category_expenses.iloc[7:].agg("sum"), 2)),
                    }
                )
                break

        # Добавление раздела "Наличные и переводы" по убыванию в них суммы расходов

        answer_transfers_and_cash.append(
            {
                "category": "Наличные",
                "amount": float(
                    round(
                        sorted_transactions_list.loc[sorted_transactions_list["Категория"] == "Наличные"][
                            "Сумма операции с округлением"
                        ].agg("sum"),
                        2,
                    )
                ),
            }
        )
        answer_transfers_and_cash.append(
            {
                "category": "Переводы",
                "amount": float(
                    round(
                        sorted_transactions_list.loc[sorted_transactions_list["Категория"] == "Переводы"][
                            "Сумма операции с округлением"
                        ].agg("sum"),
                        2,
                    )
                ),
            }
        )

        answer = {
            "total_amount": round(total_expenses, 2),
            "main": answer_main,
            "transfers_and_cash": answer_transfers_and_cash,
        }

        # Сортировка категорий по убыванию суммы расходов в них
        answer["transfers_and_cash"] = sorted(answer["transfers_and_cash"], key=lambda x: x["amount"], reverse=True)
        logger.info("Получены переводы и траты наличными")

        return answer

    except KeyError as e:
        logger.warning(f"Передана транзакция без необходимого ключа: {e}")

    except Exception as e:
        logger.warning(f"Произошла ошибка: {e}")

    return {}


def get_incomes(transactions: pd.DataFrame) -> dict:
    """Возвращает словарь вида:

    - Общая сумма поступлений.
    - Раздел "Основные", где поступления по категориям отсортированы по убыванию."""

    try:
        # Проверка на то, что это поступление и оно было успешно выполнено
        sorted_transactions_list = transactions.loc[
            (transactions["Статус"] == "OK") & (transactions["Сумма операции"] > 0)
        ]

        total_incomes = float(sorted_transactions_list["Сумма операции с округлением"].agg("sum"))

        answer_main = []

        # Сортировка категорий по убыванию суммы поступлений в них
        category_incomes = (
            sorted_transactions_list.groupby("Категория")["Сумма операции с округлением"]
            .agg("sum")
            .sort_values(ascending=False)
        )
        logger.info(f"Получено {len(category_incomes)} категор. поступлений")

        for category, amount in category_incomes.items():
            answer_main.append(
                {
                    "category": category,
                    "amount": round(amount, 2),
                }
            )

        answer = {
            "total_amount": round(total_incomes, 2),
            "main": answer_main,
        }

        return answer

    except KeyError as e:
        logger.warning(f"Передана транзакция без необходимого ключа: {e}")

    except Exception as e:
        logger.warning(f"Произошла ошибка: {e}")

    return {}


def events_func(
    transactions_list: pd.DataFrame, currencies: list[str], stocks: list[str], usd_rate: float = 1
) -> dict:
    """Основная функция страницы "События"."""
    result = {
        "expenses": get_expenses(transactions_list),
        "income": get_incomes(transactions_list),
        "currency_rates": get_currency_rate(currencies),
        "stock_prices": get_stock_exchange(stocks, usd_rate),
    }

    return result
