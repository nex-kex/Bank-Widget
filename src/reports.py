import datetime
from collections import defaultdict

from dateutil.relativedelta import relativedelta


def spending_by_workday(transactions: list[dict], date: str = "") -> dict:
    """Функция выводит средние траты в рабочий и в выходной день за последние три месяца (от переданной даты).
    Если дата не передана, то берется текущая дата."""

    # Приводит дату к строке обычного формата
    if not date:
        current_date = datetime.datetime.now()
        date = current_date.strftime("%Y-%m-%d %H:%M:%S")

    dates = []

    # Добавляет 3 последних месяца в список в формате MM.YYYY
    for i in range(3):
        date_i = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S") + relativedelta(months=-i)
        date_i_str = date_i.strftime("%m.%Y")
        dates.append(date_i_str)

    workdays_transactions = []
    weekends_transactions = []

    # Сортировка расходов за последние 3 месяца по спискам (выходные и рабочие дни)
    for transaction in transactions:
        if any(date in transaction["Дата операции"] for date in dates):

            # Проверка на то, что это расход и он был успешно выполнен
            if transaction["Статус"] == "OK" and transaction["Сумма операции"] < 0:

                workday_str = datetime.datetime.strptime(transaction["Дата операции"], "%d.%m.%Y %H:%M:%S")
                workday = datetime.datetime.strftime(workday_str, "%w")

                if workday == "0" or workday == "6":  # 0 — воскресенье, 6 — суббота
                    weekends_transactions.append(transaction["Сумма операции с округлением"])

                else:
                    workdays_transactions.append(transaction["Сумма операции с округлением"])

    if len(workdays_transactions):
        avg_workday_spending = round(sum(workdays_transactions) / len(workdays_transactions), 2)
    else:
        avg_workday_spending = 0

    if len(weekends_transactions):
        avg_weekend_spending = round(sum(weekends_transactions) / len(weekends_transactions), 2)
    else:
        avg_weekend_spending = 0

    answer = {
        "avg_workday_spending": avg_workday_spending,
        "avg_weekend_spending": avg_weekend_spending,
    }

    return answer


def spending_by_weekday(transactions: list[dict], date: str = "") -> dict:
    """Функция возвращает средние траты в каждый из дней недели за последние три месяца (от переданной даты).
    Если дата не передана, то берется текущая дата."""

    # Приводит дату к строке обычного формата
    if not date:
        current_date = datetime.datetime.now()
        date = current_date.strftime("%Y-%m-%d %H:%M:%S")

    dates = []

    # Добавляет 3 последних месяца в список в формате MM.YYYY
    for i in range(3):
        date_i = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S") + relativedelta(months=-i)
        date_i_str = date_i.strftime("%m.%Y")
        dates.append(date_i_str)

    weekdays_spending = defaultdict(list)

    # Сортировка расходов за последние 3 месяца по спискам (выходные и рабочие дни)
    for transaction in transactions:
        if any(date in transaction["Дата операции"] for date in dates):

            # Проверка на то, что это расход и он был успешно выполнен
            if transaction["Статус"] == "OK" and transaction["Сумма операции"] < 0:

                workday_str = datetime.datetime.strptime(transaction["Дата операции"], "%d.%m.%Y %H:%M:%S")
                weekday = datetime.datetime.strftime(workday_str, "%A")

                weekdays_spending[weekday].append(transaction["Сумма операции с округлением"])

    for day, sums in weekdays_spending.items():
        if len(sums):
            weekdays_spending[day] = round(sum(sums) / len(sums), 2)

    return weekdays_spending


def spending_by_category(transactions: list[dict], category: str, date: str = "") -> dict:
    """Функция возвращает траты по заданной категории за последние три месяца (от переданной даты).
    Если дата не передана, то берется текущая дата."""

    # Приводит дату к строке обычного формата
    if not date:
        current_date = datetime.datetime.now()
        date = current_date.strftime("%Y-%m-%d %H:%M:%S")

    dates = []

    # Добавляет 3 последних месяца в список в формате MM.YYYY
    for i in range(3):
        date_i = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S") + relativedelta(months=-i)
        date_i_str = date_i.strftime("%m.%Y")
        dates.append(date_i_str)

    category_spending = 0.0

    # Сортировка расходов за последние 3 месяца по спискам (выходные и рабочие дни)
    for transaction in transactions:
        if any(date in transaction["Дата операции"] for date in dates):

            # Проверка на то, что это расход и он был успешно выполнен
            if transaction["Статус"] == "OK" and transaction["Сумма операции"] < 0:

                if transaction.get("Категория") and transaction["Категория"] == category:
                    category_spending += transaction["Сумма операции с округлением"]

    answer = {
        category: round(category_spending, 2),
    }

    return answer
