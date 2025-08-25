import unittest
from unittest.mock import patch, MagicMock
from src.external_api import transaction_amount, API_KEY


class TestTransactionAmount(unittest.TestCase):

    def setUp(self):
        self.empty_transaction = [{}]
        self.rub_transaction = [{
            "operationAmount": {
                "amount": "1000.00",
                "currency": {"code": "RUB"}
            }
        }]
        self.usd_transaction = [{
            "operationAmount": {
                "amount": "100.00",
                "currency": {"code": "USD"}
            }
        }]
        self.eur_transaction = [{
            "operationAmount": {
                "amount": "50.00",
                "currency": {"code": "EUR"}
            }
        }]


    def test_empty_transaction(self):
        result = transaction_amount(self.empty_transaction)
        self.assertEqual(result, "Нет транзакции!")


    def test_rub_transaction(self):
        result = transaction_amount(self.rub_transaction)
        self.assertEqual(result, "1000.00")


    @patch('src.external_api.requests.get')
    def test_eur_transaction_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": 4500.0}
        mock_get.return_value = mock_response

        result = transaction_amount(self.eur_transaction)

        self.assertEqual(result, 4500.0)
        mock_get.assert_called_once()


    @patch('src.external_api.requests.get')
    def test_api_error_400(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_get.return_value = mock_response

        result = transaction_amount(self.usd_transaction)

        self.assertEqual(result, "Запрос содержит синтаксическую ошибку или неверные параметры.")
        mock_get.assert_called_once()


    @patch('src.external_api.requests.get')
    def test_api_error_500(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        result = transaction_amount(self.usd_transaction)

        self.assertEqual(result,
                         "На стороне сервера произошла непредвиденная ошибка, которая не позволила выполнить запрос.")
        mock_get.assert_called_once()


    @patch('src.external_api.requests.get')
    def test_api_other_error_code(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = transaction_amount(self.usd_transaction)

        self.assertIsNone(result)
        mock_get.assert_called_once()


if __name__ == '__main__':
    unittest.main()
