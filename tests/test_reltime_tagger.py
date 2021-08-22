import pytest

from ja_timex.tagger import ReltimeTagger


@pytest.fixture(scope="module")
def t():
    return ReltimeTagger()


def test_reltime_type(t):
    assert t.parse("1世紀前").type == "DURATION"
    assert t.parse("1年前").type == "DURATION"
    assert t.parse("1ヶ月前").type == "DURATION"
    assert t.parse("1日前").type == "DURATION"
    assert t.parse("1時間前").type == "DURATION"
    assert t.parse("1分前").type == "DURATION"
    assert t.parse("1秒前").type == "DURATION"


def test_year(t):
    assert t.parse("1年前").value == "P1Y"
    assert t.parse("1年くらい前").value == "P1Y"
    assert t.parse("1年ぐらい前").value == "P1Y"
    assert t.parse("1年ほど前").value == "P1Y"
    assert t.parse("1年ばかり前").value == "P1Y"
    assert t.parse("1年近くまえ").value == "P1Y"

    assert t.parse("100年前").value == "P100Y"


def test_decimal(t):
    assert t.parse("0.1年前").value == "P0.1Y"
    assert t.parse("0.1ヶ月前").value == "P0.1M"
    assert t.parse("0.1週前").value == "P0.1W"
    assert t.parse("0.1日前").value == "P0.1D"
    assert t.parse("0.1時間前").value == "PT0.1H"
    assert t.parse("0.1分前").value == "PT0.1M"
    assert t.parse("0.1秒前").value == "PT0.1S"


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


def test_minute_mod_about_prefix_and_suffix(t):
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


def test_word_before_and_after(t):
    assert t.parse("昨日").value == "P1D"
    assert t.parse("昨日").mod == "BEFORE"
    assert t.parse("一昨日").value == "P2D"
    assert t.parse("一昨日").mod == "BEFORE"
    assert t.parse("一昨々日").value == "P3D"
    assert t.parse("一昨昨日").value == "P3D"
    assert t.parse("前日").value == "P1D"
    assert t.parse("先日").value == "P1D"

    assert t.parse("明日").value == "P1D"
    assert t.parse("明日").mod == "AFTER"
    assert t.parse("明後日").value == "P2D"
    assert t.parse("明後日").mod == "AFTER"
    assert t.parse("翌日").value == "P1D"
    assert t.parse("翌々日").value == "P2D"

    assert t.parse("来週").value == "P1W"
    assert t.parse("再来週").value == "P2W"
    assert t.parse("先週").value == "P1W"
    assert t.parse("先々週").value == "P2W"

    assert t.parse("来月").value == "P1M"
    assert t.parse("再来月").value == "P2M"
    assert t.parse("先月").value == "P1M"
    assert t.parse("先々月").value == "P2M"

    assert t.parse("来年").value == "P1Y"
    assert t.parse("再来年").value == "P2Y"
    assert t.parse("おととし").value == "P2Y"
    assert t.parse("一昨年").value == "P2Y"
    # 年に関しては「先」を用いない
    assert not t.parse("先年")
    assert not t.parse("先々年")


def test_word_now(t):
    # 今日か今週かで表現する幅が異なるので、valueの値としてP0{D,W,M,Y}を取ることは表層表現を表すために必要
    assert t.parse("今日").value == "P0D"
    assert t.parse("今日").mod == "NOW"

    assert t.parse("今週").value == "P0W"
    assert t.parse("今週").mod == "NOW"

    assert t.parse("今月").value == "P0M"
    assert t.parse("今月").mod == "NOW"

    assert t.parse("今年").value == "P0Y"
    assert t.parse("今年").mod == "NOW"


def test_half_suffix_reltime(t):
    assert t.parse("1時間半後").value == "PT1.5H"
    assert t.parse("1時間半後").mod == "AFTER"
    assert t.parse("1分半後").value == "PT1.5M"
    assert t.parse("1秒半後").value == "PT1.5S"

    assert t.parse("1年半後").value == "P1.5Y"
    assert t.parse("1ヶ月半後").value == "P1.5M"
    assert t.parse("1週間半後").value == "P1.5W"
    assert t.parse("1週半後").value == "P1.5W"
    assert t.parse("1日半後").value == "P1.5D"

    assert t.parse("1時間半ほど後").value == "PT1.5H"
    assert t.parse("1時間半くらい後").value == "PT1.5H"
    assert t.parse("1時間半近く後").value == "PT1.5H"


def test_half_suffix_reltime_word(t):
    assert t.parse("半年前").value == "P0.5Y"
    assert t.parse("半年前").mod == "BEFORE"
    assert t.parse("半年後").value == "P0.5Y"
    assert t.parse("半年後").mod == "AFTER"

    assert t.parse("半月前").value == "P0.5M"
    assert t.parse("半月前").mod == "BEFORE"
    assert t.parse("半月後").value == "P0.5M"
    assert t.parse("半月後").mod == "AFTER"

    assert t.parse("半日前").value == "P0.5D"
    assert t.parse("半日前").mod == "BEFORE"
    assert t.parse("半日後").value == "P0.5D"
    assert t.parse("半日後").mod == "AFTER"

    assert t.parse("半世紀前").value == "P50Y"
    assert t.parse("半世紀前").mod == "BEFORE"
    assert t.parse("半世紀後").value == "P50Y"
    assert t.parse("半世紀後").mod == "AFTER"

    assert t.parse("四半世紀前").value == "P25Y"
    assert t.parse("四半世紀前").mod == "BEFORE"
    assert t.parse("四半世紀ほど前").value == "P25Y"
    assert t.parse("四半世紀近く前").value == "P25Y"


def test_just_suffix(t):
    assert t.parse("5年目").value == "P5Y"
    assert t.parse("5年目").mod is None

    assert t.parse("3ヶ月目").value == "P3M"
    assert t.parse("8日目").value == "P8D"
    assert t.parse("1世紀目").value == "00XX"
    assert t.parse("3週目").value == "P3W"

    # 時間/分/秒表現に目は使わない
    assert t.parse("1時間目") is None
    assert t.parse("1分目") is None
    assert t.parse("1秒目") is None

    assert t.parse("5年もの間").value == "P5Y"
    assert t.parse("5年もの間").mod is None

    assert t.parse("5年ぶり").value == "P5Y"
    assert t.parse("5年ぶり").mod is None
