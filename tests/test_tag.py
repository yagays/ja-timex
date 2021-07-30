from ja_timex.tag import TIMEX


def test_to_tag_date():
    date = TIMEX(type="DATE", value="2021-07-18", text="2021年07月18日")
    assert date.to_tag() == '<TIMEX3 type="DATE" value="2021-07-18">2021年07月18日</TIMEX3>'


def test_to_tag_time():
    date = TIMEX(type="TIME", value="PT1H", text="1時間前")
    assert date.to_tag() == '<TIMEX3 type="TIME" value="PT1H">1時間前</TIMEX3>'


def test_to_tag_duration():
    date = TIMEX(type="DURATION", value="P1W", text="1週間")
    assert date.to_tag() == '<TIMEX3 type="DURATION" value="P1W">1週間</TIMEX3>'


def test_to_tag_set():
    date = TIMEX(type="SET", value="P1W", text="週に1回", freq="1X")
    assert date.to_tag() == '<TIMEX3 type="SET" value="P1W" freq="1X">週に1回</TIMEX3>'


def test_tid():
    # tidは文脈情報を利用してTimexParser.parse()内の後処理で付与されるため、Optional[str]としている
    date = TIMEX(type="DATE", tid="t0", value="2021-07-18", text="2021年07月18日")
    assert date.to_tag() == '<TIMEX3 tid="t0" type="DATE" value="2021-07-18">2021年07月18日</TIMEX3>'
