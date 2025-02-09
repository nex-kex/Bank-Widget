import datetime
import json
import os

from dotenv import load_dotenv

from src.events import events_func
from src.main_page import main_page_func
from src.reports import spending_by_category, spending_by_weekday, spending_by_workday
from src.search import individual_transfer_search, phone_number_search, simple_search
from src.services import services_cashback, services_investments
from src.sorting import sort_by_period
from src.utils import read_from_xlsx
from src.views import create_report

load_dotenv()
OPERATIONS = os.getenv("OPERATIONS")


# Валюта и акции пользователя из user_settings.json
with open("../user_settings.json", "r", encoding="utf-8") as s:
    user_information = json.load(s)
user_currencies = user_information["user_currencies"]
user_stocks = user_information["user_stocks"]

# Получение текущей даты
current_date = datetime.datetime.now()
str_date = datetime.datetime.strftime(current_date, "%Y-%m-%d %H:%M:%S")

# Получение списка транзакций
operations_path = f"../data/{OPERATIONS}.xlsx"
transactions_list = read_from_xlsx(operations_path)


# ------------------------------------------ ВЕБ-СТРАНИЦЫ ------------------------------------------


# --------------------------------------- Страница "Главная" ---------------------------------------
current_month_operations = sort_by_period(transactions_list, str_date)
main_page_data = main_page_func(str_date, current_month_operations, user_currencies, user_stocks)
create_report(main_page_data, "../output/main_page.json")

# --------------------------------------- Страница "События" ---------------------------------------
current_period_operations = sort_by_period(transactions_list, str_date)
data = events_func(current_period_operations, user_currencies, user_stocks)
create_report(data, "../output/events.json")


# -------------------------------------------- СЕРВИСЫ --------------------------------------------


# ----------------------------- Выгодные категории повышенного кешбэка -----------------------------
# Получение даты в нужном формате
current_date = datetime.datetime.now()
str_month = datetime.datetime.strftime(current_date, "%m")
str_year = datetime.datetime.strftime(current_date, "%Y")

cashback_by_category = services_cashback(transactions_list, str_year, str_month)
create_report(cashback_by_category, "../output/cashback_by_category.json")

# ----------------------------------------- Инвесткопилка -----------------------------------------
# Получение даты в нужном формате
current_date = datetime.datetime.now()
str_year_month = datetime.datetime.strftime(current_date, "%Y-%m")

investments = services_investments(str_year_month, transactions_list, 50)
create_report({str_year_month: investments}, "../output/investments.json")

# ----------------------------------------- Простой поиск -----------------------------------------
search_line = "*"
results = simple_search(transactions_list, search_line)
create_report(results, "../output/simple_search.json")

# ---------------------------------- Поиск по телефонным номерам ----------------------------------
results = phone_number_search(transactions_list)
create_report(results, "../output/phone_number_search.json")

# -------------------------------- Поиск переводов физическим лицам --------------------------------
results = individual_transfer_search(transactions_list)
create_report(results, "../output/individual_transfer_search.json")


# --------------------------------------------- ОТЧЁТЫ ---------------------------------------------


# -------------------------------- Траты в рабочий / выходной день --------------------------------
# Дата, для которой существуют данные в таблице
date = "2021-01-09 15:34:23"

spending_by_workday(transactions_list, date)

# -------------------------------------- Траты по дням недели --------------------------------------
spending_by_weekday(transactions_list, date)

# --------------------------------------- Траты по категории ---------------------------------------
spending_by_category(transactions_list, "Супермаркеты", date)
