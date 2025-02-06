import datetime
import json

from src.events import events_func
from src.main_page import main_page_func
from src.sorting import sort_by_period
from src.utils import read_from_xlsx
from src.views import create_report

# Валюта и акции пользователя из user_settings.json
with open("../user_settings.json", "r", encoding="utf-8") as s:
    user_information = json.load(s)
user_currencies = user_information["user_currencies"]
user_stocks = user_information["user_stocks"]

# Получение текущей даты
current_date = datetime.datetime.now()
str_date = datetime.datetime.strftime(current_date, "%Y-%m-%d %H:%M:%S")

# Получение списка транзакций за текущий (последний) месяц
operations_path = "../data/operations.xlsx"
transactions_list = read_from_xlsx(operations_path)

# --------------------------------------- Страница "Главная" ---------------------------------------
current_month_operations = sort_by_period(transactions_list, str_date)
main_page_data = main_page_func(str_date, current_month_operations, user_currencies, user_stocks)
create_report(main_page_data, "../output/main_page.json")

# --------------------------------------- Страница "События" ---------------------------------------
current_period_operations = sort_by_period(transactions_list, str_date)
data = events_func(current_period_operations, user_currencies, user_stocks)
create_report(data, "../output/events.json")
