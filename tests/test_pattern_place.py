import pytest

from ja_timex.pattern.place import Place


@pytest.fixture(scope="module")
def place():
    return Place()


# ここでは値の正しさのみを検証する
# 日付表現としてのバリエーションや正しさはtaggerの方で行う


def test_place_calendar_year(place):
    assert place.is_valid("calendar_year", "2021")
    assert place.is_valid("calendar_year", "1")

    # 日付表現としての10000年は、現時点で現実世界を表現する際に使うことはない
    assert not place.is_valid("calendar_year", "10000")


def test_palce_calendar_month(place):
    assert place.is_valid("calendar_month", "1")
    assert place.is_valid("calendar_month", "01")
    assert place.is_valid("calendar_month", "12")

    assert not place.is_valid("calendar_month", "13")
    assert not place.is_valid("calendar_month", "100")


def test_place_calendar_day(place):
    assert place.is_valid("calendar_day", "1")
    assert place.is_valid("calendar_day", "01")
    assert place.is_valid("calendar_day", "31")

    assert not place.is_valid("calendar_day", "32")
    assert not place.is_valid("calendar_day", "001")
    assert not place.is_valid("calendar_day", "100")


def test_place_weekday(place):
    assert place.is_valid("weekday", "月")
    assert place.is_valid("weekday", "火")
    assert place.is_valid("weekday", "水")
    assert place.is_valid("weekday", "木")
    assert place.is_valid("weekday", "金")
    assert place.is_valid("weekday", "土")
    assert place.is_valid("weekday", "日")

    assert not place.is_valid("weekday", "月火")


def test_place_weekday_without_symbol(place):
    assert not place.is_valid("weekday", "月曜日")

    assert place.is_valid("weekday_without_symbol", "月曜日")
    assert place.is_valid("weekday_without_symbol", "月曜")
    assert not place.is_valid("weekday_without_symbol", "月")
    assert not place.is_valid("weekday_without_symbol", "日")


def test_place_weekday_with_symbol(place):
    assert not place.is_valid("weekday", "(月曜日)")
    assert not place.is_valid("weekday_without_symbol", "(月曜日)")

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


# 期間
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
    assert place.is_valid("day", "100")


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


def test_place_minute(place):
    assert place.is_valid("minute", "1")
    assert place.is_valid("minute", "60")
    assert place.is_valid("minute", "180")
    assert place.is_valid("minute", "0.5")
    assert place.is_valid("minute", "1.5")


def test_place_second(place):
    assert place.is_valid("second", "1")
    assert place.is_valid("second", "60")
    assert place.is_valid("second", "120")
    assert place.is_valid("second", "0.5")
    assert place.is_valid("second", "1.5")


def test_place_second_with_ms(place):
    assert place.is_valid("second_with_ms", "1秒05")
    assert place.is_valid("second_with_ms", "100秒5")
    assert place.is_valid("second_with_ms", "1秒0")


# reltime
def test_place_around_prefix(place):
    assert place.is_valid("around_suffix", "くらい")
    assert place.is_valid("around_suffix", "ぐらい")
    assert place.is_valid("around_suffix", "より")
    assert place.is_valid("around_suffix", "よりも")

    assert not place.is_valid("around_suffix", "くぐらい")
    assert not place.is_valid("around_suffix", "ほど程度")


# duration
def test_place_count(place):
    assert place.is_valid("count", "1")  # 1回
    assert place.is_valid("count", "1.5")
    assert place.is_valid("count", "0.05")


def test_place_year_range(place):
    assert place.is_valid("year_range", "1")  # 1年
    assert place.is_valid("year_range", "1.5")
    assert place.is_valid("year_range", "0.05")

    # 暦とは異なり表現可能
    assert place.is_valid("year_range", "10000")


def test_place_month_range(place):
    assert place.is_valid("month_range", "1")  # 1ヶ月
    assert place.is_valid("month_range", "1.5")
    assert place.is_valid("month_range", "0.05")

    # 暦とは異なり表現可能
    assert place.is_valid("month_range", "13")
    assert place.is_valid("month_range", "100")


def test_place_day_range(place):
    assert place.is_valid("day_range", "1")  # 1日
    assert place.is_valid("day_range", "1.5")
    assert place.is_valid("day_range", "0.05")

    # 暦とは異なり表現可能
    assert place.is_valid("day_range", "32")
    assert place.is_valid("day_range", "100")


def test_times_of_day_prefix(place):
    assert place.is_valid("morning_prefix", "朝")
    assert place.is_valid("morning_prefix", "今朝")
    assert place.is_valid("evening_prefix", "今夜")
    assert place.is_valid("evening_prefix", "今晩")

    assert place.is_valid("midnight_prefix", "深夜")


def test_ampm_prefix_suffix(place):
    # スペースのみは許容しない
    assert not place.is_valid("ampm_suffix", " ")
    assert not place.is_valid("ampm_suffix", "　")
