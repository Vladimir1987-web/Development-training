from typing import Any

import pytest
from pytest import FixtureRequest

from src.processing import filter_by_state, sort_by_date

""" Функция filter_by_state """


@pytest.fixture()
def data_for_canceled_empty() -> list[dict[str, Any]]:
    return [
        {"id": 594226727, "state": "CANCEL", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "", "date": "2018-10-14T08:21:33.419441"},
    ]


@pytest.fixture()
def input_data_state() -> list[dict[str, Any]]:
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


@pytest.fixture()
def data_for_executed() -> list[dict[str, Any]]:
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]


@pytest.fixture()
def data_for_canceled() -> list[dict[str, Any]]:
    return [
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


def test_filter_by_state(input_data_state: list[dict[str, Any]], data_for_executed: list[dict[str, Any]]) -> None:
    assert filter_by_state(input_data_state) == data_for_executed


def test_empty_filter_by_state(data_for_canceled_empty: list[dict[str, Any]]) -> None:
    assert filter_by_state(data_for_canceled_empty) == []


@pytest.mark.parametrize(
    "state, expected_fixture", [("EXECUTED", "data_for_executed"), ("CANCELED", "data_for_canceled")]
)
def test_filter_by_state_for_state(
    input_data_state: list[dict[str, Any]], state: str, expected_fixture: str, request: FixtureRequest
) -> None:
    expected = request.getfixturevalue(expected_fixture)
    assert filter_by_state(input_data_state, state) == expected


""" Функция sort_by_date """


@pytest.fixture()
def data_for_ascending() -> list[dict[str, Any]]:
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]


@pytest.fixture()
def data_for_decreasing() -> list[dict[str, Any]]:
    return [
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    ]


@pytest.fixture()
def data_for_one_date() -> list[dict[str, Any]]:
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 594226727, "state": "CANCELED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 615064591, "state": "CANCELED", "date": "2019-07-03T18:35:29.512364"},
    ]


@pytest.fixture()
def data_for_date() -> list[str]:
    return [
        "",
        "3.7.19",
        "2019/07/03T18:35:29.512364",
        "03-07-2019T18:35:29.512364",
        "07/03/2019",
        "20190703",
    ]


@pytest.fixture()
def data_for_non_standard(data_for_date: list[str]) -> list[dict[str, Any]]:
    return [
        {"id": 41428829, "state": "EXECUTED", "date": data_for_date[2]},
        {"id": 939719570, "state": "EXECUTED", "date": data_for_date[3]},
        {"id": 939719570, "state": "EXECUTED", "date": data_for_date[4]},
    ]


# Тестирование сортировки списка словарей по датам в порядке убывания и возрастания.
@pytest.mark.parametrize(
    "bool_value, ascending_or_decreasing", [(True, "data_for_ascending"), (False, "data_for_decreasing")]
)
def test_sort_by_date_ascending_or_decreasing(
    input_data_state: list[dict[str, Any]], bool_value: bool, ascending_or_decreasing: str, request: FixtureRequest
) -> None:
    expected = request.getfixturevalue(ascending_or_decreasing)
    where_sorted = sorted(sort_by_date(input_data_state), key=lambda item: item["date"], reverse=bool_value)
    assert where_sorted == expected


# Проверка корректности сортировки при одинаковых датах.
def test_sort_by_one_date(data_for_one_date: list[dict[str, Any]]) -> None:
    assert sort_by_date(data_for_one_date) == data_for_one_date


# Тесты на работу функции с некорректными форматами дат.
def test_sort_by_date_incorrect(data_for_date: list[str]) -> None:
    with pytest.raises(ValueError):
        sort_by_date(
            [
                {"id": 41428829, "state": "EXECUTED", "date": data_for_date[0]},
                {"id": 939719570, "state": "EXECUTED", "date": data_for_date[1]},
                {"id": 939719570, "state": "EXECUTED", "date": data_for_date[5]},
            ]
        )


# Тесты на работу функции с нестандартными форматами дат.
@pytest.mark.parametrize(
    "expected",
    [
        [
            {"id": 41428829, "state": "EXECUTED", "date": "2019/07/03T18:35:29.512364"},
            {"id": 939719570, "state": "EXECUTED", "date": "2019-07-03"},
            {"id": 939719570, "state": "EXECUTED", "date": "2019-07-03"},
        ]
    ],
)
def test_sort_by_date_non_standard(
        data_for_non_standard: list[dict[str, Any]], expected: list[dict[str, Any]]
) -> None:
    assert sort_by_date(data_for_non_standard) == expected
