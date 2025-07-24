import numpy as np

from src.processing import filter_by_state, sort_by_date
from src.reading_trans import reading_cvs, reading_excel
from src.regular_expressions import process_bank_search
from src.utils import funk_data_transactions
from src.widget import get_date, mask_account_card

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


def main(filter_trans: list) -> None:
    """
    Функция main отвечает за основную логику проекта и связывает функциональности между собой.
    :return: Выводит итоговый список транзакций
    """

    for operation in filter_trans:
        print(f'{get_date(operation['date'])} {operation['description']}')
        if 'from' not in operation or not isinstance(operation['from'], (int, float)) or np.isnan(operation['from']):
            print(f'{mask_account_card(operation['to'])}')
        else:
            print(f'{mask_account_card(operation['from'])} -> {mask_account_card(operation['to'])}')
        if answer_user_file == 1:
            print(f'{operation['operationAmount']['amount']} {operation['operationAmount']['currency']['name']}')
        elif answer_user_file == 2 or answer_user_file == 3:
            print(f'{operation['amount']} {operation['currency_name']}')


# Приветствие пользователя
print('Привет! Добро пожаловать в программу работы с банковскими транзакциями.')

list_file = []

valid_num = {1, 2, 3}
answer_user_file = 0

while answer_user_file not in valid_num:
    answer_user_file = int(input('Выберите необходимый пункт меню:'
                                 '\n1. Получить информацию о транзакциях из JSON-файла'
                                 '\n2. Получить информацию о транзакциях из CSV-файла'
                                 '\n3. Получить информацию о транзакциях из XLSX-файла'
                                 '\nВведите число: '))
    if answer_user_file not in valid_num:
        print("Неверное число.")
    elif answer_user_file == 1:
        print("Для обработки выбран JSON-файл.")
        list_file = list_json_file
    elif answer_user_file == 2:
        print("Для обработки выбран CSV-файл.")
        list_file = list_csv_file
    elif answer_user_file == 3:
        print("Для обработки выбран XLSX-файл.")
        list_file = list_excel_file

# Выбор статуса операции
print('Введите статус, по которому необходимо выполнить фильтрацию.\n'
      'Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING')
valid_statuses = {"EXECUTED", "CANCELED", "PENDING"}
status = ''
while status not in valid_statuses:
    status = input(
        "Введите статус, по которому необходимо выполнить фильтрацию. Доступные для фильтровки статусы:\n"
        "EXECUTED, CANCELED, PENDING\n")
    status = status.upper()  # Приводим к единому регистру
    if status not in valid_statuses:
        print(f"Статус операции \"{status}\" недоступен.")
    else:
        print(f"Операции отфильтрованы по статусу {status}")
        list_file_status = filter_by_state(list_file, status)
    print(list_file_status)

# уточнение выборки операций
print('Отсортировать операции по дате? Да/Нет')
user_answer_date = {'ДА', 'НЕТ'}
user_sort_date = ''
while user_sort_date not in user_answer_date:
    user_sort_date = input("Введите ответ: да или нет: ").upper()
    if user_sort_date not in user_answer_date:
        print('Введите корректный ответ')
    else:
        if user_sort_date == 'ДА':
            list_sort_date = sort_by_date(list_file_status)
            print('Отсортировать по возрастанию или по убыванию?')
            user_answer_sort = {'по возрастанию', 'по убыванию'}
            user_sort = ''
            while user_sort not in user_answer_sort:
                user_sort = input("По возрастанию или по убыванию: ").lower()
                if user_sort not in user_answer_sort:
                    print('Введите корректный ответ')
                else:
                    if user_sort == 'по убыванию':
                        list_sort_date = sort_by_date(list_file_status)
                    elif user_sort == 'по возрастанию':
                        list_sort_date = sorted(list_sort_date, key=lambda item: item["date"], reverse=False)
        elif user_sort_date == 'НЕТ':
            list_sort_date = list_file_status
        print(list_sort_date)

print('Выводить только рублевые транзакции? Да/Нет')
user_answer_rub = {'ДА', 'НЕТ'}
user_sort_rub = ''
while user_sort_rub not in user_answer_rub:
    user_sort_rub = input("Введите ответ: да или нет: ").upper()
    if user_sort_rub not in user_answer_rub:
        print('Введите корректный ответ')
    else:
        if user_sort_rub == 'ДА':
            if answer_user_file == 1:
                filtered_transactions = [x for x in list_sort_date if
                                         x["operationAmount"]["currency"]["code"] == 'RUB']
            elif answer_user_file == 2 or answer_user_file == 3:
                filtered_transactions = [x for x in list_sort_date if
                                         x["currency_code"] == 'RUB']
        elif user_sort_rub == 'НЕТ':
            filtered_transactions = list_sort_date
    print(filtered_transactions)

print('Отфильтровать список транзакций по определенному слову в описании? Да/Нет')
user_answer_description = {'ДА', 'НЕТ'}
user_sort_description = ''
while user_sort_description not in user_answer_description:
    user_sort_description = input("Введите ответ: да или нет: ").upper()
    if user_sort_description not in user_answer_description:
        print('Введите корректный ответ')
    else:
        if user_sort_description == 'ДА':
            filter_trans = process_bank_search(filtered_transactions, "Открытие")
        elif user_sort_description == 'НЕТ':
            filter_trans = filtered_transactions

if filter_trans == []:
    print('Не найдено ни одной транзакции, подходящей под ваши условия фильтрации')
else:
    print(f'Распечатываю итоговый список транзакций...\n {filter_trans}')

print(f'Всего банковских операций в выборке: {len(filter_trans)}')

main(filter_trans)
