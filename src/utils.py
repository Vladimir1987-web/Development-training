import json
import os
from typing import Dict

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.apilayer.com/exchangerates_data/latest"


def funk_data_transactions(way: str) -> list[dict]:
    """Принимает на вход путь до JSON-файла и возвращает список словарей с данными о финансовых транзакциях"""
    try:
        with open(way, encoding='utf-8') as f:
            try:
                data = json.loads(f.read())
            except json.JSONDecodeError:
                return []
        return data
    except FileNotFoundError:
        return []


def convert_to_rub(transaction: Dict) -> float:
    """Конвертирует сумму транзакции из исходной валюты в рубли по текущему курсу и возвращает сумму транзакции (ключ
amount) в рублях, тип данных float."""
    try:
        # Проверка наличия API ключа
        if not API_KEY:
            raise ValueError("API key not configured")

        # Извлечение данных
        amount = float(transaction["operationAmount"]["amount"])
        currency = transaction["operationAmount"]["currency"]["code"].upper()

        if currency == "RUB":
            return amount

        if currency not in ("USD", "EUR"):
            raise ValueError(f"Unsupported currency: {currency}")

        # Запрос к API
        response = requests.get(
            BASE_URL,
            params={"base": currency, "symbols": "RUB"},
            headers={"apikey": API_KEY},
            timeout=10
        )
        response.raise_for_status()

        data = response.json()
        print(data)

        # Проверка успешности ответа
        if not data.get('success', True):
            error_info = data.get('error', {}).get('info', 'Unknown API error')
            raise ValueError(f"API error: {error_info}")

        if 'rates' not in data or 'RUB' not in data['rates']:
            raise ValueError("Invalid API response format")

        return round(amount * data['rates']['RUB'], 2)

    except KeyError as e:
        raise ValueError(f"Missing required field in transaction: {e}")
    except requests.exceptions.RequestException as e:
        raise ValueError(f"API connection error: {str(e)}")


if __name__ == '__main__':
    print(funk_data_transactions(r'C:\Training\Python-development\Project\pythonProjectBank\data\operations.json'))
    print(convert_to_rub(
        {
            "id": 242885401,
            "state": "EXECUTED",
            "date": "2019-07-08T00:08:32.986663",
            "operationAmount": {
                "amount": "10083.68",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 38427597486442637521",
            "to": "Счет 83889757415570699323"
        }
    )
    )
