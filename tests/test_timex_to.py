import pytest
import pendulum

from ja_timex.timex import TimexParser


@pytest.fixture(scope="module")
def p():
    return TimexParser()


# test_tag.pyでも同様にto_{datetime,duration}のテストを実施しているが、
# このテストではTIMEXを直に構築するのではなく、TimexParserで処理した結果のto_*をテストしている


def test_to_datetime(p):
    assert p.parse("開発を開始したのが2021年7月18日です")[0].to_datetime() == pendulum.datetime(
        year=2021, month=7, day=18, tz="Asia/Tokyo"
    )
    assert p.parse("開発を開始したのが2021年7月です")[0].to_datetime() == pendulum.datetime(
        year=2021, month=7, day=1, tz="Asia/Tokyo"
    )
    assert p.parse("開発を開始したのが7月18日です")[0].to_datetime() == pendulum.datetime(
        year=pendulum.now().year, month=7, day=18, tz="Asia/Tokyo"
    )


def test_to_duration(p):
    assert p.parse("1秒後")[0].to_duration() == pendulum.duration(seconds=1)
    assert p.parse("試験の100分前")[0].to_duration() == pendulum.duration(minutes=100)
    assert p.parse("あと2.5時間後")[0].to_duration() == pendulum.duration(hours=2.5)  # Duration(hours=2, minutes=30)
    assert p.parse("1日前には予想もしなかった")[0].to_duration() == pendulum.duration(days=1)
    assert p.parse("3週間後にはもう忘れている")[0].to_duration() == pendulum.duration(weeks=3)
    assert p.parse("1ヶ月前から準備している")[0].to_duration() == pendulum.duration(months=1)
    assert p.parse("1年前は平和だった")[0].to_duration() == pendulum.duration(years=1)


def test_to_duration_word(p):
    assert p.parse("昨日何食べた？")[0].to_duration() == pendulum.duration(days=1)
    assert p.parse("明々後日に決行する")[0].to_duration() == pendulum.duration(days=3)

    assert p.parse("あれから半月は経った")[0].to_duration() == pendulum.duration(days=15)
    assert p.parse("もう半年は何もできない状態")[0].to_duration() == pendulum.duration(months=6)
    assert p.parse("半世紀にわたる貢献")[0].to_duration() == pendulum.duration(years=50)
