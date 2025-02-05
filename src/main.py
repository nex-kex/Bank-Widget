from main_page import main_page_func
from utils import read_from_xlsx
from sorting import sort_by_month
import datetime
from views import create_report
import json


# Валюта и акции пользователя из user_settings.json
with open("../user_settings.json", "r", encoding="utf-8") as s:
    user_information = json.load(s)
user_currencies = user_information["user_currencies"]
user_stocks = user_information["user_stocks"]

# Получение текущей даты
current_date = datetime.datetime.now()
str_date = "2024-08-25 22:54:35" # datetime.datetime.strftime(current_date, "%Y-%m-%d %H:%M:%S")

# Получение списка транзакций
operations_path = "../data/operations.xlsx"
transactions_list = read_from_xlsx(operations_path)
current_month_operations = sort_by_month(transactions_list, str_date)

# Страница "Главная"
main_page_data = main_page_func(str_date, current_month_operations, user_currencies, user_stocks)
create_report(main_page_data, "../output/main_page.json")
