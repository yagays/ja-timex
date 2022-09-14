import pendulum
import pytest

from ja_timex.tag import TIMEX


@pytest.fixture(scope="module")
def t_date():
    return TIMEX(
        type="DATE",
        value="2021-07-18",
        text="2021年07月18日",
        span=(0, 11),
        parsed={"calendar_year": "2021", "calendar_month": "07", "calendar_day": "18"},
    )


@pytest.fixture(scope="module")
def t_time():
    return TIMEX(
        type="TIME",
        value="T18-20-XX",
        text="18時20分",
        span=(0, 6),
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
    return TIMEX(type="DURATION", value="P1W", text="1週間", span=(0, 3), parsed={"week": 1})


@pytest.fixture(scope="module")
def t_set():
    return TIMEX(type="SET", value="P1W", text="週に1回", freq="1X", span=(0, 4), parsed={"range": "1", "count": "1"})


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
    date = TIMEX(type="DATE", tid="t0", value="2021-07-18", text="2021年07月18日", span=(0, 11))
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
        span=(0, 11),
        parsed={"calendar_year": "2021", "calendar_month": "07", "calendar_day": "18"},
    ).to_datetime()
    assert dt.year == 2021
    assert dt.month == 7
    assert dt.day == 18
    assert dt.hour == 0
    assert dt.minute == 0
    assert dt.second == 0

    dt = TIMEX(
        type="DATE",
        value="2021-07-XX",
        text="2021年07月",
        span=(0, 8),
        parsed={"calendar_year": "2021", "calendar_month": "07"},
    ).to_datetime()
    assert dt.year == 2021
    assert dt.month == 7
    assert dt.day == 1  # 補完された
    assert dt.hour == 0
    assert dt.minute == 0
    assert dt.second == 0

    dt = TIMEX(
        type="DATE",
        value="XXXX-07-18",
        text="7月18日",
        span=(0, 5),
        parsed={"calendar_month": "07", "calendar_day": "18"},
    ).to_datetime()
    assert dt.year == pendulum.now().year  # 補完された年
    assert dt.month == 7
    assert dt.day == 18
    assert dt.hour == 0
    assert dt.minute == 0
    assert dt.second == 0


def test_to_datetime_half():
    dt = TIMEX(
        type="TIME",
        value="T20-30-XX",
        text="20時半",
        span=(0, 4),
        parsed={"clock_hour": "20", "half_suffix": "半", "clock_minute": "XX", "clock_second": "XX"},
        reference=pendulum.now(),
    ).to_datetime()
    assert dt.hour == 20
    assert dt.minute == 30
    assert dt.second == 0


def test_is_valid_duration(t_date, t_time, t_duration, t_set):
    assert t_duration.is_valid_duration

    # 他の時間情報の場合
    assert not t_date.is_valid_duration
    assert not t_time.is_valid_duration
    assert not t_set.is_valid_duration

    # parsedが無いとFalseになる
    assert not TIMEX(type="DURATION", value="P1W", text="1週間", span=(0, 3)).is_valid_duration


def test_to_duration():
    it = TIMEX(type="DURATION", value="P1Y", text="1年間", span=(0, 3), parsed={"year": "1"}).to_duration()
    assert it.years == 1
    assert it.months == 0
    assert it.days == 365  # 日付換算

    it = TIMEX(type="DURATION", value="P1W", text="1週間", span=(0, 3), parsed={"week": "1"}).to_duration()
    assert it.weeks == 1
    assert it.days == 7  # 日付換算

    it = TIMEX(type="DURATION", value="PT1H", text="1時間", span=(0, 3), parsed={"hour": "1"}).to_duration()
    assert it.hours == 1
    assert it.minutes == 0
    assert it.seconds == 3600  # 秒換算

    it = TIMEX(type="DURATION", value="PT1.5S", text="1.5秒", span=(0, 4), parsed={"second": "1.5"}).to_duration()
    assert it.minutes == 0
    assert it.seconds == 1
    assert it.microseconds == 500000  # マイクロ秒


def test_reltime_to_duration_word():
    # 昨年や先週などの単語表現
    it = TIMEX(type="DURATION", value="P1Y", text="昨年", span=(0, 2), parsed={"year": "1"}).to_duration()
    assert it.years == 1

    it = TIMEX(type="DURATION", value="P2M", text="先々月", span=(0, 3), parsed={"month": "2"}).to_duration()
    assert it.months == 2

    it = TIMEX(type="DURATION", value="P1W", text="先週", span=(0, 2), parsed={"week": "1"}).to_duration()
    assert it.weeks == 1


def test_reltime_to_duration_word_today():
    # 今日/今週/今月/今年といった今の表現はDuration()となり、すべて0になる
    it = TIMEX(type="DURATION", value="P0D", text="今日", span=(0, 2), parsed={"day": "0"}).to_duration()
    assert it.days == 0

    it = TIMEX(type="DURATION", value="P0W", text="今週", span=(0, 2), parsed={"week": "0"}).to_duration()
    assert it.weeks == 0

    it = TIMEX(type="DURATION", value="P0M", text="今月", span=(0, 2), parsed={"month": "0"}).to_duration()
    assert it.months == 0

    it = TIMEX(type="DURATION", value="P0Y", text="今月", span=(0, 2), parsed={"year": "0"}).to_duration()
    assert it.years == 0


def test_to_duration_half():
    it = TIMEX(
        type="DURATION",
        value="P1.5Y",
        text="1年半後",
        span=(0, 4),
        parsed={"year": "1", "half_suffix": "半", "after_suffix": "後"},
    ).to_duration()
    assert it.years == 1
    assert it.months == 6

    assert it.days == 545  # 365 + 30 * 6
    # pendulumは一律で1ヶ月を30日として計算する

    it = TIMEX(
        type="DURATION",
        value="P1.5M",
        text="1ヶ月半後",
        span=(0, 5),
        parsed={"month": "1", "half_suffix": "半", "after_suffix": "後"},
    ).to_duration()
    assert it.years == 0
    assert it.months == 1

    assert it.days == 45  # 30 + 15

    it = TIMEX(
        type="DURATION",
        value="PT1.5H",
        text="1時間半後",
        span=(0, 5),
        parsed={"hour": "1", "half_suffix": "半", "after_suffix": "後"},
    ).to_duration()
    assert it.hours == 1
    assert it.minutes == 30

    assert it.seconds == 5400  # 90*60


def test_duration_to_duration_half_expression_without_number():
    it = TIMEX(type="DURATION", value="P50Y", text="半世紀", span=(0, 3), parsed={"year": "50"}).to_duration()
    assert it.years == 50

    it = TIMEX(type="DURATION", value="P25Y", text="半世紀", span=(0, 3), parsed={"year": "25"}).to_duration()
    assert it.years == 25

    it = TIMEX(type="DURATION", value="P0.5Y", text="半年", span=(0, 2), parsed={"month": "6"}).to_duration()
    assert it.months == 6

    it = TIMEX(type="DURATION", value="P0.5M", text="半月", span=(0, 2), parsed={"day": "15"}).to_duration()
    assert it.days == 15

    it = TIMEX(type="DURATION", value="P0.5D", text="半日", span=(0, 2), parsed={"day": "0.5"}).to_duration()
    assert it.days == 0
    assert it.hours == 12


def test_reltime_to_duration_half_expression_without_number():
    it = TIMEX(
        type="DURATION",
        value="P50Y",
        text="半世紀前",
        mod="BEFORE",
        span=(0, 4),
        parsed={"before_suffix": "前", "year": "50"},
    ).to_duration()
    assert it.years == 50

    it = TIMEX(
        type="DURATION",
        value="P25Y",
        text="四半世紀後",
        mod="AFTER",
        span=(0, 5),
        parsed={"after_suffix": "後", "year": "25"},
    ).to_duration()
    assert it.years == 25

    it = TIMEX(
        type="DURATION",
        value="P0.5Y",
        text="半年前",
        mod="BEFORE",
        span=(0, 3),
        parsed={"before_suffix": "前", "month": "6"},
    ).to_duration()
    assert it.months == 6

    it = TIMEX(
        type="DURATION", value="P0.5M", text="半月後", mod="AFTER", span=(0, 3), parsed={"after_suffix": "後", "day": "15"}
    ).to_duration()
    assert it.days == 15

    it = TIMEX(
        type="DURATION",
        value="P0.5D",
        text="半日前",
        mod="BEFORE",
        span=(0, 3),
        parsed={"before_suffix": "前", "day": "0.5"},
    ).to_duration()
    assert it.days == 0
    assert it.hours == 12


def test_default_timezone():
    timex = TIMEX(
        type="DATE",
        value="2021-07-18",
        text="2021年07月18日",
        span=(0, 11),
        parsed={"calendar_year": "2021", "calendar_month": "07", "calendar_day": "18"},
    )

    # default
    assert timex.to_datetime().timezone == pendulum.timezone("Asia/Tokyo")

    # specify timezone
    assert timex.to_datetime(tz="UTC").timezone == pendulum.timezone("UTC")
    assert timex.to_datetime(tz="Europe/Paris").timezone == pendulum.timezone("Europe/Paris")
    assert timex.to_datetime(tz="Asia/Tokyo").timezone == pendulum.timezone("Asia/Tokyo")

    assert timex.to_datetime(tz=pendulum.timezone("UTC")).timezone == pendulum.timezone("UTC")
    assert timex.to_datetime(tz=pendulum.timezone("Asia/Tokyo")).timezone == pendulum.timezone("Asia/Tokyo")

    with pytest.raises(TypeError):
        timex.to_datetime(tz=None)
    with pytest.raises(TypeError):
        timex.to_datetime(tz=10)
