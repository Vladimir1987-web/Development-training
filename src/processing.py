from datetime import datetime
from typing import Any


def filter_by_state(operation_list: list[dict[str, Any]], state: str = "EXECUTED") -> list[dict[str, Any]]:
    """
    Фильтрует список словарей по значению ключа 'state'
    """
    return list((transaction for transaction in operation_list if transaction.get("state") == state))


def sort_by_date(operation_list: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Функция сортировки даты"""
    for data_list in operation_list:
        if data_list['date'] == '':
            raise ValueError('Нет даты!')
        elif data_list['date'][4] == '-' or data_list['date'][4] == '/':
            pass
        elif data_list['date'][2] == '-':
            date_object_Y_m_d = datetime.strptime(data_list['date'][:10],
                                                  "%d-%m-%Y").strftime("%Y-%m-%d")
            data_list['date'] = date_object_Y_m_d
        elif data_list['date'][2] == '/':
            date_object_Y_m_d = datetime.strptime(data_list['date'][:10],
                                                  "%m/%d/%Y").strftime("%Y-%m-%d")
            data_list['date'] = date_object_Y_m_d
        else:
            raise ValueError('Не верный формат даты!')

    return sorted(operation_list, key=lambda item: item['date'], reverse=True)


if __name__ in "__main__":
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

    print(
        sort_by_date(
            [
                {'id': 41428829, 'state': 'EXECUTED', 'date': '2019/07/03T18:35:29.512364'},
                {'id': 939719570, 'state': 'EXECUTED', 'date': '03-07-2019T18:35:29.512364'},
                {'id': 939719570, 'state': 'EXECUTED', 'date': "07/03/2019"}
            ]
        )
    )
