import pytest

from ja_timex.timex import TimexParser


@pytest.fixture(scope="module")
def p():
    return TimexParser()


# 取得すべきではない表現が正しく取得されないか


def test_century_without_number(p):
    assert p.parse("世紀の瞬間を目撃した") == []
    assert p.parse("世紀末のノストラダムスの大予言") == []


def test_phrase_contains_temporal_expression(p):
    assert p.parse("一時的に太ったな") == []
    assert p.parse("準備が不十分だった") == []


def test_pattern_filter_numexp(p):
    assert len(p.parse("高さは7.18メートルです")) == 0
    assert len(p.parse("濃度は7.18%です")) == 0


def test_pattern_filter_partial_num(p):
    assert len(p.parse("13/13は1です")) == 0

    # 7.7を取得しない
    assert len(p.parse("興行収入2億7.765万円を記録した")) == 0

    # 1/5を取得しない
    assert len(p.parse("1/50の縮小模型")) == 0

    # 320/5を取得しない
    assert len(p.parse("BCI-321+320/5MP")) == 0

    # 37-3, 3.9を取得しない
    assert len(p.parse("Core i7-3770（3.90GHz）")) == 0


def test_ignore_kansuji():
    p = TimexParser(ignore_kansuji=True)

    # 一昨日とかは漢数字のままパターン化している
    assert len(p.parse("一昨日のことは覚えていない")) == 1

    # 漢数字の表現は読み取ることができない
    assert p.parse("十分のインターバル") == []
    assert p.parse("ここから三時間はかかる") == []
    assert p.parse("週三回の運動") == []
