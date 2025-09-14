import json
import os
import unittest
from unittest.mock import mock_open, patch

from src.utils import load_transaction_data


class TestLoadTransactionData(unittest.TestCase):

    @patch("os.path.exists")
    @patch("os.path.getsize")
    def test_file_not_exists(self, mock_getsize, mock_exists):
        mock_exists.return_value = False
        mock_getsize.return_value = 100

        result = load_transaction_data()

        self.assertEqual(result, [])
        mock_exists.assert_called_once_with(os.path.join("data", "operations.json"))
        mock_getsize.assert_not_called()

    @patch("os.path.exists")
    @patch("os.path.getsize")
    def test_empty_file(self, mock_getsize, mock_exists):
        mock_exists.return_value = True
        mock_getsize.return_value = 0

        result = load_transaction_data()

        self.assertEqual(result, [])
        mock_exists.assert_called_once_with(os.path.join("data", "operations.json"))
        mock_getsize.assert_called_once_with(os.path.join("data", "operations.json"))

    @patch("os.path.exists")
    @patch("os.path.getsize")
    @patch("builtins.open", new_callable=mock_open)
    def test_valid_json_data(self, mock_file, mock_getsize, mock_exists):
        mock_exists.return_value = True
        mock_getsize.return_value = 100

        test_data = [
            {"id": 1, "amount": 100, "description": "Test transaction"},
            {"id": 2, "amount": 200, "description": "Another transaction"},
        ]

        with patch("json.load") as mock_json_load:
            mock_json_load.return_value = test_data

            result = load_transaction_data()

            self.assertEqual(result, test_data)
            mock_file.assert_called_once_with(os.path.join("data", "operations.json"), "r", encoding="utf-8")
            mock_json_load.assert_called_once()

    @patch("os.path.exists")
    @patch("os.path.getsize")
    @patch("builtins.open", new_callable=mock_open)
    def test_json_not_list(self, mock_file, mock_getsize, mock_exists):
        mock_exists.return_value = True
        mock_getsize.return_value = 100

        with patch("json.load") as mock_json_load:
            mock_json_load.return_value = {"not": "a list"}

            result = load_transaction_data()

            self.assertEqual(result, [])
            mock_file.assert_called_once_with(os.path.join("data", "operations.json"), "r", encoding="utf-8")
            mock_json_load.assert_called_once()

    @patch("os.path.exists")
    @patch("os.path.getsize")
    @patch("builtins.open", new_callable=mock_open)
    def test_json_decode_error(self, mock_file, mock_getsize, mock_exists):
        mock_exists.return_value = True
        mock_getsize.return_value = 100

        with patch("json.load") as mock_json_load:
            mock_json_load.side_effect = json.JSONDecodeError("Invalid JSON", "doc", 0)

            result = load_transaction_data()

            self.assertEqual(result, [])
            mock_file.assert_called_once_with(os.path.join("data", "operations.json"), "r", encoding="utf-8")
            mock_json_load.assert_called_once()

    @patch("os.path.exists")
    @patch("os.path.getsize")
    def test_permission_error(self, mock_getsize, mock_exists):
        mock_exists.return_value = True
        mock_getsize.return_value = 100

        with patch("builtins.open") as mock_open:
            mock_open.side_effect = PermissionError("No permission")

            result = load_transaction_data()

            self.assertEqual(result, [])
            mock_open.assert_called_once_with(os.path.join("data", "operations.json"), "r", encoding="utf-8")

    @patch("os.path.exists")
    @patch("os.path.getsize")
    def test_file_not_found_error(self, mock_getsize, mock_exists):
        mock_exists.return_value = True
        mock_getsize.return_value = 100

        with patch("builtins.open") as mock_open:
            mock_open.side_effect = FileNotFoundError("File disappeared")

            result = load_transaction_data()

            self.assertEqual(result, [])
            mock_open.assert_called_once_with(os.path.join("data", "operations.json"), "r", encoding="utf-8")

    @patch("os.path.exists")
    @patch("os.path.getsize")
    def test_general_exception(self, mock_getsize, mock_exists):
        mock_exists.return_value = True
        mock_getsize.return_value = 100

        with patch("builtins.open") as mock_open:
            mock_open.side_effect = Exception("Some unexpected error")

            result = load_transaction_data()

            self.assertEqual(result, [])
            mock_open.assert_called_once_with(os.path.join("data", "operations.json"), "r", encoding="utf-8")
