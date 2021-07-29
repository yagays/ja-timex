import pytest

from ja_timex.tagger.reltime_tagger import ReltimeTagger


@pytest.fixture(scope="module")
def t():
    return ReltimeTagger()


def test_year(t):
    assert t.parse("1年前").value == "P1Y"
    assert t.parse("1年くらい前").value == "P1Y"
    assert t.parse("1年ぐらい前").value == "P1Y"
    assert t.parse("1年ほど前").value == "P1Y"
    assert t.parse("1年ばかり前").value == "P1Y"
    assert t.parse("1年近くまえ").value == "P1Y"

    assert t.parse("100年前").value == "P100Y"


def test_year_mod_about_prefix_and_suffix(t):
    assert t.parse("1年前").mod == "BEFORE"
    assert t.parse("1年後").mod == "AFTER"
    assert t.parse("1年近く").mod == "APPROX"
    assert t.parse("1年前後").mod == "APPROX"
    assert t.parse("1年くらい").mod == "APPROX"
    assert t.parse("1年ばかり").mod == "APPROX"


def test_month_mod_about_prefix_and_suffix(t):
    assert t.parse("1ヶ月前").mod == "BEFORE"
    assert t.parse("1ヶ月後").mod == "AFTER"
    assert t.parse("1ヶ月近く").mod == "APPROX"
    assert t.parse("1ヶ月前後").mod == "APPROX"
    assert t.parse("1ヶ月くらい").mod == "APPROX"
    assert t.parse("1ヶ月ばかり").mod == "APPROX"


def test_day_mod_about_prefix_and_suffix(t):
    assert t.parse("1日前").mod == "BEFORE"
    assert t.parse("1日後").mod == "AFTER"
    assert t.parse("1日近く").mod == "APPROX"
    assert t.parse("1日前後").mod == "APPROX"
    assert t.parse("1日くらい").mod == "APPROX"
    assert t.parse("1日ばかり").mod == "APPROX"


def test_ac_century_mod_about_prefix_and_suffix(t):
    assert t.parse("1世紀前").mod == "BEFORE"
    assert t.parse("1世紀後").mod == "AFTER"
    assert t.parse("1世紀近く").mod == "APPROX"
    assert t.parse("1世紀前後").mod == "APPROX"
    assert t.parse("1世紀くらい").mod == "APPROX"
    assert t.parse("1世紀ばかり").mod == "APPROX"


def test_week_mod_about_prefix_and_suffix(t):
    assert t.parse("1週前").mod == "BEFORE"
    assert t.parse("1週後").mod == "AFTER"
    assert t.parse("1週近く").mod == "APPROX"
    assert t.parse("1週前後").mod == "APPROX"
    assert t.parse("1週くらい").mod == "APPROX"
    assert t.parse("1週ばかり").mod == "APPROX"

    assert t.parse("1週間前").mod == "BEFORE"


def test_hour_mod_about_prefix_and_suffix(t):
    assert t.parse("1時間前").mod == "BEFORE"
    assert t.parse("1時間後").mod == "AFTER"
    assert t.parse("1時間近く").mod == "APPROX"
    assert t.parse("1時間前後").mod == "APPROX"
    assert t.parse("1時間くらい").mod == "APPROX"
    assert t.parse("1時間ばかり").mod == "APPROX"


def test_minutes_mod_about_prefix_and_suffix(t):
    assert t.parse("1分前").mod == "BEFORE"
    assert t.parse("1分後").mod == "AFTER"
    assert t.parse("1分近く").mod == "APPROX"
    assert t.parse("1分前後").mod == "APPROX"
    assert t.parse("1分くらい").mod == "APPROX"
    assert t.parse("1分ばかり").mod == "APPROX"


def test_second_mod_about_prefix_and_suffix(t):
    assert t.parse("1秒前").mod == "BEFORE"
    assert t.parse("1秒後").mod == "AFTER"
    assert t.parse("1秒近く").mod == "APPROX"
    assert t.parse("1秒前後").mod == "APPROX"
    assert t.parse("1秒くらい").mod == "APPROX"
    assert t.parse("1秒ばかり").mod == "APPROX"
