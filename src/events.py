from collections import defaultdict

from src.api_search import get_currency_rate, get_stock_exchange


def get_expenses(transactions_list: list[dict]) -> dict:
    """Возвращает словарь вида:

    - Общая сумма расходов.
    - Раздел "Основные", где траты по 7 основным категориям отсортированы по убыванию, остальные траты в "Остальном".
    - Раздел "Переводы и наличные", сумма по категориям отсортирована по убыванию."""

    category_expenses = defaultdict(int)
    total_expenses = 0

    for transaction in transactions_list:
        total_expenses += transaction["Сумма операции с округлением"]

        # Проверка на то, что это расход и он был успешно выполнен
        if transaction["Статус"] == "OK" and transaction["Сумма операции"] < 0:
            category_expenses[transaction["Категория"]] += transaction["Сумма операции с округлением"]

    # Сортировка названий категорий по убыванию суммы расходов в них
    sorted_categories = sorted(category_expenses, key=lambda x: category_expenses[x], reverse=True)

    answer = {
        "total_amount": round(total_expenses, 2),
        "main": [],
        "transfers_and_cash": [],
    }

    # Заполнение данных по 7 основным категориям
    for i in range(7):
        answer["main"].append(
            {
                "category": sorted_categories[i],
                "amount": round(category_expenses[sorted_categories[i]], 2),
            }
        )
    # Создание категории "Остальное" и добавление в неё остальных расходов
    answer["main"].append(
        {
            "category": "Остальное",
            "amount": 0,
        }
    )
    for i in range(7, len(sorted_categories)):
        answer["main"][7]["amount"] += category_expenses[sorted_categories[i]]
    answer["main"][7]["amount"] = round(answer["main"][7]["amount"], 2)

    # Добавление раздела "Наличные и переводы" по убыванию в них суммы расходов
    for category in sorted_categories:
        if category == "Наличные":
            answer["transfers_and_cash"].append(
                {
                    "category": "Наличные",
                    "amount": round(category_expenses["Наличные"], 2),
                }
            )
            answer["transfers_and_cash"].append(
                {
                    "category": "Переводы",
                    "amount": round(category_expenses["Переводы"], 2),
                }
            )
            break
        elif category == "Переводы":
            answer["transfers_and_cash"].append(
                {
                    "category": "Переводы",
                    "amount": round(category_expenses["Переводы"], 2),
                }
            )
            answer["transfers_and_cash"].append(
                {
                    "category": "Наличные",
                    "amount": round(category_expenses["Наличные"], 2),
                }
            )
            break

    return answer


def get_incomes(transactions_list: list[dict]) -> dict:
    """Возвращает словарь вида:

    - Общая сумма поступлений.
    - Раздел "Основные", где поступления по категориям отсортированы по убыванию."""

    category_incomes = defaultdict(int)
    total_incomes = 0

    for transaction in transactions_list:
        total_incomes += transaction["Сумма операции с округлением"]

        # Проверка на то, что это поступление и оно было успешно выполнен
        if transaction["Статус"] == "OK" and transaction["Сумма операции"] > 0:
            category_incomes[transaction["Категория"]] += transaction["Сумма операции с округлением"]

    # Сортировка названий категорий по убыванию суммы поступлений в них
    sorted_categories = sorted(category_incomes, key=lambda x: category_incomes[x], reverse=True)

    answer = {
        "total_amount": round(total_incomes, 2),
        "main": [],
    }
    # Заполнение данных по категориям
    for i in range(len(sorted_categories)):
        answer["main"].append(
            {
                "category": sorted_categories[i],
                "amount": round(category_incomes[sorted_categories[i]], 2),
            }
        )

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
