from unittest.mock import patch

import pytest
import pandas as pd

from src.reading_trans import reading_cvs, reading_excel


@pytest.fixture
def two_transactions() -> list:
    return [
        {
            'id': 650703.0, 'state': 'EXECUTED', 'date': '2023-09-05T11:30:32Z', 'amount': 16210.0,
            'currency_name': 'Sol', 'currency_code': 'PEN', 'from': 'Счет 58803664561298323391',
            'to': 'Счет 39745660563456619397', 'description': 'Перевод организации'
        },
        {
            'id': 3598919.0, 'state': 'EXECUTED', 'date': '2020-12-06T23:00:58Z', 'amount': 29740.0,
            'currency_name': 'Peso', 'currency_code': 'COP', 'from': 'Discover 3172601889670065',
            'to': 'Discover 0720428384694643', 'description': 'Перевод с карты на карту'
        }
    ]


''' Тест функции reading_cvs '''
# Проверка правильности работы функции
@patch('pandas.read_csv')
def test_reading_cvs(mock_get, two_transactions) -> None:
    mock_get.return_value = pd.DataFrame(two_transactions)
    data_csv = "transactions.csv"
    assert reading_cvs(data_csv) == two_transactions


# Если файл CSV не найден
def test_reading_not_cvs() -> None:
    data_csv = "t.csv"
    assert reading_cvs(data_csv) == []


# Если pandas.read_csv возвращает не DataFrame
@patch('pandas.read_csv')
def test_reading_cvs_empy(mock_get, two_transactions) -> None:
    mock_get.return_value = two_transactions
    data_csv = "transactions.csv"
    assert reading_cvs(data_csv) == []


''' Тест функции reading_excel '''
# Проверка правильности работы функции
@patch('pandas.read_excel')
def test_reading_excel(mock_get, two_transactions) -> None:
    mock_get.return_value = pd.DataFrame(two_transactions)
    data_csv = "transactions.excel.xlsx"
    assert reading_excel(data_csv) == two_transactions


# Если файл excel не найден
def test_reading_not_excel() -> None:
    data_csv = "t.excel"
    assert reading_excel(data_csv) == []


# Если pandas.read_csv возвращает не DataFrame
@patch('pandas.read_excel')
def test_reading_excel_empy(mock_get, two_transactions) -> None:
    mock_get.return_value = two_transactions
    data_csv = "transactions.excel"
    assert reading_excel(data_csv) == []
