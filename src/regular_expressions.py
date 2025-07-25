import re
from collections import Counter

from src.reading_trans import reading_cvs, reading_excel
from src.utils import funk_data_transactions

# Создаём переменные со списками словарей, полученных из:
# JSON-файла
wey_json = r"C:\Training\Python-development\Project\pythonProjectBank\data\operations.json"
list_json_file = funk_data_transactions(wey_json)
# CSV
wey_csv = r"C:\Training\Python-development\Project\pythonProjectBank\src\transactions.csv"
list_csv_file = reading_cvs(wey_csv)
# EXCEL
wey_excel = r"C:\Training\Python-development\Project\pythonProjectBank\src\transactions_excel.xlsx"
list_excel_file = reading_excel(wey_excel)


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """Принимает список словарей с данными о банковских операциях и строку поиска,
    а возвращает список словарей, у которых в описании есть данная строка."""
    if search == "":
        raise ValueError("Отсутствует строка поиска")
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    result_new = [
        operation for operation in data if "description" in operation and pattern.search(operation["description"])
    ]

    return result_new


def process_bank_operations(data: list[dict], categories: list) -> dict:
    """Принимает список словарей с данными о банковских операциях и список категорий операций, а возвращает словарь,
    в котором ключи — это названия категорий, а значения — это количество операций в каждой категории."""
    category_count = Counter()
    for transaction in data:
        description = transaction.get("description", "")
        if description in categories:
            category_count[description] += 1

    return dict(category_count)


if __name__ == "__main__":
    print(process_bank_search(list_json_file, "рk"))
    print(
        process_bank_operations(
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
            ],
            ["Перевод организации", "Открытие счёта", "Перевод с карты на карту"],
        )
    )
