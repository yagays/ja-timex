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


def test_abstime_partial_pattern_of_number_expression(p):
    # 部分的な表現はなるべく取得しない

    timexes = p.parse("13/13は1です")
    assert len(timexes) == 1
    # 3/13を取得しないが、13/1は取得されてしまう
    # 「今月8日」といった直後に続く数字があるため


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
