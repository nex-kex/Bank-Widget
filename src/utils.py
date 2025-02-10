import logging
import os

import pandas as pd

log_path = "../logs/utils.log"

# Устраняет ошибку отсутствия файла при импорте модуля
if str(os.path.dirname(os.path.abspath(__name__)))[-3:] != "src":
    log_path = log_path[1:]


logger = logging.getLogger("utils")
file_handler = logging.FileHandler(log_path, "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def read_from_xlsx(xlsx_file: str) -> list[dict]:
    """Читает XLSX-файл file_name с транзакциями и возвращает их в виде списка словарей."""
    try:
        data = pd.read_excel(xlsx_file)
        transactions = data.to_dict(orient="records")

    except Exception as e:
        logger.critical(f"Произошла ошибка при чтении XLSX-файла: {e}")

    return transactions
