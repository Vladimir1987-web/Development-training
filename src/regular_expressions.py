import re
from collections import Counter

from reading_trans import reading_cvs, reading_excel
from utils import funk_data_transactions

# Создаём переменные со списками словарей, полученных из:
# JSON-файла
wey_json = r"C:\Training\Python-development\Project\pythonProjectBank\data\operations.json"
list_json_file = funk_data_transactions(wey_json)
# CSV
wey_csv = "transactions.csv"
list_csv_file = reading_cvs(wey_csv)
# EXCEL
wey_excel = "transactions_excel.xlsx"
list_excel_file = reading_excel(wey_excel)


def list_description(data: list[dict]) -> list:
    my_list = [operation["description"] for operation in data if "description" in operation]

    return my_list


def process_bank_search(data: list[dict], search: str) -> list[dict]:
    """Принимает список словарей с данными о банковских операциях и список категорий операций,
    а возвращает список словарей, у которых в описании есть данная строка."""
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    result_new = [
        operation for operation in data if "description" in operation and pattern.search(operation["description"])
    ]

    return result_new


def process_bank_operations(data: list[dict], categories: list) -> dict:
    """Принимает список словарей с данными о банковских операциях и список категорий операций, а возвращает словарь,
    в котором ключи — это названия категорий, а значения — это количество операций в каждой категории."""
    counted = Counter(categories)
    # Выводим результаты подсчета
    return dict(counted)


if __name__ == "__main__":
    print(process_bank_search(list_json_file, "Открытие"))
    print(process_bank_operations(list_csv_file, list_description(list_excel_file)))
