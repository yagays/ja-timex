import pytest

from ja_timex.tagger.set_tagger import SetTagger


@pytest.fixture(scope="module")
def t():
    return SetTagger()


def test_count(t):
    assert t.parse("年1回").value == "P1Y"
    assert t.parse("年1回").freq == "1X"

    # ここから下は全部同じ表現になるが正しいのか？
    # @unitが必要かもしれない
    assert t.parse("年に1ヶ月").value == "P1Y"
    assert t.parse("年に1ヶ月").freq == "P1M"
    assert t.parse("年に1日").value == "P1Y"
    assert t.parse("年に1日").freq == "P1D"
    assert t.parse("年に1時間").value == "P1Y"
    assert t.parse("年に1時間").freq == "PT1H"
    assert t.parse("年に1分").value == "P1Y"
    assert t.parse("年に1分").freq == "PT1M"
    assert t.parse("年に1秒").value == "P1Y"
    assert t.parse("年に1秒").freq == "PT1S"

    assert t.parse("年3回").value == "P1Y"
    assert t.parse("年3回").freq == "3X"

    assert t.parse("月10回").value == "P1M"
    assert t.parse("月10回").freq == "10X"

    assert t.parse("日に3回").value == "P1D"
    assert t.parse("日に3回").freq == "3X"

    assert t.parse("週40時間").value == "P1W"
    assert t.parse("週40時間").freq == "PT40H"


def test_count_range(t):
    assert t.parse("3年に1回").value == "P3Y"
    assert t.parse("3年に1回").freq == "1X"
