import pytest

from ja_timex.modifier import Modifier


@pytest.fixture(scope="module")
def m():
    return Modifier()


def test_modifier_prefix(m):
    assert m.parse("約1年前", (1, 2), "DATE") == "APPROX"

    assert m.parse("約、1年前", (2, 3), "DATE") is None


def test_modifier_suffix(m):
    assert m.parse("2021年頃", (0, 4), "DATE") == "APPROX"

    assert m.parse("2021年かその頃", (0, 4), "DATE") is None
