import pandas as pd


def reading_cvs(way_cvs: str) -> list:
    """
    Считывает финансовые операции из CSV и возвращает список словарей с транзакциями.
    :param way:
    :return:
    """
    try:
        df_csv = pd.read_csv(way_cvs, sep=";")
        transactions_csv_list = df_csv.to_dict(orient="records")
        return transactions_csv_list
    except FileNotFoundError:
        print(f"Ошибка: Файл {way_cvs} не найден.")
        return []
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return []


def reading_excel(way_excel: str) -> list:
    """
    Считывает финансовые операции из Excel и возвращает список словарей с транзакциями.
    :param way:
    :return:
    """
    try:
        df_excel = pd.read_excel(way_excel)
        transactions_excel_list = df_excel.to_dict(orient="records")
        return transactions_excel_list
    except FileNotFoundError:
        print(f"Ошибка: Файл {way_excel} не найден.")
        return []
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return []


if __name__ == "__main__":
    print(reading_cvs("transactions.csv"))
    print(reading_excel("transactions_excel.xlsx"))
