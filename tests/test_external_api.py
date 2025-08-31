import unittest
from unittest.mock import MagicMock, patch

from src.external_api import transaction_amount


class TestTransactionAmount(unittest.TestCase):

    def test_empty_transaction(self):
        result = transaction_amount({})
        self.assertEqual(result, "Нет транзакции!")

    def test_none_transaction(self):
        result = transaction_amount(None)
        self.assertEqual(result, "Нет транзакции!")

    def test_rub_currency(self):
        transaction = {
            "operationAmount": {
                "amount": "1500.50",
                "currency": {
                    "code": "RUB"
                }
            }
        }
        result = transaction_amount(transaction)
        self.assertEqual(result, 1500.50)

    @patch('src.external_api.API_KEY', 'test_api_key')
    @patch('requests.get')
    def test_usd_currency_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "result": 7500.25
        }
        mock_get.return_value = mock_response

        transaction = {
            "operationAmount": {
                "amount": "100.00",
                "currency": {
                    "code": "USD"
                }
            }
        }

        result = transaction_amount(transaction)

        self.assertEqual(result, 7500.25)
        mock_get.assert_called_once_with(
            "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=USD&amount=100.0",
            headers={"apikey": "test_api_key"}
        )

    @patch('src.external_api.API_KEY', 'test_api_key')
    @patch('requests.get')
    def test_eur_currency_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "result": 8500.75
        }
        mock_get.return_value = mock_response

        transaction = {
            "operationAmount": {
                "amount": "85.50",
                "currency": {
                    "code": "EUR"
                }
            }
        }

        result = transaction_amount(transaction)

        self.assertEqual(result, 8500.75)
        mock_get.assert_called_once_with(
            "https://api.apilayer.com/exchangerates_data/convert?to=RUB&from=EUR&amount=85.5",
            headers={"apikey": "test_api_key"}
        )

    @patch('src.external_api.API_KEY', 'test_api_key')
    @patch('requests.get')
    def test_api_failure_status_code(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_get.return_value = mock_response

        transaction = {
            "operationAmount": {
                "amount": "100.00",
                "currency": {
                    "code": "USD"
                }
            }
        }

        result = transaction_amount(transaction)
        self.assertEqual(result, "Ошибка при конвертации валюты")

    @patch('src.external_api.API_KEY', 'test_api_key')
    @patch('requests.get')
    def test_api_failure_success_false(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": False,
            "error": {"info": "Invalid API key"}
        }
        mock_get.return_value = mock_response

        transaction = {
            "operationAmount": {
                "amount": "100.00",
                "currency": {
                    "code": "USD"
                }
            }
        }

        result = transaction_amount(transaction)
        self.assertEqual(result, "Ошибка при конвертации валюты")

    @patch('src.external_api.API_KEY', 'test_api_key')
    @patch('requests.get')
    def test_api_exception(self, mock_get):
        mock_get.side_effect = Exception("Connection error")

        transaction = {
            "operationAmount": {
                "amount": "100.00",
                "currency": {
                    "code": "USD"
                }
            }
        }

        result = transaction_amount(transaction)
        self.assertEqual(result, "Ошибка при запросе к API")

    def test_unsupported_currency(self):
        transaction = {
            "operationAmount": {
                "amount": "100.00",
                "currency": {
                    "code": "GBP"
                }
            }
        }

        result = transaction_amount(transaction)
        self.assertEqual(result, "Неподдерживаемая валюта: GBP")
