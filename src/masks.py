import logging
from typing import Union

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename=r"C:\Training\Python-development\Project\pythonProjectBank\logs\masks.log",
    encoding="utf-8",  # Запись логов в файл
    filemode="w",
)
app_logger = logging.getLogger("masks.py")


def get_mask_card_number(card_number: Union[str, int]) -> str:
    """
    Принимает на вход номер карты и возвращает ее маску
    """
    app_logger.info("Принятие на вход номера карты.")
    if not isinstance(card_number, (int | str)):
        app_logger.error("Ошибка типа данных.")
        raise TypeError("Ошибка типа данных")
    # Переводим числа в строку и убираем пробелы в номере карты
    str_card_number = str(card_number)
    number_card = str_card_number.replace(" ", "")

    if len(number_card) != 16:
        app_logger.error("Неверная длина номера карты!")
        raise ValueError("Неверная длина номера карты!")

    if not number_card.isdigit():
        app_logger.error("Недопустимые символы в номере карты!")
        raise ValueError("Недопустимые символы в номере карты!")

    # Вставляем пробелы после каждой четвёртой цифры
    mask_cart = " ".join(number_card[i : i + 4] for i in range(0, len(number_card), 4))
    # Переводим строку в список
    mask_cart_list = list(mask_cart)

    # Делаем маску номера карты
    for i in range(len(mask_cart_list)):
        if 7 <= i <= 13 and mask_cart_list[i] != " ":
            mask_cart_list[i] = "*"
    mask_card_number = "".join(mask_cart_list)

    app_logger.info("Вывод маски номера карты.")
    return mask_card_number


def get_mask_account(number_cart: Union[str, int]) -> str:
    """
    Принимает на вход номер счета и возвращает его маску
    :param number_cart:
    :return:
    """
    app_logger.info("Принятие на вход номера счета.")
    if not isinstance(number_cart, (int | str)):
        app_logger.error("Ошибка типа данных.")
        raise TypeError("Ошибка типа данных")

    # Переводим числа в строку и убираем пробелы в номере счёта
    cart_str = str(number_cart)
    number_cart = cart_str.replace(" ", "")

    if not number_cart.isdigit():
        app_logger.error("Недопустимые символы в номере карты!")
        raise ValueError("Недопустимые символы в номере карты!")

    if len(number_cart) != 20:
        app_logger.error("Неверная длина номера карты!")
        raise ValueError("Неверная длина номера карты!")

    # Делаем маску номера счёта
    number_mask = str(number_cart[-4:])
    app_logger.info("Вывод маски номера счёта.")
    return f"**{number_mask}"


if __name__ == "__main__":
    print(get_mask_card_number("1234567812345678"))
    print(get_mask_account(73654108430135874305))
