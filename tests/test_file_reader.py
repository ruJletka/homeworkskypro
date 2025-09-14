from unittest.mock import mock_open, patch

import pandas as pd
import pytest

from src.file_reader import read_transaction_csv, read_transaction_excel


def test_read_transaction_csv_success(test_csv_data, expected_result):
    with patch('builtins.open', mock_open(read_data=test_csv_data)):
        with patch('os.path.join', return_value="data/transactions.csv"):
            result = read_transaction_csv()

            assert len(result) == 3
            assert result == expected_result
            assert isinstance(result, list)
            for item in result:
                assert isinstance(item, dict)


def test_read_transaction_csv_file_not_found():
    with patch('builtins.open', side_effect=FileNotFoundError("File not found")):
        with patch('os.path.join', return_value="data/transactions.csv"):
            with pytest.raises(FileNotFoundError):
                read_transaction_csv()


def test_read_transaction_csv_encoding_error():
    with patch('builtins.open', side_effect=UnicodeDecodeError("utf-8", b"", 0, 1, "Invalid byte")):
        with patch('os.path.join', return_value="data/transactions.csv"):
            with pytest.raises(UnicodeDecodeError):
                read_transaction_csv()


@patch('pandas.read_excel')
def test_read_transaction_excel_success(mock_read_excel, expected_result):
    mock_df = pd.DataFrame(expected_result)
    mock_read_excel.return_value = mock_df

    with patch('os.path.join', return_value="data/transactions_excel.xlsx"):
        result = read_transaction_excel()

        assert len(result) == 3
        assert result == expected_result
        assert isinstance(result, list)
        for item in result:
            assert isinstance(item, dict)

    mock_read_excel.assert_called_once_with("data/transactions_excel.xlsx")


@patch('pandas.read_excel')
def test_read_transaction_excel_file_not_found(mock_read_excel):
    mock_read_excel.side_effect = FileNotFoundError("Excel file not found")

    with patch('os.path.join', return_value="data/transactions_excel.xlsx"):
        with pytest.raises(FileNotFoundError):
            read_transaction_excel()


def test_read_transaction_csv_empty_file():
    empty_csv_data = "date;amount;category;description"

    with patch('builtins.open', mock_open(read_data=empty_csv_data)):
        with patch('os.path.join', return_value="data/transactions.csv"):
            result = read_transaction_csv()

            assert result == []


@patch('pandas.read_excel')
def test_read_transaction_excel_empty_file(mock_read_excel):
    mock_df = pd.DataFrame()
    mock_read_excel.return_value = mock_df

    with patch('os.path.join', return_value="data/transactions_excel.xlsx"):
        result = read_transaction_excel()

        assert result == []
