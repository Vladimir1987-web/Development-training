import json


def funk_data_transactions(way: str) -> list[dict]:
    """Принимает на вход путь до JSON-файла и возвращает список словарей с данными о финансовых транзакциях"""
    try:
        with open(way, encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                return []
            if type(data) is not list:
                return []
        return data
    except FileNotFoundError:
        return []


if __name__ == '__main__':
    print(funk_data_transactions(r'C:\Training\Python-development\Project\pythonProjectBank\data\operations.json'))
