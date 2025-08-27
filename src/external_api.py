import os
from typing import Any, Dict, Union

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')


def transaction_amount(transaction: Dict[str, Any]) -> Union[float, str]:
    """Функция, принимающая на вход транзакцию и возвращающая сумму транзакции в рублях или сообщение об ошибке"""
    if not transaction or transaction == {}:
        return "Нет транзакции!"

    # Получаем данные о валюте и сумме
    currency_code = transaction["operationAmount"]["currency"]["code"]
    amount = float(transaction["operationAmount"]["amount"])

    if currency_code == "RUB":
        return amount

    if currency_code in ["USD", "EUR"]:
        url = f"https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency_code}&amount={amount}"
        headers = {"apikey": API_KEY}

        try:
            response = requests.get(url, headers=headers)
            data = response.json()

            if response.status_code == 200 and data.get("success", False):
                return round(data["result"], 2)
            else:
                return "Ошибка при конвертации валюты"

        except:
            return "Ошибка при запросе к API"

    return f"Неподдерживаемая валюта: {currency_code}"
