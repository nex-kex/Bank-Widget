from src.services import count_investments, get_category_cashback


def test_get_category_cashback_empty():
    assert get_category_cashback([]) == {}


def test_get_category_cashback(short_list_of_transactions):
    assert get_category_cashback(short_list_of_transactions) == {
        "Цветы": 777,
        "Супермаркеты": 30,
        "Переводы": 20,
    }


def test_count_investments_empty():
    assert count_investments([], 100) == 0


def test_count_investments(short_list_of_transactions):
    assert count_investments(short_list_of_transactions, 10) == 36.05
