import re
import datetime


def sort_by_month(transactions_list: list[dict], date: str, status: str = "OK") -> list[dict]:
    """Из списка всех операций возвращает только операции за текущий месяц.
    Если таких нет, то возвращает операции за последний доступный месяц."""

    current_time = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    string_month = current_time.strftime("%m.%Y")

    current_month_transactions = []

    if any(str(x["Дата платежа"])[3:] == string_month for x in transactions_list):
        for transaction in transactions_list:
            if re.search(string_month, str(transaction["Дата платежа"])) and transaction["Статус"] == status:
                current_month_transactions.append(transaction)

    else:
        string_month = transactions_list[0]["Дата платежа"][2:]

    for transaction in transactions_list:
        if re.search(string_month, str(transaction["Дата платежа"])) and transaction["Статус"] == status:
            current_month_transactions.append(transaction)

    return current_month_transactions
