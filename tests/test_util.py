from ja_timex.util import is_parial_pattern_of_number_expression


def test_is_parial_pattern_of_number_expression():
    # 前後に数字または+がある場合
    # マイナスは1/12-1/20といった表現があるため、対象外
    assert "13/13"[0:4] == "13/1"
    assert is_parial_pattern_of_number_expression((0, 4), "13/13")

    assert "13/13"[1:5] == "3/13"
    assert is_parial_pattern_of_number_expression((1, 5), "13/13")

    assert "13/1+2"[0:4] == "13/1"
    assert is_parial_pattern_of_number_expression((0, 4), "13/1+2")

    assert "+3/13"[1:5] == "3/13"
    assert is_parial_pattern_of_number_expression((1, 5), "+3/13")

    # 前後に数字ではない文字の場合
    assert "13/1は"[0:4] == "13/1"
    assert not is_parial_pattern_of_number_expression((0, 4), "13/1は")

    assert "は3/13"[1:5] == "3/13"
    assert not is_parial_pattern_of_number_expression((1, 5), "は3/13")
