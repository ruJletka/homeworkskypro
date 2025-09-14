from unittest.mock import patch

from main import display_transaction, setup_logger


class TestDisplayTransaction:

    def setup_method(self):
        self.logger = setup_logger()

    def test_display_transaction_complete_data(self):
        transaction = {
            "date": "2023-10-15T12:30:45.123456",
            "description": "Перевод организации",
            "from": "Visa Platinum 7000792289606361",
            "to": "Счет 73654108430135874305",
            "operationAmount": {"amount": "5000.00", "currency": {"name": "руб."}},
            "id": "123",
        }

        result = display_transaction(transaction)

        assert "15.10.2023" in result
        assert "Перевод организации" in result
        assert "7000 79** **** 6361" in result
        assert "**4305" in result
        assert "5000.00 руб." in result

    def test_display_transaction_card_to_card(self):
        transaction = {
            "date": "2023-10-16T14:22:33.000000",
            "description": "Перевод с карты на карту",
            "from": "Maestro 1596837868705199",
            "to": "Visa Classic 6831982476737658",
            "operationAmount": {"amount": "12345.67", "currency": {"name": "USD"}},
            "id": "456",
        }

        result = display_transaction(transaction)

        assert "16.10.2023" in result
        assert "Перевод с карты на карту" in result
        assert "1596 83** **** 5199" in result
        assert "6831 98** **** 7658" in result
        assert "12345.67 USD" in result

    def test_display_transaction_only_to_account(self):
        transaction = {
            "date": "2023-10-17T09:15:00.000000",
            "description": "Пополнение счета",
            "to": "Счет 48894420494657011968",
            "operationAmount": {"amount": "10000.00", "currency": {"name": "руб."}},
            "id": "789",
        }

        result = display_transaction(transaction)

        assert "17.10.2023" in result
        assert "Пополнение счета" in result
        assert "Не указано" in result
        assert "**1968" in result
        assert "10000.00 руб." in result

    def test_display_transaction_missing_date(self):
        transaction = {
            "description": "Тестовая операция",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
            "operationAmount": {"amount": "1500.00", "currency": {"name": "EUR"}},
            "id": "999",
        }

        result = display_transaction(transaction)

        assert "Тестовая операция" in result
        assert "**6952" in result
        assert "**6702" in result
        assert "1500.00 EUR" in result

    def test_display_transaction_missing_amount(self):
        transaction = {
            "date": "2023-10-18T16:45:00.000000",
            "description": "Без суммы",
            "from": "Visa Gold 5999414228426353",
            "to": "Счет 73654108430135874305",
            "operationAmount": {"currency": {"name": "руб."}},
            "id": "888",
        }
        result = display_transaction(transaction)

        assert "18.10.2023" in result
        assert "Без суммы" in result
        assert "5999 41** **** 6353" in result
        assert "0 руб." in result

    def test_display_transaction_missing_currency(self):
        transaction = {
            "date": "2023-10-19T11:30:00.000000",
            "description": "Без валюты",
            "from": "MasterCard 7158300734726758",
            "to": "Счет 35383033474447895560",
            "operationAmount": {"amount": "2000.00"},
            "id": "777",
        }

        result = display_transaction(transaction)

        assert "19.10.2023" in result
        assert "Без валюты" in result
        assert "7158 30** **** 6758" in result
        assert "2000.00 руб." in result

    def test_display_transaction_empty_operation_amount(self):
        transaction = {
            "date": "2023-10-20T10:00:00.000000",
            "description": "Пустая сумма операции",
            "from": "Счет 10848359769870775355",
            "to": "Счет 64686473678894779589",
            "operationAmount": {},
            "id": "666",
        }

        result = display_transaction(transaction)

        assert "20.10.2023" in result
        assert "Пустая сумма операции" in result
        assert "**5355" in result
        assert "**9589" in result
        assert "0 руб." in result

    def test_display_transaction_minimal_data(self):
        transaction = {"description": "Минимальные данные", "id": "555"}

        result = display_transaction(transaction)

        assert "Минимальные данные" in result
        assert "Не указано" in result
        assert "Не указано" in result
        assert "0 руб." in result

    @patch("main.mask_account_card")
    def test_mask_account_card_called_correctly(self, mock_mask):
        mock_mask.return_value = "**TEST**"

        transaction = {
            "date": "2023-10-21T15:00:00.000000",
            "description": "Тест маскировки",
            "from": "Счет 12345678901234567890",
            "to": "Visa 1234123412341234",
            "operationAmount": {"amount": "1000.00", "currency": {"name": "руб."}},
            "id": "444",
        }

        result = display_transaction(transaction)

        assert mock_mask.call_count == 2
        mock_mask.assert_any_call("Счет 12345678901234567890")
        mock_mask.assert_any_call("Visa 1234123412341234")
        assert "**TEST**" in result

    @patch("main.get_date")
    def test_get_date_called_correctly(self, mock_get_date):
        mock_get_date.return_value = "21.10.2023"

        transaction = {
            "date": "2023-10-21T15:00:00.000000",
            "description": "Тест даты",
            "from": "Счет 12345678901234567890",
            "to": "Счет 09876543210987654321",
            "operationAmount": {"amount": "1000.00", "currency": {"name": "руб."}},
            "id": "333",
        }

        result = display_transaction(transaction)

        mock_get_date.assert_called_once_with("2023-10-21T15:00:00.000000")
        assert "21.10.2023" in result
