import re

import pytest
from pytest import FixtureRequest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.fixture()
def transactions() -> list:
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657",
        },
    ]


@pytest.fixture()
def currency_usd() -> dict[str, str | dict[str, str | dict[str, str]] | int]:
    return {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    }


@pytest.fixture()
def currency_rub() -> dict[str, str | dict[str, str | dict[str, str]] | int]:
    return {
        "id": 873106923,
        "state": "EXECUTED",
        "date": "2019-03-23T01:09:46.296404",
        "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 44812258784861134719",
        "to": "Счет 74489636417521191160",
    }


""" Тесты функции filter_by_currency. """


# Тест функции на корректную фильтрацию транзакции по заданной валюте.
@pytest.mark.parametrize("currency, currency_withdrawal", [("USD", "currency_usd"), ("RUB", "currency_rub")])
def test_filter_by_currency(
    transactions: list, currency: str, currency_withdrawal: str, request: FixtureRequest
) -> None:
    expected = request.getfixturevalue(currency_withdrawal)
    assert next(filter_by_currency(transactions, currency)) == expected


# Если список пустой
def test_filter_by_currency_empy() -> None:
    with pytest.raises(StopIteration):
        usd_transactions = filter_by_currency([], "USD")
        next(usd_transactions)


# Тест в случае, когда транзакции в заданной валюте отсутствуют.
def test_canceled_empty() -> None:
    with pytest.raises(StopIteration):
        usd_transactions = filter_by_currency(
            [
                {
                    "id": 939719570,
                    "state": "EXECUTED",
                    "date": "2018-06-30T02:08:58.425572",
                    "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": ""}},
                    "description": "Перевод организации",
                    "from": "Счет 75106830613657916952",
                    "to": "Счет 11776614605963066702",
                },
                {
                    "id": 142264268,
                    "state": "EXECUTED",
                    "date": "2019-04-04T23:20:05.206878",
                    "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": ""}},
                    "description": "Перевод со счета на счет",
                    "from": "Счет 19708645243227258542",
                    "to": "Счет 75651667383060284188",
                },
            ],
            "USD",
        )
        next(usd_transactions)


""" Тесты функции filter_by_currency. """


# Проверка, что функция возвращает корректные описания для каждой транзакции.
def test_transaction_descriptions(transactions: list) -> None:
    generator = transaction_descriptions(transactions)
    assert next(generator) == "Перевод организации"
    assert next(generator) == "Перевод со счета на счет"


# Тест с различным количеством входных транзакций, включая пустой список.
def test_transaction_descriptions_one() -> None:
    with pytest.raises(StopIteration):
        expected_transactions = transaction_descriptions(
            [
                {
                    "id": 939719570,
                    "state": "EXECUTED",
                    "date": "2018-06-30T02:08:58.425572",
                    "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
                    "description": "Перевод организации",
                    "from": "Счет 75106830613657916952",
                    "to": "Счет 11776614605963066702",
                },
            ]
        )
        next(expected_transactions)
        next(expected_transactions)


def test_transaction_descriptions_empy() -> None:
    with pytest.raises(StopIteration):
        expected_transactions = transaction_descriptions([])
        next(expected_transactions)


""" Тестирование генератора card_number_generator. """


# Тест на то, что генератор выдает правильные номера карт в заданном диапазоне.
def test_card_number_generator() -> None:
    num_generator = card_number_generator(1, 5)
    assert next(num_generator) == "0000 0000 0000 0001"
    assert next(num_generator) == "0000 0000 0000 0002"
    assert next(num_generator) == "0000 0000 0000 0003"
    assert next(num_generator) == "0000 0000 0000 0004"
    assert next(num_generator) == "0000 0000 0000 0005"


# Проверка корректности форматирования номеров карт.
def test_card_number_format() -> None:
    card_number = "0000 0000 0000 0001"
    pattern = r"^\d{4} \d{4} \d{4} \d{4}$"
    assert re.match(pattern, card_number), "Формат номера карты неверный"


# Проверка что, генератор корректно обрабатывает крайние значения диапазона и правильно завершает генерацию.
def test_extreme_values() -> None:
    assert next(card_number_generator(1, 1)) == "0000 0000 0000 0001"


def test_generation_completion() -> None:
    with pytest.raises(StopIteration):
        num_generator = card_number_generator(9999999999999999, 99999999999999999)
        next(num_generator)
