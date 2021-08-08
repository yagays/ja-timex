import pytest

from ja_timex.tag import TIMEX


@pytest.fixture(scope="module")
def t_date():
    return TIMEX(
        type="DATE",
        value="2021-07-18",
        text="2021年07月18日",
        parsed={"calendar_year": "2021", "calendar_month": "07", "calendar_day": "18"},
    )


@pytest.fixture(scope="module")
def t_time():
    return TIMEX(
        type="TIME",
        value="T18-20-XX",
        text="18時20分",
        parsed={
            "am_prefix": "",
            "pm_prefix": None,
            "clock_hour": "18",
            "clock_minute": "20",
            "am_suffix": None,
            "pm_suffix": None,
            "clock_second": "XX",
        },
    )


@pytest.fixture(scope="module")
def t_duration():
    return TIMEX(type="DURATION", value="P1W", text="1週間", parsed={"week": 1})


@pytest.fixture(scope="module")
def t_set():
    return TIMEX(type="SET", value="P1W", text="週に1回", freq="1X", parsed={"range": "1", "count": "1"})


def test_to_tag_date(t_date):
    assert t_date.to_tag() == '<TIMEX3 type="DATE" value="2021-07-18">2021年07月18日</TIMEX3>'


def test_to_tag_time(t_time):
    assert t_time.to_tag() == '<TIMEX3 type="TIME" value="T18-20-XX">18時20分</TIMEX3>'


def test_to_tag_duration(t_duration):
    assert t_duration.to_tag() == '<TIMEX3 type="DURATION" value="P1W">1週間</TIMEX3>'


def test_to_tag_set(t_set):
    assert t_set.to_tag() == '<TIMEX3 type="SET" value="P1W" freq="1X">週に1回</TIMEX3>'


def test_tid():
    # tidは文脈情報を利用してTimexParser.parse()内の後処理で付与されるため、Optional[str]としている
    date = TIMEX(type="DATE", tid="t0", value="2021-07-18", text="2021年07月18日")
    assert date.to_tag() == '<TIMEX3 tid="t0" type="DATE" value="2021-07-18">2021年07月18日</TIMEX3>'


def test_is_valid_datetime(t_date, t_time, t_duration, t_set):

    assert t_date.is_valid_datetime
    assert t_time.is_valid_datetime
    assert t_duration.is_valid_datetime
    assert not t_set.is_valid_datetime


def test_to_datetime():
    dt = TIMEX(
        type="DATE",
        value="2021-07-18",
        text="2021年07月18日",
        parsed={"calendar_year": "2021", "calendar_month": "07", "calendar_day": "18"},
    ).to_datetime()
    assert dt.year == 2021
    assert dt.month == 7
    assert dt.day == 18
    assert dt.hour == 0
    assert dt.minute == 0
    assert dt.second == 0

    dt = TIMEX(
        type="DATE", value="2021-07-XX", text="2021年07月", parsed={"calendar_year": "2021", "calendar_month": "07"}
    ).to_datetime()
    assert dt.year == 2021
    assert dt.month == 7
    assert dt.day == 1  # 補完された
    assert dt.hour == 0
    assert dt.minute == 0
    assert dt.second == 0

    dt = TIMEX(
        type="DATE", value="XXXX-07-18", text="7月18日", parsed={"calendar_month": "07", "calendar_day": "18"}
    ).to_datetime()
    assert dt.year == 2021  # 補完された
    assert dt.month == 7
    assert dt.day == 18
    assert dt.hour == 0
    assert dt.minute == 0
    assert dt.second == 0


def test_is_valid_duration(t_date, t_time, t_duration, t_set):
    assert t_duration.is_valid_duration

    # 他の時間情報の場合
    assert not t_date.is_valid_duration
    assert not t_time.is_valid_duration
    assert not t_set.is_valid_duration

    # parsedが無いとFalseになる
    assert not TIMEX(type="DURATION", value="P1W", text="1週間").is_valid_duration


def test_to_duration():
    it = TIMEX(type="DURATION", value="P1Y", text="1年間", parsed={"year": 1}).to_duration()
    assert it.years == 1
    assert it.months == 0
    assert it.days == 365  # 日付換算

    it = TIMEX(type="DURATION", value="P1W", text="1週間", parsed={"week": 1}).to_duration()
    assert it.weeks == 1
    assert it.days == 7  # 日付換算

    it = TIMEX(type="DURATION", value="PT1H", text="1時間", parsed={"hour": 1}).to_duration()
    assert it.hours == 1
    assert it.minutes == 0
    assert it.seconds == 3600  # 秒換算

    it = TIMEX(type="DURATION", value="PT1.5S", text="1.5秒", parsed={"second": 1.5}).to_duration()
    assert it.minutes == 0
    assert it.seconds == 1
    assert it.microseconds == 500000  # マイクロ秒


def test_to_duration_half():
    it = TIMEX(
        type="DURATION", value="P1.5Y", text="1年半後", parsed={"year": "1", "half_suffix": "半", "after_suffix": "後"}
    ).to_duration()
    assert it.years == 1
    assert it.months == 6

    assert it.days == 545  # 365 + 30 * 6
    # pendulumは一律で1ヶ月を30日として計算する

    it = TIMEX(
        type="DURATION", value="P1.5M", text="1ヶ月半後", parsed={"month": "1", "half_suffix": "半", "after_suffix": "後"}
    ).to_duration()
    assert it.years == 0
    assert it.months == 1

    assert it.days == 45  # 30 + 15

    it = TIMEX(
        type="DURATION", value="PT1.5H", text="1時間半後", parsed={"hour": "1", "half_suffix": "半", "after_suffix": "後"}
    ).to_duration()
    assert it.hours == 1
    assert it.minutes == 30

    assert it.seconds == 5400  # 90*60
