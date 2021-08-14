import pytest

from ja_timex.tag import TIMEX
from ja_timex.timex import TimexParser


@pytest.fixture(scope="module")
def p():
    return TimexParser()


def test_abstime(p):
    timexes = p.parse("2021年7月18日")
    assert len(timexes) == 1
    assert type(timexes[0]) == TIMEX
    assert timexes[0].value == "2021-07-18"

    timexes = p.parse("2021回目の7月18日")
    assert len(timexes) == 1
    assert type(timexes[0]) == TIMEX
    assert timexes[0].value == "XXXX-07-18"


def test_tid_is_modified_in_parsing(p):
    timexes = p.parse("彼は2008年4月から週に3回ジョギングを1時間行ってきた")

    assert timexes[0].tid == "t0"
    assert timexes[1].tid == "t1"
    assert timexes[2].tid == "t2"


def test_ignore_number_normalize(p):
    # 一を1と変換しない。可読性のために、reltimeのPatternでも漢数字で扱う
    timexes = p.parse("一昨年と一昨日は言うのに一昨月とは言わないのは何故か")

    assert len(timexes) == 2
    assert timexes[0].value == "P2Y"
    assert timexes[1].value == "P2D"

    timexes = p.parse("一昨昨日と一昨々日")
    assert len(timexes) == 2
    assert timexes[0].value == "P3D"
    assert timexes[1].value == "P3D"


def test_every_year_and_month(p):
    timexes = p.parse("毎年6月から8月にかけて")

    assert len(timexes) == 3
    assert timexes[0].value == "P1Y"
    assert timexes[0].type == "SET"
    assert timexes[1].value == "XXXX-06-XX"
    assert timexes[1].type == "DATE"
    assert timexes[2].value == "XXXX-08-XX"
    assert timexes[2].type == "DATE"


def test_morning_evening(p):
    timexes = TimexParser().parse("朝9時スタートです。")
    assert len(timexes) == 1
    assert timexes[0].value == "T09-XX-XX"
    assert timexes[0].type == "TIME"
    assert timexes[0].text == "朝9時"

    timexes = TimexParser().parse("今夜9時スタートです。")
    assert len(timexes) == 1
    assert timexes[0].value == "T21-XX-XX"
    assert timexes[0].type == "TIME"
    assert timexes[0].text == "今夜9時"


def test_duration_with_half_expression(p):
    timexes = TimexParser().parse("今から1時間半後に始めます")
    assert len(timexes) == 1
    assert timexes[0].value == "PT1.5H"
    assert timexes[0].type == "DURATION"
    assert timexes[0].text == "1時間半後"

    timexes = TimexParser().parse("今から2年半ほど前の話")
    assert len(timexes) == 1
    assert timexes[0].value == "P2.5Y"
    assert timexes[0].type == "DURATION"
    assert timexes[0].text == "2年半ほど前"


def test_duration_with_half_expression_without_number(p):
    timexes = TimexParser().parse("半年前の記念日")
    assert len(timexes) == 1
    assert timexes[0].value == "P0.5Y"
    assert timexes[0].type == "DURATION"
    assert timexes[0].text == "半年前"

    timexes = TimexParser().parse("四半世紀の時を経て")
    assert len(timexes) == 1
    assert timexes[0].value == "P25Y"
    assert timexes[0].type == "DURATION"
    assert timexes[0].text == "四半世紀"


def test_just_suffix_reltime(p):
    # 8日というDATEではなく、8日目というDURATION
    timexes = p.parse("8日目の蝉")
    assert timexes[0].value == "P8D"
    assert timexes[0].type == "DURATION"
    assert timexes[0].mod == "JUST"

    timexes = p.parse("30年もの間")
    assert timexes[0].value == "P30Y"
    assert timexes[0].type == "DURATION"
    assert timexes[0].mod == "JUST"
