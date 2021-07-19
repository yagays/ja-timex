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


def test_year_mod(t):
    assert t.parse("1年前").mod == "BEFORE"
    assert t.parse("1年後").mod == "AFTER"
