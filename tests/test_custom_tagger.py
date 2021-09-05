import re
from typing import List

import pytest

from ja_timex.pattern.place import Pattern
from ja_timex.tag import TIMEX
from ja_timex.tagger import BaseTagger
from ja_timex.timex import TimexParser


@pytest.fixture(scope="module")
def p():
    # Custom Taggerで必要となる要素と、TimexParserの指定

    def parse_kouki(re_match: re.Match, pattern: Pattern) -> TIMEX:
        args = re_match.groupdict()
        span = re_match.span()

        year = int(args["calendar_year"]) - 660
        return TIMEX(
            type="DATE",
            value=f"{year}-XX-XX",
            text=re_match.group(),
            mod=pattern.option.get("mod"),
            parsed=args,
            span=span,
            pattern=pattern,
        )

    custom_pattern = [
        Pattern(
            re_pattern="皇紀(?P<calendar_year>[0-9]{1,4})年",
            parse_func=parse_kouki,
            option={},
        )
    ]

    class CustomTagger(BaseTagger):
        def __init__(self, patterns: List[Pattern] = custom_pattern) -> None:
            self.patterns = patterns

    return TimexParser(custom_tagger=CustomTagger())


def test_custom_tagger_kouki(p):
    # Custom Taggerあり
    timexes = p.parse("西暦2021年は皇紀2681年です")
    assert len(timexes) == 2

    assert timexes[0].value == "2021-XX-XX"
    assert timexes[0].text == "西暦2021年"

    assert timexes[1].value == "2021-XX-XX"
    assert timexes[1].text == "皇紀2681年"
    assert timexes[1].parsed == {"calendar_year": "2681"}


def test_without_custom_tagger():
    # Custom Taggerなし
    p = TimexParser()
    timexes = p.parse("西暦2021年は皇紀2681年です")
    assert len(timexes) == 2

    assert timexes[0].value == "2021-XX-XX"
    assert timexes[0].text == "西暦2021年"

    # そのまま2681年と解釈される
    assert timexes[1].value == "2681-XX-XX"
    assert timexes[1].text == "2681年"
    assert timexes[1].parsed == {"calendar_day": "XX", "calendar_month": "XX", "calendar_year": "2681"}
