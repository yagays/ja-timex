import re

from ja_timex.pattern.place import Pattern, Place
from ja_timex.tag import TIMEX


def parse_p(re_match: re.Match, pattern: Pattern) -> TIMEX:
    args = re_match.groupdict()
    span = re_match.span()

    # 日付を表す持続時間表現の場合
    value = "P"
    if "year" in args:
        value += args["year"] + "Y"
    if "month" in args:
        value += args["month"] + "M"
    if "week" in args:
        value += args["week"] + "W"
    if "day" in args:
        value += args["day"] + "D"

    return TIMEX(
        type="DURATION",
        value=value,
        text=re_match.group(),
        parsed=args,
        span=span,
        pattern=pattern,
    )


def parse_pt(re_match: re.Match, pattern: Pattern) -> TIMEX:
    args = re_match.groupdict()
    span = re_match.span()

    # 時間を表す持続時間表現の場合
    value = "PT"
    if "hour" in args:
        value += args["hour"] + "H"
    if "minutes" in args:
        value += args["minutes"] + "M"
    if "second" in args:
        value += args["second"] + "S"
    if "second_with_ms" in args:
        value += args["second_with_ms"].replace("秒", ".") + "S"

    return TIMEX(
        type="DURATION",
        value=value,
        text=re_match.group(),
        parsed=args,
        span=span,
        pattern=pattern,
    )


p = Place()

patterns = []


# 年
patterns += [
    # P
    Pattern(
        re_pattern=f"{p.year}年(間)?",
        parse_func=parse_p,
        option={},
    ),
    Pattern(
        re_pattern=f"{p.month}[ヶ|か|カ|ケ|箇]?月(間)?",
        parse_func=parse_p,
        option={},
    ),
    Pattern(
        re_pattern=f"{p.week}週(間)?",
        parse_func=parse_p,
        option={},
    ),
    Pattern(
        re_pattern=f"{p.day}日(間)?",
        parse_func=parse_p,
        option={},
    ),
    Pattern(
        re_pattern=f"{p.year}年{p.month}[ヶ|か|カ|ケ|箇]月(間)?",
        parse_func=parse_p,
        option={},
    ),
    Pattern(
        re_pattern=f"{p.year}年{p.month}[ヶ|か|カ|ケ|箇]月{p.day}日(間)?",
        parse_func=parse_p,
        option={},
    ),
    # PT
    Pattern(
        re_pattern=f"{p.hour}時間",
        parse_func=parse_pt,
        option={},
    ),
    Pattern(
        re_pattern=f"{p.minutes}分(間)?",
        parse_func=parse_pt,
        option={},
    ),
    Pattern(
        re_pattern=f"{p.second}秒(間)?",
        parse_func=parse_pt,
        option={},
    ),
    Pattern(
        re_pattern=f"{p.second_with_ms}",
        parse_func=parse_pt,
        option={},
    ),
    Pattern(
        re_pattern=f"{p.hour}時間{p.minutes}分(間)?",
        parse_func=parse_pt,
        option={},
    ),
    Pattern(
        re_pattern=f"{p.hour}時間{p.minutes}分{p.second}秒(間)?",
        parse_func=parse_pt,
        option={},
    ),
    Pattern(
        re_pattern=f"{p.minutes}分{p.second}秒(間)?",
        parse_func=parse_pt,
        option={},
    ),
]
