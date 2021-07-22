import pytest

from ja_timex.number_normalizer import NumberNormalizer


@pytest.fixture(scope="module")
def nn():
    return NumberNormalizer()


def test_normalize_number(nn):
    pass


def test_normalize_zen_to_han(nn):
    assert nn._normalize_zen_to_han("１世紀") == "1世紀"
    assert nn._normalize_zen_to_han("２０２１年") == "2021年"
    assert nn._normalize_zen_to_han("複数現れる１や２といった全角数字") == "複数現れる1や2といった全角数字"

    assert nn._normalize_zen_to_han("カナやａｂｃは変わらない") == "カナやａｂｃは変わらない"

    # 数字の間にはいる,や.の全角文字
    assert nn._normalize_zen_to_han("１，０００年") == "1,000年"
    assert nn._normalize_zen_to_han("１．０時間") == "1.0時間"

    assert nn._normalize_zen_to_han("通常の句点．または句読点，は変換しない") == "通常の句点．または句読点，は変換しない"


def test_remove_comma_inside_digits(nn):
    assert nn._remove_comma_inside_digits("1,000時間") == "1000時間"
    assert nn._remove_comma_inside_digits("今から3,000年前") == "今から3000年前"
    assert nn._remove_comma_inside_digits("今から1,234,567,890年前") == "今から1234567890年前"

    # 通常の数字表現
    assert nn._remove_comma_inside_digits("1234") == "1234"
    assert nn._remove_comma_inside_digits("12.345") == "12.345"

    # 数字の列挙ではあるが、全体で一つの数字を表すものではない場合
    assert nn._remove_comma_inside_digits("12,") == "12,"
    assert nn._remove_comma_inside_digits("1,2,3") == "1,2,3"
    assert nn._remove_comma_inside_digits("12,34,56") == "12,34,56"
    assert nn._remove_comma_inside_digits("12.23.45.67") == "12.23.45.67"
    assert nn._remove_comma_inside_digits("1000,1001") == "1000,1001"
    assert nn._remove_comma_inside_digits("1000,1001,12") == "1000,1001,12"

    # 判定が困難なケース
    # [12, 345, 67]と[12345, 67]の2つのケースが考えられるが、ここでは後者を採用する
    assert nn._remove_comma_inside_digits("12,345,67") == "12345,67"
    # 桁が増えても同様
    assert nn._remove_comma_inside_digits("12,345,678,9") == "12345678,9"


def test_remove_comma_inside_digits_only_str(nn):
    assert nn._remove_comma_inside_digits("こんにちは") == "こんにちは"
    assert nn._remove_comma_inside_digits("千時間") == "千時間"


def test_normalize_phrase_contains_number(nn):
    # 下記は青空文庫より用例を収集

    # 魔都 久生十蘭
    assert nn.normalize("噴水が歌を唄うということですが一体それは真実でしょうか")

    # 三国志 05 臣道の巻 吉川英治
    assert nn.normalize("三人の血はひとつだ。三人は一心同体だと")

    # 獄中への手紙 06 一九三九年（昭和十四年） 宮本百合子
    assert nn.normalize("歩くのがまだ十分ゆかず。")
