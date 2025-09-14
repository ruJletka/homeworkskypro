import csv
from typing import Any

import pandas as pd


def read_transaction_csv(file_path: str) -> Any:
    """Функция для считывания финансовых операций из CSV"""
    with open(file_path, encoding="utf-8") as file:
        reader = csv.DictReader(file, delimiter=";")
        dictionary_list = []
        for row in reader:
            dictionary_list.append(row)
        return dictionary_list


def read_transaction_excel(file_path: str) -> list[dict[str, str]]:
    """Функция считывает финансовые операции из Excel и выдает список словарей с транзакциями."""
    df = pd.read_excel(file_path)
    dictionary_list_excel = df.to_dict(orient='records')

    return dictionary_list_excel
