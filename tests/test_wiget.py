from typing import Union

import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "card_or_account_number, expected",
    [
        ("Maestro 7000792289606361", "Maestro 7000 79** **** 6361"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("счет 73654108430135874305", "счет **4305"),
        ("Счет 35383033474447895560", "Счет **5560"),
    ],
)
def test_mask_account_card(card_or_account_number: Union[str], expected: Union[str]) -> None:
    assert mask_account_card(card_or_account_number) == expected


def test_mask_account_card_invalid_number() -> None:
    with pytest.raises(ValueError):
        mask_account_card("")


def test_get_date_empty() -> None:
    with pytest.raises(ValueError):
        get_date("")


@pytest.mark.parametrize(
    "info_date, expected",
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2024/03/11T02:26:18.671407", "11.03.2024"),
        ("03/11/2024", "11.03.2024"),
        ("11-03-2024", "11.03.2024"),
    ],
)
def test_get_date_format_date(info_date: str, expected: str) -> None:
    assert get_date(info_date) == expected
