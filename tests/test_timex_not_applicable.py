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


# 取得すべきではないが、ルールベースでは取得せざるを得ないケース


def test_abstime_partial_pattern_of_number_expression(p):
    # 部分的な表現はなるべく取得しない

    timexes = p.parse("13/13は1です")
    assert len(timexes) == 1
    # 3/13を取得しないが、13/1は取得されてしまう
    # 「今月8日」といった直後に続く数字があるため
