from src.bank_analytics import process_bank_operations


def test_basic_counting():
    data = [
        {"description": "Перевод в Сбербанк", "amount": 100},
        {"description": "Оплата Яндекс.Такси", "amount": -500},
        {"description": "Покупка в Сбермаркете", "amount": -200},
    ]

    categories = ["Сбер", "Яндекс"]
    result = process_bank_operations(data, categories)

    assert result == {"Сбер": 2, "Яндекс": 1}


def test_case_insensitive():
    data = [
        {"description": "ПЕРЕВОД В СБЕРБАНК", "amount": 100},
        {"description": "оплата яндекс.такси", "amount": -500},
    ]

    categories = ["сбер", "ЯНДЕКС"]
    result = process_bank_operations(data, categories)

    assert result == {"сбер": 1, "ЯНДЕКС": 1}


def test_empty_categories():
    data = [{"description": "Перевод", "amount": 100}]
    result = process_bank_operations(data, [])
    assert result == {}


def test_no_matches():
    data = [{"description": "Перевод", "amount": 100}]
    categories = ["Яндекс", "Такси"]
    result = process_bank_operations(data, categories)
    assert result == {"Яндекс": 0, "Такси": 0}


def test_operations_without_description():
    data = [{"description": "Перевод в Сбер", "amount": 100}, {"description": "", "amount": 200}, {"amount": 300}]

    categories = ["Сбер"]
    result = process_bank_operations(data, categories)
    assert result == {"Сбер": 1}
