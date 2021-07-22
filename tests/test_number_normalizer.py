import pytest

from ja_timex.number_normalizer import NumberNormalizer, kansuji2number


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


def test_kansuji2number():
    assert kansuji2number("零") == "0"
    assert kansuji2number("一") == "1"
    assert kansuji2number("二") == "2"
    assert kansuji2number("三") == "3"

    # 十/百/千は単体で使用したり先頭に付けることができる
    assert kansuji2number("十") == "10"
    assert kansuji2number("百") == "100"
    assert kansuji2number("千") == "1000"
    # 万以上は必ず数字を伴う
    assert kansuji2number("一万") == "10000"
    assert kansuji2number("一億") == "100000000"
    assert kansuji2number("一兆") == "1000000000000"
    assert kansuji2number("一京") == "10000000000000000"
    assert kansuji2number("一垓") == "100000000000000000000"

    # 十
    assert kansuji2number("十一") == "11"
    assert kansuji2number("二十") == "20"
    assert kansuji2number("二十一") == "21"

    # 百
    assert kansuji2number("百二十一") == "121"
    assert kansuji2number("百二十") == "120"
    assert kansuji2number("百一") == "101"
    assert kansuji2number("二百一") == "201"

    # 千
    assert kansuji2number("九千二百三十四") == "9234"
    assert kansuji2number("千二百三十四") == "1234"
    assert kansuji2number("千二百三十") == "1230"
    assert kansuji2number("千二百十") == "1210"
    assert kansuji2number("千二百四") == "1204"
    assert kansuji2number("千三十四") == "1034"
    assert kansuji2number("千四") == "1004"
    assert kansuji2number("千百") == "1100"

    # 万
    assert kansuji2number("一万二千三百四十五") == "12345"
    assert kansuji2number("一万二千三百四十") == "12340"
    assert kansuji2number("一万三百四十五") == "10345"
    assert kansuji2number("一万四十五") == "10045"
    assert kansuji2number("一万五") == "10005"

    assert kansuji2number("十万二千三百四十五") == "102345"
    assert kansuji2number("一千一百万") == "11000000"


def test_kansuji2number_positional_notation():
    # 位取り記数法
    assert kansuji2number("一五") == "15"
    assert kansuji2number("一〇") == "10"
    assert kansuji2number("三〇") == "30"
    assert kansuji2number("一八二〇") == "1820"

    # ゼロのみ
    assert kansuji2number("〇") == "0"
    assert kansuji2number("〇〇") == "00"

    # コンマ、小数点を含む
    # 青空文庫「五ヵ年計画とソヴェト同盟の文化的飛躍」宮本百合子
    assert kansuji2number("一、〇〇〇・〇〇〇") == "1、000・000"

    # 日付表現
    # 青空文庫 「獄中への手紙 07 一九四〇年（昭和十五年）」宮本百合子
    assert kansuji2number("一九四〇・一・四") == "1940・1・4"

    # 時間表現
    # 青空文庫「単独行」加藤文太郎
    assert kansuji2number("六・〇〇") == "6・00"
    assert kansuji2number("一〇・三〇") == "10・30"

    # 以下の表記は存在するが、ここでは数字のみが入ってくる前提のため、考慮しない
    # assert kansuji2number("一〇万年") == "10万年"


1940


def test_test_kansuji2number_mixed():
    # その桁が0であることを示すような、記法が混ざるパターン

    # 青空文庫「吉田松陰」徳富蘇峰
    assert kansuji2number("一千七百〇八") == "1708"
    # 青空文庫「みみずのたはこと」徳冨健次郎 徳冨蘆花
    assert kansuji2number("百〇七") == "107"
    # 青空文庫「特殊部落の人口増殖」喜田貞吉
    assert kansuji2number("二千〇〇一") == "2001"
    # 青空文庫「利根川水源地の山々」木暮理太郎
    assert kansuji2number("千七百六〇") == "1760"
    # 〇が2つ以上の場合
    assert kansuji2number("千六〇〇") == "1600"

    # 「五ヵ年計画とソヴェト同盟の文化的飛躍」宮本百合子
    # assert kansuji2number("三二〇千〇〇〇") == "320000"


def test_normalize_phrase_contains_number(nn):
    # 下記は青空文庫より用例を収集

    # 魔都 久生十蘭
    assert nn.normalize("噴水が歌を唄うということですが一体それは真実でしょうか")

    # 三国志 05 臣道の巻 吉川英治
    assert nn.normalize("三人の血はひとつだ。三人は一心同体だと")

    # 獄中への手紙 06 一九三九年（昭和十四年） 宮本百合子
    assert nn.normalize("歩くのがまだ十分ゆかず。")
