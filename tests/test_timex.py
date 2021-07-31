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
