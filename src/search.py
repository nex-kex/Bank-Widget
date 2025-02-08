import re


def simple_search(transactions_list: list[dict], search_info: str) -> list[dict]:
    """Функция принимает список словарей с данными о транзакциях и строку поиска,
    а возвращает список тех транзакций, в описании или категории которых есть строка поиска."""

    filtered_transactions = []

    for transaction in transactions_list:

        # Определяет, где искать
        if transaction.get("Категория"):
            search_in = str(transaction["Категория"]) + transaction["Описание"]
        else:
            search_in = transaction["Описание"]

        if search_info.lower() in search_in.lower():
            filtered_transactions.append(transaction)

    return filtered_transactions


def phone_number_search(transactions_list: list[dict]) -> list[dict]:
    """Функция принимает список словарей с данными о транзакциях и возвращает список тех транзакций,
    в описании которых есть телефонные номера."""

    filtered_transactions = []

    for transaction in transactions_list:
        if re.search(r"\+\d \d{3} \d{3}-\d{2}-\d{2}", transaction["Описание"]):
            filtered_transactions.append(transaction)

    return filtered_transactions


def individual_transfer_search(transactions_list: list[dict]) -> list[dict]:
    """Функция принимает список словарей с данными о транзакциях и возвращает список тех транзакций,
    которые относятся к переводам физическим лицам."""

    filtered_transactions = []

    for transaction in transactions_list:

        if transaction.get("Категория") and transaction["Категория"] == "Переводы":
            if re.search(r"^\w+ \w\.$", transaction["Описание"]):
                filtered_transactions.append(transaction)

    return filtered_transactions
