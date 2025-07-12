# Проект pythonProjectBank
## Описание:
Это проект, который будет готовить данные для отображения в новом виджете,
показывающем несколько последних успешных банковских операций клиента.
## Установка:
1. Клонируйте репозиторий:
```git clone https://github.com/Vladimir1987-web/Development-training.git```
2. Установите зависимости:
```pip install -r requirements.txt```
## Использование:
Данный проект состоит из шести модулей:
1. Модуль mask.py - в нём две функции:
- get_mask_card_number - Принимает на вход номер 
карты и возвращает ее маску
- get_mask_account - Принимает на вход номер 
счета и возвращает его маску
Пример использования:
- print(get_mask_card_number(1234567812345678))
- print(get_mask_account(73654108430135874305))

2. Модуль widget.py - в нём две функции:
- mask_account_card - Обрабатывает информацию как о картах,
так и о счетах
- get_date - Принимает на вход строку с датой в формате 
"2024-03-11T02:26:18.671407"
и возвращает строку с датой в формате "ДД.ММ.ГГГГ" ("11.03.2024").

Пример использования:
- print(mask_account_card("Счет 64686473678894779589"))
- print(get_date("2024-03-11T02:26:18.671407"))

3. Модуль processing.py - в нём две функции:
- filter_by_state - Фильтрует список словарей по значению ключа 
'state'
- sort_by_date - Функция сортировки даты.

Пример использования:
```
print(
        filter_by_state(
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ]
        )
    )

- print(
        sort_by_date(
            [
            {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
            {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
            {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
            {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
            ]
        )
    )
```
4. Модуль generators.py, состоящий из трёх функций:
- filter_by_currency - Фильтрует транзакции по заданному коду валюты и возвращает итератор.
- transaction_descriptions - Принимает список словарей с транзакциями и возвращает описание каждой операции по очереди.
- card_number_generator - Генерирует номера карт в заданном диапазоне.
Пример использования:
```commandline
if __name__ == "__main__":

    usd_transactions = filter_by_currency(transaction, "USD")
    try:
        for _ in range(5):
            print(next(usd_transactions))
    except StopIteration:
        print("Нет транзакций в указанной валюте.")

    descriptions = transaction_descriptions(transaction)
    try:
        for _ in range(6):
            print(next(descriptions))
    except StopIteration:
        print("Нет транзакций больше.")

    try:
        numb_cart_generator = card_number_generator(9999999999999998, 999999999999999999)
        print(next(numb_cart_generator))
        print(next(numb_cart_generator))
        print(next(numb_cart_generator))
        print(next(numb_cart_generator))
    except StopIteration:
        print("Диапазон исчерпан.")

```
5. Модуль decorators.py, который декорирует функцию my_function, логируя результат её выполнения в файл или консоль.
Пример использования:
```commandline
if __name__ == "__main__":
    my_function(1, "2")
```
6. Модуль utils.py, состоящий из двух функций:
- funk_data_transactions - Принимает на вход путь до JSON-файла и возвращает список словарей с данными
о финансовых транзакциях.
- convert_to_rub - Конвертирует сумму транзакции из исходной валюты в рубли по текущему курсу и возвращает сумму транзакции (ключ
amount) в рублях, тип данных float.
Пример использования:
```commandline
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
```

### Тестирование
В пакете tests реализованы шесть модулей для тестирования функций каждого модуля из пакета src:
1) Модуль test_masks.py
2) Модуль test_wiget.py
3) Модуль test_procesing.py
4) Модуль test_generators.py
5) Модуль test_decorators.py
6) Модуль test_utils.py