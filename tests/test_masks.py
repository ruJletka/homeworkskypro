import pytest
from unittest.mock import patch, MagicMock
import logging

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("1596837868705199", "1596 83 ** 5199"),
        ("7158300734726758", "7158 30 ** 6758"),
        ("6831982476737658", "6831 98 ** 7658"),
        ("8990922113665229", "8990 92 ** 5229"),
        ("5999414228426353", "5999 41 ** 6353"),
        ("1337666777228282", "1337 66 ** 8282"),
        ("89909221136652292", "Несуществующий номер карты"),
        ("5e99941f228426c3", "Несуществующий номер карты"),
        ("1234", "Несуществующий номер карты"),
        ("", "Несуществующий номер карты"),
    ]
)
def test_get_mask_card_number(card_number: str, expected: str) -> None:
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize(
    "account_number, expected",
    [
        ("73654108430135874305", "**4305"),
        ("35383033474447895560", "**5560"),
        ("64686473678894779589", "**9589"),
        ("00000000000000000000", "**0000"),
        ("11111111111111111111", "**1111"),
        ("646864736788947795890", "Неверный номер аккаунта"),
        ("0z0f00h00g00r00e00c0", "Неверный номер аккаунта"),
        ("12345", "Неверный номер аккаунта"),
        ("", "Неверный номер аккаунта"),
    ]
)
def test_get_mask_account(account_number: str, expected: str) -> None:
    assert get_mask_account(account_number) == expected


def test_get_mask_card_number_logging() -> None:
    with patch('src.masks.logger') as mock_logger:
        result = get_mask_card_number("1596837868705199")
        assert result == "1596 83 ** 5199"

        mock_logger.info.assert_any_call("Вызов функции get_mask_card_number с аргументом: 1596837868705199")
        mock_logger.info.assert_any_call("Успешное создание маски карты: 1596 83 ** 5199")

        result = get_mask_card_number("123")
        assert result == "Несуществующий номер карты"

        mock_logger.error.assert_called_with(
            "Ошибка в get_mask_card_number: Несуществующий номер карты. Входные данные: 123"
        )


def test_get_mask_account_logging() -> None:
    with patch('src.masks.logger') as mock_logger:
        result = get_mask_account("73654108430135874305")
        assert result == "**4305"

        mock_logger.info.assert_any_call("Вызов функции get_mask_account с аргументом: 73654108430135874305")
        mock_logger.info.assert_any_call("Успешное создание маски аккаунта: **4305")

        result = get_mask_account("short")
        assert result == "Неверный номер аккаунта"

        mock_logger.error.assert_called_with(
            "Ошибка в get_mask_account: Неверный номер аккаунта. Входные данные: short"
        )


def test_get_mask_card_number_edge_cases() -> None:
    assert get_mask_card_number("1" * 16) == "1111 11 ** 1111"

    assert get_mask_card_number("0" * 16) == "0000 00 ** 0000"

    assert get_mask_card_number(None) == "Несуществующий номер карты"

    assert get_mask_card_number(1596837868705199) == "1596 83 ** 5199"


def test_get_mask_account_edge_cases() -> None:
    assert get_mask_account("1" * 20) == "**1111"

    assert get_mask_account("0" * 20) == "**0000"

    assert get_mask_account(None) == "Неверный номер аккаунта"

    assert get_mask_account(73654108430135874305) == "**4305"
