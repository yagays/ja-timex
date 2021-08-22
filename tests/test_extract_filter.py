from ja_timex.extract_filter import NumexpFilter, PartialNumFilter


def test_numexp_filter():
    f = NumexpFilter()

    assert f.filter((0, 4), "7.18キロメートル")
    assert f.filter((0, 4), "7.18 キロメートル")
    assert f.filter((0, 4), "7.18cm")
    assert f.filter((0, 4), "7.18mm")
    assert f.filter((0, 4), "7.18%")
    assert f.filter((0, 4), "7.18インチ")
    assert f.filter((0, 4), "7.18GHz")
    assert f.filter((0, 3), "2.4GHz")
    assert f.filter((0, 4), "7.18円")

    assert not f.filter((0, 4), "7.18は晴れ")
    assert not f.filter((0, 4), "7.18に釣り上げられた10メートルの魚")

    # 3つ以上の数字に分けられる場合はフィルタの対象外
    assert not f.filter((0, 4), "2020.7.18")
    assert not f.filter((0, 4), "2020.7.18円相場は")  # 単位が付いていた場合も同様


def test_partial_num_filter():
    f = PartialNumFilter()
    # 前後に数字または+がある場合
    # マイナスは1/12-1/20といった表現があるため、対象外
    assert "13/13"[0:4] == "13/1"
    assert f.filter((0, 4), "13/13")

    assert "13/13"[1:5] == "3/13"
    assert f.filter((1, 5), "13/13")

    assert "13/1+2"[0:4] == "13/1"
    assert f.filter((0, 4), "13/1+2")

    assert "+3/13"[1:5] == "3/13"
    assert f.filter((1, 5), "+3/13")

    # 前後に数字ではない文字の場合
    assert "13/1は"[0:4] == "13/1"
    assert not f.filter((0, 4), "13/1は")

    assert "は3/13"[1:5] == "3/13"
    assert not f.filter((1, 5), "は3/13")

    # 末尾の0.1の前方に"."がある場合もTrueと判定する
    assert f.filter((0, 4), "128.0.0.1")
