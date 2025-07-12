import json
from unittest.mock import patch

import pytest

from src.utils import convert_to_rub, funk_data_transactions

""""Тестирование функции funk_data_transactions"""


# Проверка правильности работы функции
@patch("builtins.open", create=True)
def tests_funk_data_transactions(mock_open) -> None:
    mock_file = mock_open.return_value.__enter__.return_value
    fake_data = [
        {
            "id": 441945886,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589",
        },
        {
            "id": 41428829,
            "state": "EXECUTED",
            "date": "2019-07-03T18:35:29.512364",
            "operationAmount": {"amount": "8221.37", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "MasterCard 7158300734726758",
            "to": "Счет 35383033474447895560",
        },
    ]
    json_fake_data = json.dumps(fake_data)
    mock_file.read.return_value = json_fake_data
    assert funk_data_transactions("file_path") == fake_data
    mock_open.assert_called_once_with("file_path", encoding="utf-8")


# если JSON-строка имеет неправильный формат, содержит некорректные символы или имеет другие ошибки
@patch("builtins.open", create=True)
def tests_funk_data_transactions_value(mock_open) -> None:
    mock_file = mock_open.return_value.__enter__.return_value
    fake_data = "{'name': 'John', 'age': 30, 'city': 'New York'}"
    mock_file.read.return_value = fake_data
    assert funk_data_transactions("file_path") == []


# если файл не найден
def tests_funk_data_transactions_not_found() -> None:
    assert funk_data_transactions(r"C:\Training\Python-development\Project\pythonProjectBank\data\op.json") == []


""""Тестирование функции convert_to_rub"""


@pytest.fixture
def one_transaction_rub() -> dict:
    return {
        "id": 441945886,
        "state": "EXECUTED",
        "date": "2019-08-26T10:50:58.294041",
        "operationAmount": {"amount": "31957.58", "currency": {"name": "руб.", "code": "RUB"}},
    }


@pytest.fixture
def one_transaction_usd() -> dict:
    return {
        "id": 41428829,
        "state": "EXECUTED",
        "date": "2019-07-03T18:35:29.512364",
        "operationAmount": {"amount": "8221.37", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "MasterCard 7158300734726758",
        "to": "Счет 35383033474447895560",
    }


@pytest.fixture
def one_transaction_error() -> dict:
    return {
        "id": 41428829,
        "state": "EXECUTED",
        "date": "2019-07-03T18:35:29.512364",
        "operationAmount": {"amount": "8221.37", "currency": {"name": "USA", "code": "USA"}},
        "description": "Перевод организации",
        "from": "MasterCard 7158300734726758",
        "to": "Счет 35383033474447895560",
    }


# Проверка правильности работы функции


# Если валюта в рублях
def test_transaction_rub(one_transaction_rub) -> None:
    assert convert_to_rub(one_transaction_rub) == float(one_transaction_rub["operationAmount"]["amount"])


# Если валюта в USD
@patch("requests.get")
def test_transaction_usd(mock_get, one_transaction_usd) -> None:
    mock_get.return_value.json.return_value = {
        "success": True,
        "timestamp": 1752256276,
        "base": "USD",
        "date": "2025-07-11",
        "rates": {"RUB": 77.999},
    }
    convert_rub = round(float(one_transaction_usd["operationAmount"]["amount"]) * 77.999, 2)
    assert convert_to_rub(one_transaction_usd) == convert_rub
    mock_get.assert_called_once()


# При некорректной валюте
def test_transaction_error(one_transaction_error) -> None:
    with pytest.raises(ValueError):
        convert_to_rub(one_transaction_error)


# Проверка успешности ответа
@patch("requests.get")
def test_answer_error1(mock_get, one_transaction_usd) -> None:
    mock_get.return_value.json.return_value = {
        "success": False,
        "timestamp": 1752256276,
        "base": "USD",
        "date": "2025-07-11",
        "rates": {"RUB": 77.999},
    }
    with pytest.raises(ValueError):
        convert_to_rub(one_transaction_usd)
    mock_get.assert_called_once()


@patch("requests.get")
def test_answer_error2(mock_get, one_transaction_usd) -> None:
    mock_get.return_value.json.return_value = {
        "success": True,
        "timestamp": 1752256276,
        "base": "USD",
        "date": "2025-07-11",
        "r": {"RUB": 77.999},
    }
    with pytest.raises(ValueError):
        convert_to_rub(one_transaction_usd)
    mock_get.assert_called_once()


@patch("requests.get")
def test_answer_error3(mock_get, one_transaction_usd) -> None:
    mock_get.return_value.json.return_value = {
        "success": False,
        "timestamp": 1752256276,
        "base": "USD",
        "date": "2025-07-11",
        "rates": {"USD": 77.999},
    }
    with pytest.raises(ValueError):
        convert_to_rub(one_transaction_usd)
    mock_get.assert_called_once()


# При отсутствии необходимых ключей в транзакции
@patch("requests.get")
def test_key_success(mock_get, one_transaction_usd) -> None:
    mock_get.return_value.json.return_value = {
        "timestamp": 1752256276,
        "base": "USD",
        "date": "2025-07-11",
        "rates": {"USD": 77.999},
    }
    with pytest.raises(ValueError):
        convert_to_rub(one_transaction_usd)
    mock_get.assert_called_once()


# При отсутствии данных транзакции
@patch("requests.get")
def test_not_data(mock_get, one_transaction_usd) -> None:
    mock_get.return_value.json.return_value = {}
    with pytest.raises(ValueError):
        convert_to_rub(one_transaction_usd)
    mock_get.assert_called_once()
