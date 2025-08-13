from typing import Iterator


def filter_by_currency(transactions: list, currency: str) -> Iterator[str]:
    """Функция принимает на вход список словарей, представляющих транзакции.
    Функция должна возвращать итератор, который поочередно выдает транзакции,
    где валюта операции соответствует заданной"""

    for transaction in transactions:
        if transaction["operationAmount"]["currency"]["code"] == currency:
            yield transaction


def transaction_descriptions(transactions: list) -> Iterator[str]:
    """Функция принимает список словарей с транзакциями
     и возвращает описание каждой операции по очереди."""

    for transaction in transactions:
        yield transaction.get("description")