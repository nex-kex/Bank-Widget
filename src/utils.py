import pandas as pd


def read_from_xlsx(xlsx_file: str) -> list[dict]:
    """Читает XLSX-файл file_name с транзакциями и возвращает из в виде списка словарей."""
    data = pd.read_excel(xlsx_file)
    transactions = data.to_dict(orient="records")
    return transactions
