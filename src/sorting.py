import datetime
import logging
import os
import re

log_path = "../logs/sorting.log"

# Устраняет ошибку отсутствия файла при импорте модуля
if str(os.path.dirname(os.path.abspath(__name__)))[-3:] != "src":
    log_path = log_path[1:]


logger = logging.getLogger("sorting")
file_handler = logging.FileHandler(log_path, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def sort_by_period(transactions_list: list[dict], date: str, status: str = "OK", period: str = "M") -> list[dict]:
    """Из списка всех операций возвращает только операции за текущий период
    (неделя, месяц, год или за всё время). По умолчанию - месяц.
    Если таких нет, то возвращает операции за последний доступный месяц."""

    current_period = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S").strftime("%m.%Y-%W")
    current_period_transactions = []
    string_period = ""  # period = "ALL"

    if period == "W":
        string_period = current_period[3:]  # "YYYY-WW"
    elif period == "M":
        string_period = current_period[:7]  # "mm.YYYY"
    elif period == "Y":
        string_period = current_period[3:7]  # "YYYY"

    if len(transactions_list) != 0:

        try:
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
                last_date = datetime.datetime.strptime(
                    transactions_list[0]["Дата операции"], "%d.%m.%Y %H:%M:%S"
                ).strftime("%Y-%m-%d %H:%M:%S")

                logger.info(f"Не найдено транзакций для {date}. Поиск транзакций для {last_date}")

                return sort_by_period(transactions_list, last_date, status=status, period=period)

        except KeyError as e:
            logger.critical(f"Передана транзакция без необходимого ключа: {e}")

    logger.info(f"Найдено {len(current_period_transactions)} транзакций за переданный период")

    return current_period_transactions
