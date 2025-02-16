import pandas as pd
import pytest

from src.main_page import get_cards_numbers, get_top_transactions, greet_user


@pytest.mark.parametrize(
    "date, greeting",
    [
        ("2025-02-11 05:59:59", "Доброй ночи"),
        ("2025-02-11 06:00:00", "Доброе утро"),
        ("2025-02-11 12:30:00", "Добрый день"),
        ("2025-02-11 19:00:00", "Добрый вечер"),
    ],
)
def test_greet_user(date, greeting):
    assert greet_user(date) == greeting


def test_get_cards_numbers(short_list_of_transactions):
    assert get_cards_numbers(pd.DataFrame(short_list_of_transactions)) == [
        {"last_digits": "5441", "total_spent": 87068.0, "cashback": 870.68},
        {
            "last_digits": "7197",
            "total_spent": 6753.95,
            "cashback": 67.54,
        },
        {
            "last_digits": "4556",
            "total_spent": 250.0,
            "cashback": 2.5,
        },
    ]


def test_get_top_transactions_empty():
    assert get_top_transactions(pd.DataFrame([])) == []


def test_get_top_transactions(short_list_of_transactions):
    assert get_top_transactions(pd.DataFrame(short_list_of_transactions)) == [
        {"date": "10.01.2021", "amount": 87068.0, "category": "nan", "description": "Перевод с карты"},
        {"date": "01.07.2018", "amount": 3000.0, "category": "Переводы", "description": "Анастасия Л."},
        {"date": "04.11.2018", "amount": 1065.9, "category": "Супермаркеты", "description": "Пятёрочка"},
        {"date": "04.12.2018", "amount": 1025.0, "category": "Топливо", "description": "Pskov AZS 12 K2"},
        {"date": "08.02.2019", "amount": 1004.9, "category": "Различные товары", "description": "Torgovyy Dom* Mayak"},
    ]


def test_get_top_transactions_income():
    assert get_top_transactions(
        pd.DataFrame([
            {
                "Дата платежа": "01.08.2018",
                "Сумма операции": 316.0,
                "Категория": "Красота",
                "Описание": "OOO Balid",
                "Сумма операции с округлением": 316.0,
            },
            {
                "Дата платежа": "01.07.2018",
                "Сумма операции": -3000.0,
                "Категория": "Переводы",
                "Описание": "Анастасия Л.",
                "Сумма операции с округлением": 3000.0,
            },
        ])
    ) == [{"date": "01.07.2018", "amount": 3000.0, "category": "Переводы", "description": "Анастасия Л."}]
