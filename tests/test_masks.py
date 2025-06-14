import pytest
from src.masks import get_mask_card_number
from src.masks import get_mask_account


@pytest.fixture
def card_numb():
    return 1234567812345678


def test_get_mask_card_number(card_numb):
    assert get_mask_card_number(card_numb) == '1234 56** **** 5678'


@pytest.mark.parametrize('card_number', ['1234 5678 1234 5678*',
                                       '',
                                       123456781234,
                                       12345678123456789])
def test_get_mask_card_number_invalid_card_number(card_number):
    with pytest.raises(ValueError):
        get_mask_card_number(card_number)


def test_typeerror_get_mask_card_number():
    with pytest.raises(TypeError):
        get_mask_card_number([1, 2])


@pytest.fixture
def numb_cart():
    return 73654108430135874305

def test_get_mask_account(numb_cart):
    get_mask_account(numb_cart) == '**4305'


def test_typeerror_def_test_get_mask_account():
    with pytest.raises(TypeError):
        get_mask_account([1, 2])


@pytest.mark.parametrize('cart_number', ['73654108430135874305№',
                                       '',
                                       736541084301358743053,
                                       12345678123456789])
def test_get_mask_account_invalid_number(cart_number):
    with pytest.raises(ValueError):
        get_mask_account(cart_number)
