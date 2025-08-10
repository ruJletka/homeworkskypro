import pytest
from src.widget import mask_account_card, get_date


@pytest.mark.parametrize("entry_value, expected", [("Visa Gold 1596837868705199", "Visa Gold 1596 83** **** 5199"),
                                                    ("MasterCard 15968378687051994", "Несуществующий номер карты"),
                                                    ("dsdasda 1596837868705199y", "Несуществующий номер карты"),
                                                    ("Счет 73654108430135874305", "Счет **4305"),
                                                    ("Счет 35383033474447895560", "Счет **5560"),
                                                    ("Счет 35383033474447895560t", "Неверный номер аккаунта"),
                                                    ("Счет 3538303347", "Неверный номер аккаунта")])

def test_mask_account_card(entry_value, expected):
    assert mask_account_card(entry_value) == expected


def test_get_date():
    assert get_date("2024-03-11T02:26:18.671407") == "11.03.2024"