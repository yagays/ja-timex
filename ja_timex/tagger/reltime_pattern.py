import re

from ja_timex.tag import TIMEX
from ja_timex.tagger.place import Pattern, Place


def parse_century(re_match: re.Match, pattern: Pattern) -> TIMEX:
    args = re_match.groupdict()
    span = re_match.span()

    century_num = int(args["accentury"])
    century_range = f"{century_num - 1}" + "XX"
    value = century_range.zfill(4)
    f"{century_num - 1}" + "XX"
    return TIMEX(
        type="TIME",
        value=value,
        value_from_surface=value,
        text=re_match.group(),
        mod=pattern.option["mod"],
        value_format="century",
        parsed=args,
        span=span,
    )


def parse_year(re_match: re.Match, pattern: Pattern) -> TIMEX:
    args = re_match.groupdict()
    span = re_match.span()

    value = args["year"]
    return TIMEX(
        type="TIME",
        value=f"P{value}Y",
        value_from_surface=f"P{value}Y",
        text=re_match.group(),
        mod=pattern.option["mod"],
        value_format="year",
        parsed=args,
        span=span,
    )


def parse_month(re_match: re.Match, pattern: Pattern) -> TIMEX:
    args = re_match.groupdict()
    span = re_match.span()

    value = args["month"]
    return TIMEX(
        type="TIME",
        value=f"P{value}M",
        value_from_surface=f"P{value}M",
        text=re_match.group(),
        mod=pattern.option["mod"],
        value_format="month",
        parsed=args,
        span=span,
    )


def parse_day(re_match: re.Match, pattern: Pattern) -> TIMEX:
    args = re_match.groupdict()
    span = re_match.span()

    value = args["day"]
    return TIMEX(
        type="TIME",
        value=f"P{value}D",
        value_from_surface=f"P{value}D",
        text=re_match.group(),
        mod=pattern.option["mod"],
        value_format="day",
        parsed=args,
        span=span,
    )


def parse_hour(re_match: re.Match, pattern: Pattern) -> TIMEX:
    args = re_match.groupdict()
    span = re_match.span()

    value = args["hour"]
    return TIMEX(
        type="TIME",
        value=f"PT{value}H",
        value_from_surface=f"PT{value}H",
        text=re_match.group(),
        mod=pattern.option["mod"],
        value_format="hour",
        parsed=args,
        span=span,
    )


def parse_minutes(re_match: re.Match, pattern: Pattern) -> TIMEX:
    args = re_match.groupdict()
    span = re_match.span()

    value = args["minutes"]
    return TIMEX(
        type="TIME",
        value=f"PT{value}M",
        value_from_surface=f"PT{value}M",
        text=re_match.group(),
        mod=pattern.option["mod"],
        value_format="minutes",
        parsed=args,
        span=span,
    )


def parse_second(re_match: re.Match, pattern: Pattern) -> TIMEX:
    args = re_match.groupdict()
    span = re_match.span()

    value = args["second"]
    return TIMEX(
        type="TIME",
        value=f"PT{value}S",
        value_from_surface=f"PT{value}S",
        text=re_match.group(),
        mod=pattern.option["mod"],
        value_format="second",
        parsed=args,
        span=span,
    )


def parse_second_with_ms(re_match: re.Match, pattern: Pattern) -> TIMEX:
    args = re_match.groupdict()
    span = re_match.span()

    value = args["second_with_ms"].replace("秒", ".")
    return TIMEX(
        type="TIME",
        value=f"PT{value}S",
        value_from_surface=f"PT{value}S",
        text=re_match.group(),
        mod=pattern.option["mod"],
        value_format="second_with_ms",
        parsed=args,
        span=span,
    )


def parse_week(re_match: re.Match, pattern: Pattern) -> TIMEX:
    args = re_match.groupdict()
    span = re_match.span()

    value = args["week"]
    return TIMEX(
        week="TIME",
        value=f"P{value}W",
        value_from_surface=f"P{value}W",
        text=re_match.group(),
        mod=pattern.option["mod"],
        value_format="week",
        parsed=args,
        span=span,
    )


p = Place()

patterns = []


# 年
patterns += [
    Pattern(
        re_pattern=f"{p.year}年{p.around_prefix}?(前|まえ)",
        parse_func=parse_year,
        option={"mod": "BEFORE"},
    ),
    Pattern(
        re_pattern=f"{p.year}年{p.around_prefix}?(後|あと)",
        parse_func=parse_year,
        option={"mod": "AFTER"},
    ),
    Pattern(
        re_pattern=f"{p.year}年(はじめ|初め|始め|初頭|初期|前半|前記|頭)",
        parse_func=parse_year,
        option={"mod": "START"},
    ),
    Pattern(
        re_pattern=f"{p.year}年(なかば|半ば|中ごろ|中頃|中盤|中旬|中期|頭)",
        parse_func=parse_year,
        option={"mod": "MID"},
    ),
    Pattern(
        re_pattern=f"{p.year}年(後半|後期|終盤|終わり|末)",
        parse_func=parse_year,
        option={"mod": "END"},
    ),
    Pattern(
        re_pattern=f"{p.year}年([こご]ろ|頃|近く|前後|くらい|ばかり)",
        parse_func=parse_year,
        option={"mod": "APPROX"},
    ),
]

# 月
patterns += [
    Pattern(
        re_pattern=f"{p.month}月{p.around_prefix}?(前|まえ)",
        parse_func=parse_month,
        option={"mod": "BEFORE"},
    ),
    Pattern(
        re_pattern=f"{p.month}月{p.around_prefix}?(後|あと)",
        parse_func=parse_month,
        option={"mod": "AFTER"},
    ),
]


# 日
patterns += [
    Pattern(
        re_pattern=f"{p.day}日{p.around_prefix}?(前|まえ)",
        parse_func=parse_day,
        option={"mod": "BEFORE"},
    ),
    Pattern(
        re_pattern=f"{p.day}日{p.around_prefix}?(後|あと)",
        parse_func=parse_day,
        option={"mod": "AFTER"},
    ),
]

# 世紀
patterns += [
    Pattern(
        re_pattern=f"{p.ac_century}世紀{p.around_prefix}?(前|まえ)",
        parse_func=parse_century,
        option={"mod": "BEFORE"},
    ),
    Pattern(
        re_pattern=f"{p.ac_century}世紀{p.around_prefix}?(後|あと)",
        parse_func=parse_century,
        option={"mod": "AFTER"},
    ),
]

# 週
patterns += [
    Pattern(
        re_pattern=f"{p.week}日{p.around_prefix}?(前|まえ)",
        parse_func=parse_week,
        option={"mod": "BEFORE"},
    ),
    Pattern(
        re_pattern=f"{p.week}日{p.around_prefix}?(後|あと)",
        parse_func=parse_week,
        option={"mod": "AFTER"},
    ),
]

# 時間
patterns += [
    Pattern(
        re_pattern=f"{p.hour}日{p.around_prefix}?(前|まえ)",
        parse_func=parse_hour,
        option={"mod": "BEFORE"},
    ),
    Pattern(
        re_pattern=f"{p.hour}日{p.around_prefix}?(後|あと)",
        parse_func=parse_hour,
        option={"mod": "AFTER"},
    ),
]

# 分
patterns += [
    Pattern(
        re_pattern=f"{p.minutes}日{p.around_prefix}?(前|まえ)",
        parse_func=parse_minutes,
        option={"mod": "BEFORE"},
    ),
    Pattern(
        re_pattern=f"{p.minutes}日{p.around_prefix}?(後|あと)",
        parse_func=parse_minutes,
        option={"mod": "AFTER"},
    ),
]

# 秒
patterns += [
    Pattern(
        re_pattern=f"{p.second}日{p.around_prefix}?(前|まえ)",
        parse_func=parse_second,
        option={"mod": "BEFORE"},
    ),
    Pattern(
        re_pattern=f"{p.second}日{p.around_prefix}?(後|あと)",
        parse_func=parse_second,
        option={"mod": "AFTER"},
    ),
]


# {"pattern":"以前", "process_type":"or_less"}
# {"pattern":"まで", "process_type":"made"}
# {"pattern":"迄", "process_type":"or_less"}
# {"pattern":"より前", "process_type":"less"}
# {"pattern":"以降", "process_type":"or_over"}
# {"pattern":"より後", "process_type":"over"}
# {"pattern":"~", "process_type":"kara_suffix"}
# {"pattern":"〜", "process_type":"kara_suffix"}
# {"pattern":"～", "process_type":"kara_suffix"}
# {"pattern":"-", "process_type":"kara_suffix"}
# {"pattern":"−", "process_type":"kara_suffix"}
# {"pattern":"ー", "process_type":"kara_suffix"}
# {"pattern":"から", "process_type":"kara_suffix"}
# {"pattern":"上旬", "process_type":"joujun"}
# {"pattern":"中旬", "process_type":"tyujun"}
# {"pattern":"下旬", "process_type":"gejun"}
# {"pattern":"PM", "process_type":"gogo"}
# {"pattern":"AM", "process_type":"gozen"}
# {"pattern":"ＰＭ", "process_type":"gogo"}
# {"pattern":"ＡＭ", "process_type":"gozen"}
# {"pattern":"PM", "process_type":"gogo"}
# {"pattern":"AM", "process_type":"gozen"}
# {"pattern":"　ＰＭ", "process_type":"gogo"}
# {"pattern":"　ＡＭ", "process_type":"gozen"}
