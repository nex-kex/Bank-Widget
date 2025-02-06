import json


def create_report(data: dict | list[dict], file_path: str) -> None:
    """Записывает информацию в JSON-файл."""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
