import pytest

from ja_timex.tagger.duration_pattern import DurationPlace


@pytest.fixture(scope="module")
def place():
    return DurationPlace()


# ここでは値の正しさのみを検証する
# 日付表現としてのバリエーションや正しさはtaggerの方で行う


def test_place_year(place):
    # same as test_abstime_pattern.py
    assert place.is_valid("year", "2021")
    assert place.is_valid("year", "1")

    assert not place.is_valid("year", "10000")


def test_palce_month(place):
    assert place.is_valid("month", "1")
    assert place.is_valid("month", "01")
    assert place.is_valid("month", "12")
    assert place.is_valid("month", "13")
    assert place.is_valid("month", "100")

    assert not place.is_valid("month", "-1")


def test_place_day(place):
    # same as test_abstime_pattern.py
    assert place.is_valid("day", "1")
    assert place.is_valid("day", "01")
    assert place.is_valid("day", "31")

    assert not place.is_valid("day", "32")
    assert not place.is_valid("day", "001")
    assert not place.is_valid("day", "100")


def test_place_century(place):
    assert place.is_valid("century", "21")
    assert place.is_valid("century", "1")
    assert place.is_valid("century", "01")

    # 「0世紀」自体は概念としては存在しないが、記載自体は可能
    assert place.is_valid("century", "0")


def test_place_week(place):
    assert place.is_valid("week", "1")
    assert place.is_valid("week", "52")
    assert place.is_valid("week", "0.5")
    assert place.is_valid("week", "1.5")


def test_place_hour(place):
    assert place.is_valid("hour", "1")
    assert place.is_valid("hour", "24")
    assert place.is_valid("hour", "128")
    assert place.is_valid("hour", "0.5")
    assert place.is_valid("hour", "1.5")


def test_place_minutes(place):
    assert place.is_valid("minutes", "1")
    assert place.is_valid("minutes", "60")
    assert place.is_valid("minutes", "180")
    assert place.is_valid("minutes", "0.5")
    assert place.is_valid("minutes", "1.5")


def test_place_second(place):
    assert place.is_valid("second", "1")
    assert place.is_valid("second", "60")
    assert place.is_valid("second", "120")
    assert place.is_valid("second", "0.5")
    assert place.is_valid("second", "1.5")
