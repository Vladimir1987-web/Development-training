from datetime import datetime
from typing import Union

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(card_or_account_number: Union[str]) -> str:
    """
    Обрабатывает информацию как о картах, так и о счетах
    :param card_or_account_number:
    :return:
    """

    if card_or_account_number == "":
        raise ValueError("Введите номер карты или счета!")

    name = ""
    value_number = ""
    for i in card_or_account_number:
        if i.isalpha():
            name += i
        elif i.isdigit():
            value_number += i

    if "счет" in name.lower():
        str_mask_account = get_mask_account(value_number)
        return f"{name} {str_mask_account}"
    else:
        str_mask_number = get_mask_card_number(value_number)
        return f"{name} {str_mask_number}"


def get_date(info_date: Union[str]) -> str:
    """
    Принимает на вход строку с датой в формате "2024-03-11T02:26:18.671407"
    и возвращает строку с датой в формате "ДД.ММ.ГГГГ" ("11.03.2024")
    :param info_date:
    :return:
    """

    if info_date == "":
        raise ValueError("Нет даты!")

    if info_date[:4].isdigit():
        if info_date[4] == "-":
            date_object_d_m_Y = datetime.strptime(info_date[:10], "%Y-%m-%d").strftime("%d.%m.%Y")
        elif info_date[4] == "/":
            date_object_d_m_Y = datetime.strptime(info_date[:10], "%Y/%m/%d").strftime("%d.%m.%Y")
    else:
        if info_date[2] == "-":
            date_object_d_m_Y = datetime.strptime(info_date[:10], "%d-%m-%Y").strftime("%d.%m.%Y")
        elif info_date[2] == "/":
            date_object_d_m_Y = datetime.strptime(info_date[:10], "%m/%d/%Y").strftime("%d.%m.%Y")

    return date_object_d_m_Y


if __name__ in "__main__":
    print(mask_account_card("Счет 64686473678894779589"))
    print(get_date("03/11/2024"))
