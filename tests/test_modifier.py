import pytest

from ja_timex.modifier import Modifier
from ja_timex.tag import TIMEX


@pytest.fixture(scope="module")
def m():
    return Modifier()


def test_modifier_prefix(m):
    target_text = "約1年前"
    target_timex = TIMEX(type="DATE", value="", value_from_surface="", text=target_text, span=(1, 2))
    assert m.parse(target_text, target_timex).mod == "APPROX"

    target_text = "約、1年前"
    target_timex = TIMEX(type="DATE", value="", value_from_surface="", text=target_text, span=(2, 3))
    assert m.parse(target_text, target_timex).mod is None


def test_modifier_suffix(m):
    target_text = "2021年頃"
    target_timex = TIMEX(type="DATE", value="", value_from_surface="", text=target_text, span=(0, 4))
    assert m.parse(target_text, target_timex).mod == "APPROX"

    target_text = "2021年かその頃"
    target_timex = TIMEX(type="DATE", value="", value_from_surface="", text=target_text, span=(0, 4))
    assert m.parse(target_text, target_timex).mod is None
