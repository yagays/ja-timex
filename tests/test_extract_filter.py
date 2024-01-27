import re

from ja_timex.extract_filter import DecimalFilter, NumexpFilter, PartialNumFilter, PartialPhraseFilter
from ja_timex.pattern.place import Pattern
from ja_timex.tag import Extract


def make_extract(target, original, type_name="abstime"):
    return Extract(
        type_name=type_name,
        re_match=re.search(target, original),
        pattern=Pattern(re_pattern=None, parse_func=lambda x: x, option=None),
    )


def test_numexp_filter():
    f = NumexpFilter()

    assert f.filter(make_extract("7.18", "7.18キロメートル"), "7.18キロメートル")
    assert f.filter(make_extract("7.18", "7.18 キロメートル"), "7.18 キロメートル")
    assert f.filter(make_extract("7.18", "7.18cm"), "7.18cm")
    assert f.filter(make_extract("7.18", "7.18mm"), "7.18mm")
    assert f.filter(make_extract("7.18", "7.18%"), "7.18%")
    assert f.filter(make_extract("7.18", "7.18インチ"), "7.18インチ")
    assert f.filter(make_extract("7.18", "7.18GHz"), "7.18GHz")
    assert f.filter(make_extract("7.18", "7.18円"), "7.18円")
    assert f.filter(make_extract("2.4", "2.4GHz"), "2.4GHz")

    assert not f.filter(make_extract("7.18", "7.18は晴れ"), "7.18は晴れ")
    assert not f.filter(
        make_extract("7.18", "7.18に釣り上げられた10メートルの魚"), "7.18に釣り上げられた10メートルの魚"
    )

    # 3つ以上の数字に分けられる場合はフィルタの対象外
    assert not f.filter(make_extract("2020.7.18", "2020.7.18"), "2020.7.18")
    assert not f.filter(
        make_extract("2020.7.18", "2020.7.18円相場は"), "2020.7.18円相場は"
    )  # 単位が付いていた場合も同様


def test_partial_num_filter():
    f = PartialNumFilter()
    # 前後に数字または+がある場合
    # マイナスは1/12-1/20といった表現があるため、対象外
    assert f.filter(make_extract("13/1", "13/13"), "13/13")

    assert f.filter(make_extract("3/13", "13/13"), "13/13")

    assert f.filter(make_extract("13/1", "13/1+2"), "13/1+2")

    assert f.filter(make_extract("3/13", "+3/13"), "+3/13")

    # 前後に数字ではない文字の場合
    assert not f.filter(make_extract("13/1", "13/1は"), "13/1は")

    assert not f.filter(make_extract("3/13", "は3/13"), "は3/13")

    # 末尾の0.1の前方に"."がある場合もTrueと判定する
    assert f.filter(make_extract("0.1", "127.0.0.1"), "127.0.0.1")


def test_decimal_filter():
    f = DecimalFilter()

    # 0.1や0/1, 0-1といった表現において、0が0000年を表すことはない
    assert f.filter(make_extract("0.18", "0.18"), "0.18")
    assert f.filter(make_extract("0/10", "0/10"), "0/10")
    assert f.filter(make_extract("0-10", "0-10"), "0-10")

    # DURATIONの場合た対象外（0.1ヶ月という表記はあり得るため）
    assert not f.filter(make_extract("0.18", "0.18", "duration"), "0.18")


def test_partial_phrase_filter():
    f = PartialPhraseFilter()

    # suffix
    assert f.filter(make_extract("毎日", "毎日新聞によると"), "毎日新聞によると")  # suffixかつそれが"新聞"の場合
    assert not f.filter(make_extract("毎日", "毎日読んでる新聞によると"), "毎日読んでる新聞によると")  # 離れている場合
    assert not f.filter(make_extract("毎日", "新聞毎日読んでる"), "新聞毎日読んでる")  # prefixの場合

    # prefix
    assert f.filter(make_extract("3年", "石の上にも3年と言いますが"), "石の上にも3年と言いますが")
    assert f.filter(make_extract("三年", "石の上にも三年と言いますが"), "石の上にも三年と言いますが")

    assert not f.filter(
        make_extract("3年", "石の上に3年と言いますが"), "石の上に3年と言いますが"
    )  # 一部文字が変わっている場合
    assert not f.filter(
        make_extract("三年", "石の上に三年と言いますが"), "石の上に三年と言いますが"
    )  # 一部文字が変わっている場合
