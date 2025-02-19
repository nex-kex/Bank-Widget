import pandas as pd

from src.events_page import get_expenses, get_incomes


def test_get_expenses_empty():
    assert get_expenses(pd.DataFrame([])) == {}


def test_get_expenses_3_categories():
    assert get_expenses(
        pd.DataFrame(
            [
                {
                    "Статус": "OK",
                    "Сумма операции": -21.0,
                    "Категория": "Супермаркеты",
                    "Сумма операции с округлением": 21.0,
                },
                {
                    "Статус": "OK",
                    "Сумма операции": 316.0,
                    "Категория": "Красота",
                    "Сумма операции с округлением": 316.0,
                },
                {
                    "Статус": "OK",
                    "Сумма операции": -3000.0,
                    "Категория": "Переводы",
                    "Сумма операции с округлением": 3000.0,
                },
            ]
        )
    ) == {
        "total_amount": 3021.0,
        "main": [
            {"category": "Переводы", "amount": 3000.0},
            {"category": "Супермаркеты", "amount": 21.0},
        ],
        "transfers_and_cash": [
            {"category": "Переводы", "amount": 3000.0},
            {"category": "Наличные", "amount": 0.0},
        ],
    }


def test_get_expenses(short_list_of_transactions):
    assert get_expenses(pd.DataFrame(short_list_of_transactions)) == {
        "total_amount": 7003.95,
        "main": [
            {"category": "Переводы", "amount": 3000.0},
            {"category": "Супермаркеты", "amount": 1509.99},
            {"category": "Топливо", "amount": 1025.0},
            {"category": "Различные товары", "amount": 1004.9},
            {"category": "Связь", "amount": 250.0},
            {"category": "Цветы", "amount": 120.0},
            {"category": "Магазины", "amount": 73.06},
            {"category": "Остальное", "amount": 21.0},
        ],
        "transfers_and_cash": [{"category": "Переводы", "amount": 3000.0}, {"category": "Наличные", "amount": 0}],
    }


def test_get_expenses_cash():
    assert get_expenses(
        pd.DataFrame(
            [
                {
                    "Статус": "OK",
                    "Сумма операции": -2100.0,
                    "Категория": "Наличные",
                    "Сумма операции с округлением": 2100.0,
                }
            ]
        )
    ) == {
        "total_amount": 2100,
        "main": [{"category": "Наличные", "amount": 2100}],
        "transfers_and_cash": [{"category": "Наличные", "amount": 2100.0}, {"category": "Переводы", "amount": 0}],
    }


def test_get_incomes_empty():
    assert get_incomes(pd.DataFrame([])) == {}


def test_get_incomes_3_categories():
    assert get_incomes(
        pd.DataFrame(
            [
                {
                    "Статус": "OK",
                    "Сумма операции": 21.0,
                    "Категория": "Супермаркеты",
                    "Сумма операции с округлением": 21.0,
                },
                {
                    "Статус": "OK",
                    "Сумма операции": 316.0,
                    "Категория": "Красота",
                    "Сумма операции с округлением": 316.0,
                },
                {
                    "Статус": "OK",
                    "Сумма операции": -3000.0,
                    "Категория": "Переводы",
                    "Сумма операции с округлением": 3000.0,
                },
            ]
        )
    ) == {
        "total_amount": 337.0,
        "main": [
            {"category": "Красота", "amount": 316.0},
            {"category": "Супермаркеты", "amount": 21},
        ],
    }
