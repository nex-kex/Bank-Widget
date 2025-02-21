import pandas as pd

from src.reports import spending_by_category


def test_spending_by_category_empty():
    assert spending_by_category(pd.DataFrame([]), "category").to_dict(orient="records") == []


def test_spending_by_category(short_list_of_transactions):
    assert spending_by_category(
        pd.DataFrame(short_list_of_transactions), "различные товары", "2019-02-08 12:41:24"
    ).to_dict(orient="records") == [{"Различные товары": 1004.9}]


# def test_spending_by_workday_empty():
#     assert spending_by_workday([]) == {"avg_weekend_spending": 0, "avg_workday_spending": 0}
#     assert spending_by_workday([], "2025-02-11 00:00:00") == {"avg_weekend_spending": 0, "avg_workday_spending": 0}
#
#
# def test_spending_by_workday(short_list_of_transactions):
#     assert spending_by_workday(short_list_of_transactions, "2018-09-10 12:41:24") == {
#         "avg_weekend_spending": 3000,
#         "avg_workday_spending": 21,
#     }
#
#
# def test_spending_by_weekday_empty():
#     assert spending_by_weekday([]) == {}
#
#
# def test_spending_by_weekday(short_list_of_transactions):
#     assert spending_by_weekday(short_list_of_transactions, "2018-09-10 12:41:24") == {"Monday": 21, "Sunday": 3000}
