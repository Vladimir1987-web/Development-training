import datetime

from masks import get_mask_account, get_mask_card_number


def mask_account_card(card_or_account_number: str) -> str:
    """
    Обрабатывает информацию как о картах, так и о счетах
    :param card_or_account_number:
    :return:
    """
    name = ''
    value_number = ''
    for i in card_or_account_number:
        if i.isalpha():
            name += i
        elif i.isdigit():
            value_number += i

    if 'счет' in name.lower():
        str_mask_account = get_mask_account(value_number)
        return str_mask_account
    else:
        str_mask_number = get_mask_card_number(value_number)
        return str_mask_number


def get_date(info_date: str) -> str:
    """
    Принимает на вход строку с датой в формате "2024-03-11T02:26:18.671407"
    и возвращает строку с датой в формате "ДД.ММ.ГГГГ" ("11.03.2024")
    :param info_date:
    :return:
    """
    return f'{info_date[8:10]}.{info_date[5:7]}.{info_date[0:4]}'


if __name__ in '__main__':
    print(mask_account_card('Счет 64686473678894779589'))
    print(get_date('2024-03-11T02:26:18.671407'))