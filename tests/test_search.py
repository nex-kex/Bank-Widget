from src.search import individual_transfer_search, phone_number_search, simple_search


def test_simple_search_empty():
    assert simple_search([], "") == []


def test_simple_search(short_list_of_transactions):
    assert simple_search(short_list_of_transactions, "анастасия") == [
        {
            "Дата операции": "01.07.2018 12:49:53",
            "Дата платежа": "01.07.2018",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -3000.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -3000.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": 20,
            "Категория": "Переводы",
            "MCC": "nan",
            "Описание": "Анастасия Л.",
            "Бонусы (включая кэшбэк)": 0,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 3000.0,
        }
    ]


def test_simple_search_no_category():
    assert simple_search([{"Описание": "Анастасия Л."}], "анастасия") == [{"Описание": "Анастасия Л."}]


def test_phone_number_search_empty():
    assert phone_number_search([]) == []


def test_phone_number_search(short_list_of_transactions):
    assert phone_number_search(short_list_of_transactions) == [
        {
            "Дата операции": "05.12.2018 14:58:38",
            "Дата платежа": "05.12.2018",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -120.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -120.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": 777,
            "Категория": "Цветы",
            "MCC": 5992.0,
            "Описание": "Пополнение на +7 777 777-77-77",
            "Бонусы (включая кэшбэк)": 2,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 120.0,
        }
    ]


def test_individual_transfer_search_empty():
    assert individual_transfer_search([]) == []


def test_individual_transfer_search(short_list_of_transactions):
    assert individual_transfer_search(short_list_of_transactions) == [
        {
            "Дата операции": "01.07.2018 12:49:53",
            "Дата платежа": "01.07.2018",
            "Номер карты": "*7197",
            "Статус": "OK",
            "Сумма операции": -3000.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -3000.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": 20,
            "Категория": "Переводы",
            "MCC": "nan",
            "Описание": "Анастасия Л.",
            "Бонусы (включая кэшбэк)": 0,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 3000.0,
        }
    ]
