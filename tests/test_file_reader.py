import unittest
from unittest.mock import MagicMock, mock_open, patch

from src.file_reader import read_transaction_csv, read_transaction_excel


class TestTransactionFunctions(unittest.TestCase):

    def test_read_transaction_csv_normal_case(self):
        csv_content = """date;amount;description
2023-01-01;1000.00;Salary
2023-01-02;-50.00;Grocery"""

        expected_result = [
            {'date': '2023-01-01', 'amount': '1000.00', 'description': 'Salary'},
            {'date': '2023-01-02', 'amount': '-50.00', 'description': 'Grocery'}
        ]

        with patch('builtins.open', mock_open(read_data=csv_content)):
            with patch('csv.DictReader') as mock_reader:
                mock_reader.return_value = expected_result

                result = read_transaction_csv('test.csv')
                self.assertEqual(result, expected_result)

    def test_read_transaction_csv_empty_file(self):
        csv_content = "date;amount;description\n"

        with patch('builtins.open', mock_open(read_data=csv_content)):
            with patch('csv.DictReader') as mock_reader:
                mock_reader.return_value = []

                result = read_transaction_csv('empty.csv')
                self.assertEqual(result, [])

    def test_read_transaction_excel_normal_case(self):
        mock_df = MagicMock()
        expected_result = [
            {'date': '2023-01-01', 'amount': '1000.00', 'description': 'Salary'},
            {'date': '2023-01-02', 'amount': '-50.00', 'description': 'Grocery'}
        ]

        mock_df.to_dict.return_value = expected_result

        with patch('pandas.read_excel', return_value=mock_df):
            result = read_transaction_excel('test.xlsx')
            self.assertEqual(result, expected_result)

    def test_read_transaction_excel_empty_file(self):
        mock_df = MagicMock()
        mock_df.to_dict.return_value = []

        with patch('pandas.read_excel', return_value=mock_df):
            result = read_transaction_excel('empty.xlsx')
            self.assertEqual(result, [])
