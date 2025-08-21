import pytest

from src.generators import filter_by_currency, transaction_descriptions, card_number_generator


def test_filter_by_currency(trans_list: list, usd_curr: list, rub_curr: list, eur_curr: list) -> list:
    assert [filter_by_currency(trans_list, "USD") == usd_curr]
    assert [filter_by_currency(trans_list, "RUB") == rub_curr]
    assert [filter_by_currency([], "USD") == []]
    assert [filter_by_currency(trans_list, "EUR") == eur_curr]


@pytest.mark.parametrize("input_data, expected_output", [([{"description": "Оплата товара"}], ["Оплата товара"]),
                                                         ([{"description": "Перевод"}, {"description": "Покупка"}],
                                                          ["Перевод", "Покупка"]),
                                                         ([], []),
                                                         ([{"description": "Перевод организации"},
                                                           {"description": "Перевод со счета на счет"},
                                                           {"description": "Перевод с карты на карту"}],
                                                          ["Перевод организации", "Перевод со счета на счет",
                                                           "Перевод с карты на карту"])])
def test_transaction_descriptions(input_data, expected_output):
    assert list(transaction_descriptions(input_data)) == expected_output


@pytest.mark.parametrize("start, end, expected_num", [(1, 1, ["0000 0000 0000 0001"]),
                                                      (1, 3, ["0000 0000 0000 0001",
                                                              "0000 0000 0000 0002", "0000 0000 0000 0003"]),
                                                      (123, 123, ["0000 0000 0000 0123"]),
                                                      (9999999999999999, 9999999999999999, ["9999 9999 9999 9999"]),
                                                      (0, 0, ["0000 0000 0000 0000"]),
                                                      (9999999999999998, 9999999999999999,
                                                       ["9999 9999 9999 9998", "9999 9999 9999 9999"])])
def test_card_number_generator(start, end, expected_num):
    generator = card_number_generator(start, end)
    assert list(generator) == expected_num
