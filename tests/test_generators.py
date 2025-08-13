import pytest

from src.generators import filter_by_currency, transaction_descriptions, card_number_generator


def test_filter_by_currency(trans_list: list, usd_curr: list, rub_curr: list) -> list:
    assert [filter_by_currency(trans_list, "USD") == usd_curr]
    return usd_curr
    assert [filter_by_currency(trans_list, "RUB") == rub_curr]
    return rub_curr
    assert [filter_by_currency([], "USD") == []]
    return []
    assert [filter_by_currency(trans_list, "EUR") == eur_curr]
    return eur_curr


