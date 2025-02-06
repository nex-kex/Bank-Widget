import datetime
import re


def sort_by_period(transactions_list: list[dict], date: str, status: str = "OK", period: str = "M") -> list[dict]:
    """Из списка всех операций возвращает только операции за текущий период
    (неделя, месяц, год или за всё время). По умолчанию - месяц.
    Если таких нет, то возвращает операции за последний доступный месяц."""

    current_period = datetime.datetime.strptime(date, "%d.%m.%Y %H:%M:%S").strftime("%m.%Y-%W")
    current_period_transactions = []
    string_period = ""  # period = "ALL"

    if period == "W":
        string_period = current_period[3:]  # "YYYY-WW"
    elif period == "M":
        string_period = current_period[:7]  # "mm.YYYY"
    elif period == "Y":
        string_period = current_period[3:7]  # "YYYY"

    if any(
        string_period in datetime.datetime.strptime(x["Дата операции"], "%d.%m.%Y %H:%M:%S").strftime("%m.%Y-%W")
        for x in transactions_list
    ):
        for transaction in transactions_list:
            transaction_date = datetime.datetime.strptime(
                str(transaction["Дата операции"]), "%d.%m.%Y %H:%M:%S"
            ).strftime("%m.%Y-%W")
            if re.search(string_period, transaction_date) and transaction["Статус"] == status:
                current_period_transactions.append(transaction)
    else:
        return sort_by_period(transactions_list, transactions_list[0]["Дата операции"], status=status, period=period)

    return current_period_transactions
