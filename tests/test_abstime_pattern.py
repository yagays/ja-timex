import pytest

from ja_timex.tagger.abstime_pattern import Place


@pytest.fixture(scope="module")
def place():
    return Place()


# ここでは値の正しさのみを検証する
# 日付表現としてのバリエーションや正しさはtaggerの方で行う


def test_place_year(place):
    assert place.is_valid("year", "2021")
    assert place.is_valid("year", "1")

    # 日付表現としての10000年は、現時点で現実世界を表現する際に使うことはない
    assert not place.is_valid("year", "10000")


def test_palce_month(place):
    assert place.is_valid("month", "1")
    assert place.is_valid("month", "01")
    assert place.is_valid("month", "12")

    assert not place.is_valid("month", "13")
    assert not place.is_valid("month", "100")


def test_place_day(place):
    assert place.is_valid("day", "1")
    assert place.is_valid("day", "01")
    assert place.is_valid("day", "31")

    assert not place.is_valid("day", "32")
    assert not place.is_valid("day", "001")
    assert not place.is_valid("day", "100")


def test_place_weekday(place):
    assert place.is_valid("weekday", "月")
    assert place.is_valid("weekday", "火")
    assert place.is_valid("weekday", "水")
    assert place.is_valid("weekday", "木")
    assert place.is_valid("weekday", "金")
    assert place.is_valid("weekday", "土")
    assert place.is_valid("weekday", "日")

    assert not place.is_valid("weekday", "月火")


def test_place_weekday_with_suffix(place):
    assert not place.is_valid("weekday", "月曜日")

    assert place.is_valid("weekday_with_suffix", "月曜日")
    assert place.is_valid("weekday_with_suffix", "月曜")
    assert place.is_valid("weekday_with_suffix", "月")
    assert place.is_valid("weekday_with_suffix", "日")


def test_place_weekday_with_symbol(place):
    assert not place.is_valid("weekday", "(月曜日)")
    assert not place.is_valid("weekday_with_suffix", "(月曜日)")

    assert place.is_valid("weekday_with_symbol", "(月曜日)")
    assert place.is_valid("weekday_with_symbol", "(月曜)")
    assert place.is_valid("weekday_with_symbol", "(月)")
    assert place.is_valid("weekday_with_symbol", "(日)")


def test_place_season(place):
    assert place.is_valid("season", "春")
    assert place.is_valid("season", "夏")
    assert place.is_valid("season", "秋")
    assert place.is_valid("season", "冬")

    assert not place.is_valid("season", "春夏秋冬")
    assert not place.is_valid("season", "季節")


def test_place_quarter(place):
    assert place.is_valid("quarter", "1")
    assert place.is_valid("quarter", "2")
    assert place.is_valid("quarter", "3")
    assert place.is_valid("quarter", "4")

    assert not place.is_valid("quarter", "5")
    assert not place.is_valid("quarter", "11")
