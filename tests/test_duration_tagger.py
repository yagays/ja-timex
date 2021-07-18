import pytest

from ja_timex.tagger.duration_tagger import DurationTagger


@pytest.fixture(scope="module")
def t():
    return DurationTagger()


def test_year(t):
    assert t.parse("1年間").value == "P1Y"
    assert t.parse("100年間").value == "P100Y"
    
    # abstimeともdurationとも取れる表現
    assert t.parse("1年").value == "P1Y"
    assert t.parse("2021年").value == "P2021Y"


def test_month(t):
    assert t.parse("1ヶ月間").value == "P1M"
    assert t.parse("100ヶ月間").value == "P100M"
    assert t.parse("1ヶ月").value == "P1M"


def test_day(t):
    assert t.parse("1日間").value == "P1D"
    assert t.parse("100日間").value == "P100D"
    assert t.parse("1日").value == "P1D"


def test_hour(t):
    assert t.parse("1時間").value == "PT1H"
    assert t.parse("100時間").value == "PT100H"

    # 1時間のことを1時とは呼ばない
    assert t.parse("1時") is None


def test_minutes(t):
    assert t.parse("1分間").value == "PT1M"
    assert t.parse("100分間").value == "PT100M"
    assert t.parse("1分").value == "PT1M"


def test_second(t):
    assert t.parse("1秒間").value == "PT1S"
    assert t.parse("100秒間").value == "PT100S"
    assert t.parse("1秒").value == "PT1S"


def test_second_with_ms(t):
    assert t.parse("1秒05").value == "PT1.05S"
    assert t.parse("100秒5").value == "PT100.5S"
    assert t.parse("1秒0").value == "PT1.0S"
