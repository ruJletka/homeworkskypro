from typing import Dict, List

import pytest

from src.bank_operations import process_bank_search


class TestProcessBankSearch:

    @pytest.fixture
    def sample_data(self) -> List[Dict]:
        return [
            {"id": 1, "amount": 1000, "description": "Перевод на карту Сбербанк", "date": "2023-10-01"},
            {"id": 2, "amount": -500, "description": "Оплата услуг Яндекс.Такси", "date": "2023-10-02"},
            {"id": 3, "amount": -200, "description": "Покупка в Сбермаркете", "date": "2023-10-03"},
            {"id": 4, "amount": -150, "description": "", "date": "2023-10-04"},
            {"id": 5, "amount": 3000, "description": "Зарплата от компании Яндекс", "date": "2023-10-05"},
        ]

    def test_search_existing_word(self, sample_data):
        result = process_bank_search(sample_data, "Сбер")
        assert len(result) == 2
        assert all("Сбер" in op["description"] for op in result)
        assert {op["id"] for op in result} == {1, 3}

    def test_search_case_insensitive(self, sample_data):
        result_lower = process_bank_search(sample_data, "яндекс")
        result_upper = process_bank_search(sample_data, "ЯНДЕКС")
        result_mixed = process_bank_search(sample_data, "Яндекс")

        assert len(result_lower) == 2
        assert len(result_upper) == 2
        assert len(result_mixed) == 2
        assert {op["id"] for op in result_lower} == {2, 5}

    def test_search_nonexistent_word(self, sample_data):
        result = process_bank_search(sample_data, "НесуществующееСлово")
        assert len(result) == 0

    def test_empty_search_string(self, sample_data):
        result = process_bank_search(sample_data, "")
        assert len(result) == len(sample_data)

    def test_search_with_special_characters(self, sample_data):
        data_with_special = sample_data + [
            {"id": 6, "amount": -100, "description": "Оплата Netflix.com", "date": "2023-10-06"}
        ]

        result = process_bank_search(data_with_special, "Netflix.com")
        assert len(result) == 1
        assert result[0]["id"] == 6

    def test_search_partial_word(self, sample_data):
        result = process_bank_search(sample_data, "карт")
        assert len(result) == 1
        assert result[0]["id"] == 1

    def test_empty_data(self):
        result = process_bank_search([], "Сбер")
        assert len(result) == 0

    def test_data_without_description(self):
        data = [
            {"id": 1, "amount": 100},
            {"id": 2, "amount": 200, "description": "Перевод"},
            {"id": 3, "amount": 300, "description": None},
        ]

        result = process_bank_search(data, "Перевод")
        assert len(result) == 1
        assert result[0]["id"] == 2

    def test_search_regex_special_chars_escaping(self):
        data = [
            {"id": 1, "description": "Payment (invoice 123)", "amount": 100},
            {"id": 2, "description": "Refund [order 456]", "amount": -50},
            {"id": 3, "description": "Bonus+extra", "amount": 200},
        ]

        test_cases = [("(invoice", [1]), ("[order", [2]), ("+extra", [3]), ("123)", [1]), ("456]", [2])]

        for search_string, expected_ids in test_cases:
            result = process_bank_search(data, search_string)
            assert {op["id"] for op in result} == set(expected_ids)

    def test_multiple_words_search(self, sample_data):
        result = process_bank_search(sample_data, "Оплата услуг")
        assert len(result) == 1
        assert result[0]["id"] == 2

    def test_none_search_string(self):
        data = [{"id": 1, "description": "test", "amount": 100}]
        result = process_bank_search(data, None)
        assert len(result) == 1
