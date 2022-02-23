import pendulum
import pytest

from ja_timex.timex import TimexParser


@pytest.fixture(scope="module")
def p():
    return TimexParser()


@pytest.fixture(scope="module")
def p_ref():
    return TimexParser(reference=pendulum.datetime(2021, 7, 18, tz="Asia/Tokyo"))


def test_reference_datetime_without_reference(p):
    timexes = p.parse("2021年7月18日")
    assert timexes[0].reference is None


def test_reference_datetime(p_ref):
    # すべての時間情報表現にreference datetimeが付与される
    timexes = p_ref.parse("2021年7月18日")
    assert timexes[0].type == "DATE"
    assert timexes[0].reference == pendulum.datetime(2021, 7, 18, tz="Asia/Tokyo")

    timexes = p_ref.parse("12時59分")
    assert timexes[0].type == "TIME"
    assert timexes[0].reference == pendulum.datetime(2021, 7, 18, tz="Asia/Tokyo")

    timexes = p_ref.parse("1時間前")
    assert timexes[0].type == "DURATION"
    assert timexes[0].reference == pendulum.datetime(2021, 7, 18, tz="Asia/Tokyo")

    timexes = p_ref.parse("週1回")
    assert timexes[0].type == "SET"
    assert timexes[0].reference == pendulum.datetime(2021, 7, 18, tz="Asia/Tokyo")


def test_reference_datetime_default_year(p):
    reference_past = pendulum.datetime(2010, 7, 18, tz="Asia/Tokyo")

    timexes = TimexParser(reference=reference_past).parse("2021年12月30日")
    assert timexes[0].to_datetime() == pendulum.datetime(2021, 12, 30, tz="Asia/Tokyo")

    # 年を補完
    timexes = TimexParser(reference=reference_past).parse("12月30日")
    assert timexes[0].to_datetime() == pendulum.datetime(2010, 12, 30, tz="Asia/Tokyo")

    # 年を補完
    timexes = TimexParser(reference=reference_past).parse("12月")
    assert timexes[0].to_datetime() == pendulum.datetime(2010, 12, 1, tz="Asia/Tokyo")

    # 年と月を補完
    timexes = TimexParser(reference=reference_past).parse("30日")
    assert timexes[0].to_datetime() == pendulum.datetime(2010, 7, 30, tz="Asia/Tokyo")

    # 2021年でもreferenceのmonth/dayとは限らないので、補完しない
    timexes = TimexParser(reference=reference_past).parse("2021年")
    assert timexes[0].to_datetime() == pendulum.datetime(2021, 1, 1, tz="Asia/Tokyo")

    timexes = TimexParser(reference=reference_past).parse("12時59分")
    assert timexes[0].to_datetime() == pendulum.datetime(2010, 7, 18, 12, 59, tz="Asia/Tokyo")


def test_reference_datetime_exclude(p_ref):
    # 世紀や曜日はdatetimeでは変換できない

    # reference無し
    timexes = TimexParser().parse("20世紀")
    assert timexes[0].to_datetime() is None

    timexes = TimexParser().parse("紀元前3世紀")
    assert timexes[0].to_datetime() is None

    timexes = TimexParser().parse("木曜日")
    assert timexes[0].to_datetime() is None

    # reference有り
    timexes = p_ref.parse("20世紀")
    assert timexes[0].to_datetime() is None

    timexes = p_ref.parse("紀元前3世紀")
    assert timexes[0].to_datetime() is None

    timexes = p_ref.parse("木曜日")
    assert timexes[0].to_datetime() is None

    # 日付と{曜日,世紀}は別のTIMEXで抽出されるので、影響しない
    timexes = p_ref.parse("2021年12月30日木曜日")
    assert timexes[0].to_datetime() == pendulum.datetime(2021, 12, 30, tz="Asia/Tokyo")
    assert timexes[1].to_datetime() is None

    timexes = p_ref.parse("30日木曜日")
    assert timexes[0].to_datetime() == pendulum.datetime(2021, 7, 30, tz="Asia/Tokyo")
    assert timexes[1].to_datetime() is None

    timexes = p_ref.parse("20世紀12月30日")
    assert timexes[0].to_datetime() is None
    assert timexes[1].to_datetime() == pendulum.datetime(2021, 12, 30, tz="Asia/Tokyo")


def test_reference_datetime_time(p_ref):
    timexes = p_ref.parse("12時59分1秒")
    assert timexes[0].to_datetime() == pendulum.datetime(2021, 7, 18, 12, 59, 1, tz="Asia/Tokyo")

    timexes = p_ref.parse("12時59分")
    assert timexes[0].to_datetime() == pendulum.datetime(2021, 7, 18, 12, 59, 0, tz="Asia/Tokyo")

    timexes = p_ref.parse("23時")
    assert timexes[0].to_datetime() == pendulum.datetime(2021, 7, 18, 23, 0, 0, tz="Asia/Tokyo")

    # 翌日の0時,1時
    timexes = p_ref.parse("24時")
    assert timexes[0].to_datetime() == pendulum.datetime(2021, 7, 19, 0, 0, 0, tz="Asia/Tokyo")

    timexes = p_ref.parse("25時")
    assert timexes[0].to_datetime() == pendulum.datetime(2021, 7, 19, 1, 0, 0, tz="Asia/Tokyo")


def test_reference_datetime_duration(p_ref):
    timexes = p_ref.parse("1秒後")
    assert timexes[0].to_datetime() == pendulum.datetime(2021, 7, 18, 0, 0, 1, tz="Asia/Tokyo")
    timexes = p_ref.parse("1分後")
    assert timexes[0].to_datetime() == pendulum.datetime(2021, 7, 18, 0, 1, 0, tz="Asia/Tokyo")
    timexes = p_ref.parse("1時間後")
    assert timexes[0].to_datetime() == pendulum.datetime(2021, 7, 18, 1, 0, 0, tz="Asia/Tokyo")
    timexes = p_ref.parse("1日後")
    assert timexes[0].to_datetime() == pendulum.datetime(2021, 7, 19, 0, 0, 0, tz="Asia/Tokyo")
    timexes = p_ref.parse("2ヶ月後")
    assert timexes[0].to_datetime() == pendulum.datetime(2021, 9, 18, 0, 0, 0, tz="Asia/Tokyo")
    timexes = p_ref.parse("10年後")
    assert timexes[0].to_datetime() == pendulum.datetime(2031, 7, 18, 0, 0, 0, tz="Asia/Tokyo")

    timexes = p_ref.parse("1秒前")
    assert timexes[0].to_datetime() == pendulum.datetime(2021, 7, 17, 23, 59, 59, tz="Asia/Tokyo")
    timexes = p_ref.parse("1分前")
    assert timexes[0].to_datetime() == pendulum.datetime(2021, 7, 17, 23, 59, 0, tz="Asia/Tokyo")
    timexes = p_ref.parse("1時間前")
    assert timexes[0].to_datetime() == pendulum.datetime(2021, 7, 17, 23, 0, 0, tz="Asia/Tokyo")
    timexes = p_ref.parse("1日前")
    assert timexes[0].to_datetime() == pendulum.datetime(2021, 7, 17, 0, 0, 0, tz="Asia/Tokyo")
    timexes = p_ref.parse("2ヶ月前")
    assert timexes[0].to_datetime() == pendulum.datetime(2021, 5, 18, 0, 0, 0, tz="Asia/Tokyo")
    timexes = p_ref.parse("10年前")
    assert timexes[0].to_datetime() == pendulum.datetime(2011, 7, 18, 0, 0, 0, tz="Asia/Tokyo")

    timexes = p_ref.parse("半世紀前")
    assert timexes[0].to_datetime() == pendulum.datetime(1971, 7, 18, 0, 0, 0, tz="Asia/Tokyo")
    timexes = p_ref.parse("四半世紀前")
    assert timexes[0].to_datetime() == pendulum.datetime(1996, 7, 18, 0, 0, 0, tz="Asia/Tokyo")
    timexes = p_ref.parse("半年前")
    assert timexes[0].to_datetime() == pendulum.datetime(2021, 1, 18, 0, 0, 0, tz="Asia/Tokyo")
    timexes = p_ref.parse("半月前")  # 15日
    assert timexes[0].to_datetime() == pendulum.datetime(2021, 7, 3, 0, 0, 0, tz="Asia/Tokyo")
    timexes = p_ref.parse("半日前")
    assert timexes[0].to_datetime() == pendulum.datetime(2021, 7, 17, 12, 0, 0, tz="Asia/Tokyo")

    timexes = p_ref.parse("昨日の雨はひどかった")
    assert timexes[0].to_datetime() == pendulum.datetime(2021, 7, 17, 0, 0, 0, tz="Asia/Tokyo")

    timexes = p_ref.parse("明後日には完成するでしょう")
    assert timexes[0].to_datetime() == pendulum.datetime(2021, 7, 20, 0, 0, 0, tz="Asia/Tokyo")
