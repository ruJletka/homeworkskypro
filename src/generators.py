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


def card_number_generator(start: int, end: int) -> str:
    """Функция принимает начальное и конечное значения для генерации диапазона номеров."""

    for number in range(start, end + 1):
        formatted_card_number = str(number).zfill(16)
        yield " ".join([formatted_card_number[i: i + 4] for i in range(0, 16, 4)])
