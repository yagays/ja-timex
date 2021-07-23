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
