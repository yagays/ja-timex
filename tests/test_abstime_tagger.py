import pytest

from ja_timex.tagger.abstime_tagger import AbstimeTagger


@pytest.fixture(scope="module")
def t():
    return AbstimeTagger()


def test_normal_date(t):
    assert t.parse("2021年7月18日").value == "2021-07-18"
    assert t.parse("2021/7/18").value == "2021-07-18"
    assert t.parse("2021-7-18").value == "2021-07-18"
    assert t.parse("2021.7.18").value == "2021-07-18"
    assert t.parse("2021・7・18").value == "2021-07-18"
    assert t.parse("2021,7,18").value == "2021-07-18"

    assert t.parse("2021年7月").value == "2021-07-XX"
    assert t.parse("7月18日").value == "XXXX-07-18"
    assert t.parse("2021年").value == "2021-XX-XX"
    assert t.parse("7月").value == "XXXX-07-XX"
    assert t.parse("18日").value == "XXXX-XX-18"

    assert t.parse("2021年/7月/18日").value == "2021-07-18"
    assert t.parse("2021/7").value == "2021-07-XX"
    assert t.parse("7/18").value == "XXXX-07-18"
    assert t.parse("2021年/7月").value == "2021-07-XX"
    assert t.parse("2021/7月").value == "2021-07-XX"
    assert t.parse("2021年/7").value == "2021-07-XX"


def test_normal_date_multiple_detected(t):
    # 年/月か月/日かが判定できなく、複数取得されるパターン

    # 基本的には月/日を優先する
    assert t.parse("7/8").value == "XXXX-07-08"
    assert t.parse("12/10").value == "XXXX-12-10"  # 2012年10月とも取れる
    assert t.parse("09/12").value == "XXXX-09-12"  # 2009年12月とも取れる

    # 月が取る値の範囲外の場合は年になる
    assert t.parse("2021/07").value == "2021-07-XX"
    assert t.parse("13/8").value == "0013-08-XX"  # :TODO どこかで2013に変換したい


def test_normal_date_invalid(t):
    # 2013年13月とも13月13日とも言えない場合
    assert t.parse("13/13") == None


def test_normal_date_with_weekday(t):
    # 日付はoptionに入る???
    assert t.parse("2021年7月18日日曜日").value == "2021-07-18"
    assert t.parse("7月18日日曜日").value == "XXXX-07-18"
    assert t.parse("18日日曜日").value == "XXXX-XX-18"

    assert t.parse("2021年7月18日(日)").value == "2021-07-18"
    assert t.parse("2021年7月18日(日曜)").value == "2021-07-18"
    assert t.parse("2021年7月18日(日曜日)").value == "2021-07-18"
    assert t.parse("2021年7月18日 日").value == "2021-07-18"
    assert t.parse("2021年7月18日 日曜").value == "2021-07-18"
    assert t.parse("2021年7月18日 日曜日").value == "2021-07-18"

    assert t.parse("2021年7月18日 (日)").value == "2021-07-18"
    assert t.parse("2021年7月18日 ( 日 )").value == "2021-07-18"
    assert t.parse("2021年7月18日 ( 日 ) ").value == "2021-07-18"  # 末尾のスペースはtagger内の前処理で消える

    assert t.parse("2021年7月18日日曜日").additional_info == {"weekday_text": "日", "weekday_id": "7"}
    assert t.parse("2021年7月18日日曜").additional_info == {"weekday_text": "日", "weekday_id": "7"}
    assert t.parse("2021年7月18日(日)").additional_info == {"weekday_text": "日", "weekday_id": "7"}
    assert t.parse("2021年7月18日 (日)").additional_info == {"weekday_text": "日", "weekday_id": "7"}


def test_weekday(t):
    assert t.parse("月曜日").value == "XXXX-WXX-1"
    assert t.parse("火曜日").value == "XXXX-WXX-2"
    assert t.parse("水曜日").value == "XXXX-WXX-3"
    assert t.parse("木曜日").value == "XXXX-WXX-4"
    assert t.parse("金曜日").value == "XXXX-WXX-5"
    assert t.parse("土曜日").value == "XXXX-WXX-6"
    assert t.parse("日曜日").value == "XXXX-WXX-7"

    assert t.parse("月").value == "XXXX-WXX-1"
    assert t.parse("月曜").value == "XXXX-WXX-1"
    assert t.parse("(月曜日)").value == "XXXX-WXX-1"
    assert t.parse("(月)").value == "XXXX-WXX-1"


def test_season(t):
    assert t.parse("春").value == "XXXX-SP"
    assert t.parse("夏").value == "XXXX-SU"
    assert t.parse("秋").value == "XXXX-FA"
    assert t.parse("冬").value == "XXXX-WI"

    assert t.parse("2021春").value == "2021-SP"
    assert t.parse("2021年春").value == "2021-SP"
    assert t.parse("2021/春").value == "2021-SP"

    # def test_quarter(t):
    assert t.parse("Q1").value == "XXXX-Q1"
    assert t.parse("Q2").value == "XXXX-Q2"
    assert t.parse("Q3").value == "XXXX-Q3"
    assert t.parse("Q4").value == "XXXX-Q4"
    assert t.parse("Q1").value == "XXXX-Q1"
    assert t.parse("第1四半期").value == "XXXX-Q1"

    assert t.parse("Q5") is None
    assert t.parse("10Q") is None
    assert t.parse("Q1Q") is None
    assert t.parse("第1四半") is None
    assert t.parse("1四半期") is None


def test_fiscal_year(t):
    assert t.parse("2021年度").value == "FY2021"

    # 西暦で2,3桁年度は表現しない
    assert t.parse("132年度") is None
    assert t.parse("32年度") is None


# def test_fiscal_year_wareki(t):
#     assert t.parse("令和3年度").value == "FYR03"


def test_ac_century(t):
    assert t.parse("1世紀").value == "00XX"  # 西暦1年から西暦100年
    assert t.parse("9世紀").value == "08XX"  # 西暦801年から西暦900年
    assert t.parse("11世紀").value == "10XX"  # 西暦1001年から西暦1100年
    assert t.parse("21世紀").value == "20XX"  # 西暦2001年から西暦2100年


def test_bc_year(t):
    assert t.parse("紀元前1年").value == "BC0001"
    assert t.parse("紀元前202年").value == "BC0202"
    assert t.parse("紀元前2000年").value == "BC2000"


def test_bc_century(t):
    assert t.parse("紀元前1世紀").value == "BC00XX"
    assert t.parse("紀元前2世紀").value == "BC01XX"
    assert t.parse("紀元前21世紀").value == "BC20XX"


# def test_(t):
#     t.parse("").value == ""
