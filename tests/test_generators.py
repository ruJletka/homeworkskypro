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


@pytest.mark.parametrize("input_data, expected_output", [([{"description": "Оплата товара"}], ["Оплата товара"]),
                                                        ([{"description": "Перевод"}, {"description": "Покупка"}], ["Перевод", "Покупка"]),
                                                        ([], []),
                                                        ([{"description": "Перевод организации"},
                                                          {"description": "Перевод со счета на счет"}, {"description": "Перевод с карты на карту"}],
                                                         ["Перевод организации", "Перевод со счета на счет", "Перевод с карты на карту"])])
def test_transaction_descriptions(input_data, expected_output):
    assert list(transaction_descriptions(input_data)) == expected_output