import re

from ja_timex.pattern.place import Pattern, Place
from ja_timex.tag import TIMEX


def parse_ac_century(re_match: re.Match, pattern: Pattern) -> TIMEX:
    args = re_match.groupdict()
    span = re_match.span()

    century_num = int(args["ac_century"])
    century_range = f"{century_num - 1}" + "XX"
    value = century_range.zfill(4)
    return TIMEX(
        type="DURATION",
        value=value,
        text=re_match.group(),
        mod=pattern.option.get("mod"),
        parsed=args,
        span=span,
        pattern=pattern,
    )


def parse_year(re_match: re.Match, pattern: Pattern) -> TIMEX:
    args = re_match.groupdict()
    span = re_match.span()

    value = args["year"]
    if args.get("half_suffix"):
        value += ".5"
    else:
        value += ""

    return TIMEX(
        type="DURATION",
        value=f"P{value}Y",
        text=re_match.group(),
        mod=pattern.option.get("mod"),
        parsed=args,
        span=span,
        pattern=pattern,
    )


def parse_month(re_match: re.Match, pattern: Pattern) -> TIMEX:
    args = re_match.groupdict()
    span = re_match.span()

    value = args["month"]
    if args.get("half_suffix"):
        value += ".5"
    else:
        value += ""

    return TIMEX(
        type="DURATION",
        value=f"P{value}M",
        text=re_match.group(),
        mod=pattern.option.get("mod"),
        parsed=args,
        span=span,
        pattern=pattern,
    )


def parse_day(re_match: re.Match, pattern: Pattern) -> TIMEX:
    args = re_match.groupdict()
    span = re_match.span()

    value = args["day"]
    if args.get("half_suffix"):
        value += ".5"
    else:
        value += ""

    return TIMEX(
        type="DURATION",
        value=f"P{value}D",
        text=re_match.group(),
        mod=pattern.option.get("mod"),
        parsed=args,
        span=span,
        pattern=pattern,
    )


def parse_hour(re_match: re.Match, pattern: Pattern) -> TIMEX:
    args = re_match.groupdict()
    span = re_match.span()

    value = args["hour"]
    if args.get("half_suffix"):
        value += ".5"
    else:
        value += ""

    return TIMEX(
        type="DURATION",
        value=f"PT{value}H",
        text=re_match.group(),
        mod=pattern.option.get("mod"),
        parsed=args,
        span=span,
        pattern=pattern,
    )


def parse_minute(re_match: re.Match, pattern: Pattern) -> TIMEX:
    args = re_match.groupdict()
    span = re_match.span()

    value = args["minute"]
    if args.get("half_suffix"):
        value += ".5"
    else:
        value += ""

    return TIMEX(
        type="DURATION",
        value=f"PT{value}M",
        text=re_match.group(),
        mod=pattern.option.get("mod"),
        parsed=args,
        span=span,
        pattern=pattern,
    )


def parse_second(re_match: re.Match, pattern: Pattern) -> TIMEX:
    args = re_match.groupdict()
    span = re_match.span()

    value = args["second"]
    if args.get("half_suffix"):
        value += ".5"
    else:
        value += ""

    return TIMEX(
        type="DURATION",
        value=f"PT{value}S",
        text=re_match.group(),
        mod=pattern.option.get("mod"),
        parsed=args,
        span=span,
        pattern=pattern,
    )


def parse_second_with_ms(re_match: re.Match, pattern: Pattern) -> TIMEX:
    args = re_match.groupdict()
    span = re_match.span()

    value = args["second_with_ms"].replace("???", ".")
    return TIMEX(
        type="DURATION",
        value=f"PT{value}S",
        text=re_match.group(),
        mod=pattern.option.get("mod"),
        parsed=args,
        span=span,
        pattern=pattern,
    )


def parse_week(re_match: re.Match, pattern: Pattern) -> TIMEX:
    args = re_match.groupdict()
    span = re_match.span()

    value = args["week"]
    if args.get("half_suffix"):
        value += ".5"
    else:
        value += ""

    return TIMEX(
        type="DURATION",
        value=f"P{value}W",
        text=re_match.group(),
        mod=pattern.option.get("mod"),
        parsed=args,
        span=span,
        pattern=pattern,
    )


def parse_word(re_match: re.Match, pattern: Pattern) -> TIMEX:
    args = re_match.groupdict()
    span = re_match.span()

    value = pattern.option["value"]
    # "???"???????????????????????????args????????????
    for unit in ["century", "year", "month", "week", "day"]:
        if pattern.option.get(unit):
            args[unit] = pattern.option[unit]

    return TIMEX(
        type="DURATION",
        value=value,
        text=re_match.group(),
        mod=pattern.option.get("mod"),
        parsed=args,
        span=span,
        pattern=pattern,
    )


p = Place()

patterns = []


# ???
patterns += [
    Pattern(
        re_pattern=f"{p.year}???{p.half_suffix}?{p.around_suffix}?{p.before_suffix}",
        parse_func=parse_year,
        option={"mod": "BEFORE"},
    ),
    Pattern(
        re_pattern=f"{p.year}???{p.half_suffix}?{p.around_suffix}?{p.after_suffix}",
        parse_func=parse_year,
        option={"mod": "AFTER"},
    ),
    Pattern(
        re_pattern=f"{p.year}???{p.half_suffix}?{p.approx_suffix}",
        parse_func=parse_year,
        option={"mod": "APPROX"},
    ),
    Pattern(re_pattern=f"{p.year}???{p.half_suffix}?{p.just_suffix}", parse_func=parse_year, option={}),
]

# ???
patterns += [
    Pattern(
        re_pattern=f"{p.month}[???|???|???|???|???]???{p.half_suffix}?{p.around_suffix}?{p.before_suffix}",
        parse_func=parse_month,
        option={"mod": "BEFORE"},
    ),
    Pattern(
        re_pattern=f"{p.month}[???|???|???|???|???]???{p.half_suffix}?{p.around_suffix}?{p.after_suffix}",
        parse_func=parse_month,
        option={"mod": "AFTER"},
    ),
    Pattern(
        re_pattern=f"{p.month}[???|???|???|???|???]???{p.half_suffix}?{p.approx_suffix}",
        parse_func=parse_month,
        option={"mod": "APPROX"},
    ),
    Pattern(
        re_pattern=f"{p.month}[???|???|???|???|???]???{p.half_suffix}?{p.just_suffix}",
        parse_func=parse_month,
        option={},
    ),
]


# ???
patterns += [
    Pattern(
        re_pattern=f"{p.day}???{p.half_suffix}?{p.around_suffix}?{p.before_suffix}",
        parse_func=parse_day,
        option={"mod": "BEFORE"},
    ),
    Pattern(
        re_pattern=f"{p.day}???{p.half_suffix}?{p.around_suffix}?{p.after_suffix}",
        parse_func=parse_day,
        option={"mod": "AFTER"},
    ),
    Pattern(
        re_pattern=f"{p.day}???{p.half_suffix}?{p.approx_suffix}",
        parse_func=parse_day,
        option={"mod": "APPROX"},
    ),
    Pattern(re_pattern=f"{p.day}???{p.half_suffix}?{p.just_suffix}", parse_func=parse_day, option={}),
]

# ??????
patterns += [
    Pattern(
        re_pattern=f"{p.ac_century}??????{p.around_suffix}?{p.before_suffix}",
        parse_func=parse_ac_century,
        option={"mod": "BEFORE"},
    ),
    Pattern(
        re_pattern=f"{p.ac_century}??????{p.around_suffix}?{p.after_suffix}",
        parse_func=parse_ac_century,
        option={"mod": "AFTER"},
    ),
    Pattern(
        re_pattern=f"{p.ac_century}??????{p.approx_suffix}",
        parse_func=parse_ac_century,
        option={"mod": "APPROX"},
    ),
    Pattern(re_pattern=f"{p.ac_century}??????{p.just_suffix}", parse_func=parse_ac_century, option={}),
]

# ???
patterns += [
    Pattern(
        re_pattern=f"{p.week}???(???)?{p.half_suffix}?{p.around_suffix}?{p.before_suffix}",
        parse_func=parse_week,
        option={"mod": "BEFORE"},
    ),
    Pattern(
        re_pattern=f"{p.week}???(???)?{p.half_suffix}?{p.around_suffix}?{p.after_suffix}",
        parse_func=parse_week,
        option={"mod": "AFTER"},
    ),
    Pattern(
        re_pattern=f"{p.week}???(???)?{p.half_suffix}?{p.approx_suffix}",
        parse_func=parse_week,
        option={"mod": "APPROX"},
    ),
    Pattern(re_pattern=f"{p.week}???(???)?{p.half_suffix}?{p.just_suffix}", parse_func=parse_week, option={}),
]

# ??????
patterns += [
    Pattern(
        re_pattern=f"{p.hour}??????{p.half_suffix}?{p.around_suffix}?{p.before_suffix}",
        parse_func=parse_hour,
        option={"mod": "BEFORE"},
    ),
    Pattern(
        re_pattern=f"{p.hour}??????{p.half_suffix}?{p.around_suffix}?{p.after_suffix}",
        parse_func=parse_hour,
        option={"mod": "AFTER"},
    ),
    Pattern(
        re_pattern=f"{p.hour}??????{p.half_suffix}?{p.approx_suffix}",
        parse_func=parse_hour,
        option={"mod": "APPROX"},
    ),
]

# ???
patterns += [
    Pattern(
        re_pattern=f"{p.minute}???{p.half_suffix}?{p.around_suffix}?{p.before_suffix}",
        parse_func=parse_minute,
        option={"mod": "BEFORE"},
    ),
    Pattern(
        re_pattern=f"{p.minute}???{p.half_suffix}?{p.around_suffix}?{p.after_suffix}",
        parse_func=parse_minute,
        option={"mod": "AFTER"},
    ),
    Pattern(
        re_pattern=f"{p.minute}???{p.half_suffix}?{p.approx_suffix}",
        parse_func=parse_minute,
        option={"mod": "APPROX"},
    ),
]

# ???
patterns += [
    Pattern(
        re_pattern=f"{p.second}???{p.half_suffix}?{p.around_suffix}?{p.before_suffix}",
        parse_func=parse_second,
        option={"mod": "BEFORE"},
    ),
    Pattern(
        re_pattern=f"{p.second}???{p.half_suffix}?{p.around_suffix}?{p.after_suffix}",
        parse_func=parse_second,
        option={"mod": "AFTER"},
    ),
    Pattern(
        re_pattern=f"{p.second}???{p.half_suffix}?{p.approx_suffix}",
        parse_func=parse_second,
        option={"mod": "APPROX"},
    ),
]

# ????????????
# ???
patterns += [
    Pattern(
        re_pattern="[?????????]???",
        parse_func=parse_word,
        option={"value": "P1D", "mod": "BEFORE", "day": "1"},
    ),
    Pattern(
        re_pattern="?????????",
        parse_func=parse_word,
        option={"value": "P2D", "mod": "BEFORE", "day": "2"},
    ),
    Pattern(
        re_pattern="??????[??????]???",
        parse_func=parse_word,
        option={"value": "P3D", "mod": "BEFORE", "day": "3"},
    ),
    Pattern(
        re_pattern="[??????]???",
        parse_func=parse_word,
        option={"value": "P1D", "mod": "AFTER", "day": "1"},
    ),
    Pattern(
        re_pattern="(??????|??????)???",
        parse_func=parse_word,
        option={"value": "P2D", "mod": "AFTER", "day": "2"},
    ),
    Pattern(
        re_pattern="???[??????]??????",
        parse_func=parse_word,
        option={"value": "P3D", "mod": "AFTER", "day": "3"},
    ),
]

# ???
patterns += [
    Pattern(
        re_pattern="[?????????]???",
        parse_func=parse_word,
        option={"value": "P1W", "mod": "BEFORE", "week": "1"},
    ),
    Pattern(
        re_pattern="?????????",
        parse_func=parse_word,
        option={"value": "P2W", "mod": "BEFORE", "week": "2"},
    ),
    Pattern(
        re_pattern="[??????]???",
        parse_func=parse_word,
        option={"value": "P1W", "mod": "AFTER", "week": "1"},
    ),
    Pattern(
        re_pattern="(??????|??????)???",
        parse_func=parse_word,
        option={"value": "P2W", "mod": "AFTER", "week": "2"},
    ),
]

# ???
patterns += [
    Pattern(
        re_pattern="[?????????]???",
        parse_func=parse_word,
        option={"value": "P1M", "mod": "BEFORE", "month": "1"},
    ),
    Pattern(
        re_pattern="?????????",
        parse_func=parse_word,
        option={"value": "P2M", "mod": "BEFORE", "month": "2"},
    ),
    Pattern(
        re_pattern="[??????]???",
        parse_func=parse_word,
        option={"value": "P1M", "mod": "AFTER", "month": "1"},
    ),
    Pattern(
        re_pattern="(??????|??????)???",
        parse_func=parse_word,
        option={"value": "P2M", "mod": "AFTER", "month": "2"},
    ),
]

# ???
patterns += [
    Pattern(
        re_pattern="[?????????]???",
        parse_func=parse_word,
        option={"value": "P1Y", "mod": "BEFORE", "year": "1"},
    ),
    Pattern(
        re_pattern="(?????????|????????????)",
        parse_func=parse_word,
        option={"value": "P2Y", "mod": "BEFORE", "year": "2"},
    ),
    Pattern(
        re_pattern="[??????]???",
        parse_func=parse_word,
        option={"value": "P1Y", "mod": "AFTER", "year": "1"},
    ),
    Pattern(
        re_pattern="(??????|??????)???",
        parse_func=parse_word,
        option={"value": "P2Y", "mod": "AFTER", "year": "2"},
    ),
]

# ??????????????????
patterns += [
    Pattern(
        re_pattern="[??????]???",
        parse_func=parse_word,
        option={"value": "P0D", "mod": "NOW", "day": "0"},
    ),
    Pattern(
        re_pattern="??????",
        parse_func=parse_word,
        option={"value": "P0W", "mod": "NOW", "week": "0"},
    ),
    Pattern(
        re_pattern="??????",
        parse_func=parse_word,
        option={"value": "P0M", "mod": "NOW", "month": "0"},
    ),
    Pattern(
        re_pattern="??????",
        parse_func=parse_word,
        option={"value": "P0Y", "mod": "NOW", "year": "0"},
    ),
    Pattern(
        re_pattern="?????????",
        parse_func=parse_word,
        option={"value": "P0Y", "mod": "NOW", "year": "0"},
    ),
]

# ??????????????????
patterns += [
    Pattern(
        re_pattern=f"??????{p.around_suffix}?{p.before_suffix}",
        parse_func=parse_word,
        option={"value": "P0.5Y", "mod": "BEFORE", "month": "6"},
    ),
    Pattern(
        re_pattern=f"??????{p.around_suffix}?{p.after_suffix}",
        parse_func=parse_word,
        option={"value": "P0.5Y", "mod": "AFTER", "month": "6"},
    ),
    Pattern(
        re_pattern=f"??????{p.around_suffix}?{p.before_suffix}",
        parse_func=parse_word,
        option={"value": "P0.5M", "mod": "BEFORE", "day": "15"},
    ),
    Pattern(
        re_pattern=f"??????{p.around_suffix}?{p.after_suffix}",
        parse_func=parse_word,
        option={"value": "P0.5M", "mod": "AFTER", "day": "15"},
    ),
    Pattern(
        re_pattern=f"??????{p.around_suffix}?{p.before_suffix}",
        parse_func=parse_word,
        option={"value": "P0.5D", "mod": "BEFORE", "day": "0.5"},
    ),
    Pattern(
        re_pattern=f"??????{p.around_suffix}?{p.after_suffix}",
        parse_func=parse_word,
        option={"value": "P0.5D", "mod": "AFTER", "day": "0.5"},
    ),
    Pattern(
        re_pattern=f"?????????{p.around_suffix}?{p.before_suffix}",
        parse_func=parse_word,
        option={"value": "P50Y", "mod": "BEFORE", "year": "50"},
    ),
    Pattern(
        re_pattern=f"?????????{p.around_suffix}?{p.after_suffix}",
        parse_func=parse_word,
        option={"value": "P50Y", "mod": "AFTER", "year": "50"},
    ),
    Pattern(
        re_pattern=f"????????????{p.around_suffix}?{p.before_suffix}",
        parse_func=parse_word,
        option={"value": "P25Y", "mod": "BEFORE", "year": "25"},
    ),
    Pattern(
        re_pattern=f"????????????{p.around_suffix}?{p.after_suffix}",
        parse_func=parse_word,
        option={"value": "P25Y", "mod": "AFTER", "year": "25"},
    ),
]
