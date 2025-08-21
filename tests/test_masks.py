import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize("card_number, expected", [("1596837868705199", "1596 83** **** 5199"),
                                                   ("7158300734726758", "7158 30** **** 6758"),
                                                   ("6831982476737658", "6831 98** **** 7658"),
                                                   ("8990922113665229", "8990 92** **** 5229"),
                                                   ("5999414228426353", "5999 41** **** 6353"),
                                                   ("1337666777228282", "1337 66** **** 8282"),
                                                   ("89909221136652292", "Несуществующий номер карты"),
                                                   ("5e99941f228426c3", "Несуществующий номер карты")])
def test_get_mask_card(card_number: str, expected: str) -> str:
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize("account_number, expected", [("73654108430135874305", "**4305"),
                                                      ("35383033474447895560", "**5560"),
                                                      ("64686473678894779589", "**9589"),
                                                      ("00000000000000000000", "**0000"),
                                                      ("11111111111111111111", "**1111"),
                                                      ("646864736788947795890", "Неверный номер аккаунта"),
                                                      ("0z0f00h00g00r00e00c0", "Неверный номер аккаунта")])
def test_get_mask_account(account_number: str, expected: str) -> str:
    assert get_mask_account(account_number) == expected
