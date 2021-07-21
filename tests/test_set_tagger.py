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


def test_count_range_is_temporal_expression(t):
    # 時間表現を対象としており、「3回に1回」のような時間を含まない表現は解析しない
    assert t.parse("3回に1回") is None
    assert t.parse("1回1時間") is None


def test_count_kanni_in_minutes_and_second(t):
    # 「に」「間に」とは言う
    assert t.parse("1秒に1回") is not None
    assert t.parse("1秒間に1回") is not None
    assert t.parse("1分に1回") is not None
    assert t.parse("1分間に1回") is not None

    # 「間」だけでは言わない
    assert t.parse("1秒間1回") is None
    assert t.parse("1分間1回") is None


def test_count_larger_than_range_is_invalid(t):
    # 基準となる単位より、繰り返しとなる単位が大きくなってはいけない
    assert t.parse("1ヶ月に1年") is None
    assert t.parse("1週に1年") is None
    assert t.parse("1週に1ヶ月") is None
    assert t.parse("1日に1年") is None
    assert t.parse("1日に1ヶ月") is None
    assert t.parse("1日に1週") is None
    assert t.parse("1時間に1年") is None
    assert t.parse("1時間に1ヶ月") is None
    assert t.parse("1時間に1週") is None
    assert t.parse("1時間に1日") is None
    assert t.parse("1分に1年") is None
    assert t.parse("1分に1ヶ月") is None
    assert t.parse("1分に1週") is None
    assert t.parse("1分に1日") is None
    assert t.parse("1分に1時間") is None
    assert t.parse("1秒に1年") is None
    assert t.parse("1秒に1月") is None
    assert t.parse("1秒に1週") is None
    assert t.parse("1秒に1日") is None
    assert t.parse("1秒に1時間") is None
    assert t.parse("1秒に1分") is None


def test_same_count_and_range_is_invalid_at_day_expression(t):
    # 基準となる単位と繰り返しとなる単位が同じでかつ対象が年や月の場合は対象としない
    assert t.parse("4年に1年") is None
    assert t.parse("3ヶ月に1月") is None


def test_same_count_and_range_is_valid_at_time_expression(t):
    # 基準となる単位と繰り返しとなる単位が同じでかつ対象が時間や週の場合は対象とする
    assert t.parse("3週に1週") is not None  # e.g. 土曜日は3週に1週、出勤してください
    assert t.parse("7日に1日") is not None  # e.g. 7日間に1日は休まねばなりません
    assert t.parse("3時間に1時間") is not None
    assert t.parse("3分間に1分") is not None
    assert t.parse("3秒に1秒") is not None


def test_count_has_ni_as_same_unit(t):
    # 頻度表現で「3日1日」とは言わない。必ず「3日に1日」というように「に」が含まれる
    assert t.parse("3週に1週") is not None
    assert t.parse("3日に1日") is not None
    assert t.parse("3分に1分") is not None
    assert t.parse("3秒に1秒") is not None

    assert t.parse("3週1週") is None
    assert t.parse("3日1日") is None
    assert t.parse("3分1分") is None
    assert t.parse("3秒1秒") is None


def test_count_frequency(t):
    assert t.parse("3日に1回").freq == "1X"
    assert t.parse("3日に1度").freq == "1X"

    # 度の表現は1,2にはよく使うが、3以上にはあまり使わない印象がある
    # 違和感があるものの意味が通じなくはないので、回と同様に扱う
    assert t.parse("3日に10回").freq == "10X"
    assert t.parse("3日に10度").freq == "10X"


def test_count_range(t):
    assert t.parse("3年に1回").value == "P3Y"
    assert t.parse("3年に1回").freq == "1X"