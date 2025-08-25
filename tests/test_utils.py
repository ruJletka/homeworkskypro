import unittest
from idlelib.iomenu import encoding
from unittest.mock import mock_open, patch
import json
from src.utils import load_transaction_data


class TestDataLoaderParametrized(unittest.TestCase):

    @patch('os.path.exists')
    @patch('os.path.getsize')
    def test_file_not_exists_or_empty(self, mock_getsize, mock_exists):
        test_cases = [
            (False, 100, []),
            (True, 0, []),
        ]

        for exists, size, expected in test_cases:
            with self.subTest(exists=exists, size=size):
                mock_exists.return_value = exists
                mock_getsize.return_value = size

                result = load_transaction_data('test.json')
                self.assertEqual(result, expected)

                mock_exists.assert_called_with('test.json')
                if exists:
                    mock_getsize.assert_called_with('test.json')

                mock_exists.reset_mock()
                mock_getsize.reset_mock()


    @patch('os.path.exists')
    @patch('os.path.getsize')
    @patch('builtins.open')
    def test_json_loading_errors(self, mock_open_file, mock_getsize, mock_exists):
        mock_exists.return_value = True
        mock_getsize.return_value = 100
        error_cases = [(FileNotFoundError("Not found"), []),
                       (PermissionError("No access"), []),
                       (json.JSONDecodeError("Invalid JSON", "test", 0), []),
                      ]
        for error, expected in error_cases:
            with self.subTest(error=type(error).__name__):
                mock_open_file.side_effect = error
                result = load_transaction_data('error.json')
                self.assertEqual(result, expected)
                mock_open_file.assert_called_with('error.json', 'r', encoding='utf-8')
                mock_open_file.reset_mock()

    @patch('os.path.exists')
    @patch('os.path.getsize')
    @patch('builtins.open')
    def test_invalid_data_types(self, mock_open_file, mock_getsize, mock_exists):
        mock_exists.return_value = True
        mock_getsize.return_value = 100
        invalid_data_cases = [({"not": "a list"}, []),
                              ("string", []),
                              (123, []),
                              (None, []),
                             ]
        for data, expected in invalid_data_cases:
            with self.subTest(data_type=type(data).__name__):
                with patch('json.load') as mock_json_load:
                    mock_json_load.return_value = data
                    result = load_transaction_data('invalid_type.json')
                    self.assertEqual(result, expected)
                    mock_open_file.assert_called_with('invalid_type.json', 'r', encoding='utf-8')
                    mock_open_file.reset_mock()


if __name__ == '__main__':
    unittest.main()
