from ja_timex.filter import NumexpFilter


def test_numexp_filter():
    nf = NumexpFilter()

    assert nf.filter((0, 4), "7.18キロメートル")
    assert nf.filter((0, 4), "7.18 キロメートル")
    assert nf.filter((0, 4), "7.18cm")
    assert nf.filter((0, 4), "7.18mm")
    assert nf.filter((0, 4), "7.18%")

    assert not nf.filter((0, 4), "7.18は晴れ")
    assert not nf.filter((0, 4), "7.18に釣り上げられた10メートルの魚")
