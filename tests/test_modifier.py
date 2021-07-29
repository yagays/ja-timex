import pytest

from ja_timex.modifier import Modifier
from ja_timex.tag import TIMEX


@pytest.fixture(scope="module")
def m():
    return Modifier()


def test_modifier_prefix(m):
    target_text = "約1年前"
    target_timex = TIMEX(type="DATE", value="", value_from_surface="", text=target_text, span=(1, 4))
    assert m.parse(target_text, target_timex).mod == "APPROX"

    span = m.parse(target_text, target_timex).span
    assert "約1年前" == target_text[span[0] : span[1]]

    target_text = "約、1年前"
    target_timex = TIMEX(type="DATE", value="", value_from_surface="", text=target_text, span=(2, 5))
    assert m.parse(target_text, target_timex).mod is None

    span = m.parse(target_text, target_timex).span
    assert "1年前" == target_text[span[0] : span[1]]


def test_modifier_suffix(m):
    target_text = "2021年頃"
    target_timex = TIMEX(type="DATE", value="", value_from_surface="", text=target_text, span=(0, 5))
    assert m.parse(target_text, target_timex).mod == "APPROX"
    assert m.parse(target_text, target_timex).span == (0, 6)

    target_text = "2021年かその頃"
    target_timex = TIMEX(type="DATE", value="", value_from_surface="", text=target_text, span=(0, 5))
    assert m.parse(target_text, target_timex).mod is None
    assert m.parse(target_text, target_timex).span == (0, 5)
