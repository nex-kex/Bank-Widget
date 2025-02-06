import os

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")


def get_currency_rate(currencies: list[str]) -> list[dict]:
    """Возвращает курс валют в рублях."""
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    response = requests.get(url).json()
    answer = []
    for currency in currencies:
        answer.append({"currency": currency, "rate": response["Valute"][currency]["Value"]})
    return answer


def get_stock_exchange(stocks: list[str], usd_rate: float = 1) -> list[dict]:
    """Возвращает стоимость акций в долларах. Чтобы вернуть стоимость в другой валюте,
    необходимо присвоить курс доллара необязательному параметру usd_rate."""
    stocks_str = ",".join(stocks)
    url = f"http://api.marketstack.com/v2/eod?access_key={API_KEY}&symbols={stocks_str}"

    response = requests.get(url).json()
    answer = []

    for i in range(len(stocks)):
        answer.append(
            {
                "stock": response["data"][i]["symbol"],
                "price": round(response["data"][i]["open"] * usd_rate, 2),
            }
        )

    return answer
