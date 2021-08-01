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
        mod=pattern.option["mod"],
        parsed=args,
        span=span,
        pattern=pattern,
    )


def parse_year(re_match: re.Match, pattern: Pattern) -> TIMEX:
    args = re_match.groupdict()
    span = re_match.span()

    value = args["year"]
    return TIMEX(
        type="DURATION",
        value=f"P{value}Y",
        text=re_match.group(),
        mod=pattern.option["mod"],
        parsed=args,
        span=span,
        pattern=pattern,
    )


def parse_month(re_match: re.Match, pattern: Pattern) -> TIMEX:
    args = re_match.groupdict()
    span = re_match.span()

    value = args["month"]
    return TIMEX(
        type="DURATION",
        value=f"P{value}M",
        text=re_match.group(),
        mod=pattern.option["mod"],
        parsed=args,
        span=span,
        pattern=pattern,
    )


def parse_day(re_match: re.Match, pattern: Pattern) -> TIMEX:
    args = re_match.groupdict()
    span = re_match.span()

    value = args["day"]
    return TIMEX(
        type="DURATION",
        value=f"P{value}D",
        text=re_match.group(),
        mod=pattern.option["mod"],
        parsed=args,
        span=span,
        pattern=pattern,
    )


def parse_hour(re_match: re.Match, pattern: Pattern) -> TIMEX:
    args = re_match.groupdict()
    span = re_match.span()

    value = args["hour"]
    return TIMEX(
        type="DURATION",
        value=f"PT{value}H",
        text=re_match.group(),
        mod=pattern.option["mod"],
        parsed=args,
        span=span,
        pattern=pattern,
    )


def parse_minutes(re_match: re.Match, pattern: Pattern) -> TIMEX:
    args = re_match.groupdict()
    span = re_match.span()

    value = args["minutes"]
    return TIMEX(
        type="DURATION",
        value=f"PT{value}M",
        text=re_match.group(),
        mod=pattern.option["mod"],
        parsed=args,
        span=span,
        pattern=pattern,
    )


def parse_second(re_match: re.Match, pattern: Pattern) -> TIMEX:
    args = re_match.groupdict()
    span = re_match.span()

    value = args["second"]
    return TIMEX(
        type="DURATION",
        value=f"PT{value}S",
        text=re_match.group(),
        mod=pattern.option["mod"],
        parsed=args,
        span=span,
        pattern=pattern,
    )


def parse_second_with_ms(re_match: re.Match, pattern: Pattern) -> TIMEX:
    args = re_match.groupdict()
    span = re_match.span()

    value = args["second_with_ms"].replace("秒", ".")
    return TIMEX(
        type="DURATION",
        value=f"PT{value}S",
        text=re_match.group(),
        mod=pattern.option["mod"],
        parsed=args,
        span=span,
        pattern=pattern,
    )


def parse_week(re_match: re.Match, pattern: Pattern) -> TIMEX:
    args = re_match.groupdict()
    span = re_match.span()

    value = args["week"]
    return TIMEX(
        type="DURATION",
        value=f"P{value}W",
        text=re_match.group(),
        mod=pattern.option["mod"],
        parsed=args,
        span=span,
        pattern=pattern,
    )


def parse_word(re_match: re.Match, pattern: Pattern) -> TIMEX:
    args = re_match.groupdict()
    span = re_match.span()

    value = pattern.option["value"]
    return TIMEX(
        type="DURATION",
        value=value,
        text=re_match.group(),
        mod=pattern.option["mod"],
        parsed=args,
        span=span,
        pattern=pattern,
    )


p = Place()

patterns = []


# 年
patterns += [
    Pattern(
        re_pattern=f"{p.year}年{p.around_suffix}?{p.before_suffix}",
        parse_func=parse_year,
        option={"mod": "BEFORE"},
    ),
    Pattern(
        re_pattern=f"{p.year}年{p.around_suffix}?{p.after_suffix}",
        parse_func=parse_year,
        option={"mod": "AFTER"},
    ),
    Pattern(
        re_pattern=f"{p.year}年{p.approx_suffix}",
        parse_func=parse_year,
        option={"mod": "APPROX"},
    ),
]

# 月
patterns += [
    Pattern(
        re_pattern=f"{p.month}[ヶ|か|カ|ケ|箇]月{p.around_suffix}?{p.before_suffix}",
        parse_func=parse_month,
        option={"mod": "BEFORE"},
    ),
    Pattern(
        re_pattern=f"{p.month}[ヶ|か|カ|ケ|箇]月{p.around_suffix}?{p.after_suffix}",
        parse_func=parse_month,
        option={"mod": "AFTER"},
    ),
    Pattern(
        re_pattern=f"{p.month}[ヶ|か|カ|ケ|箇]月{p.approx_suffix}",
        parse_func=parse_month,
        option={"mod": "APPROX"},
    ),
]


# 日
patterns += [
    Pattern(
        re_pattern=f"{p.day}日{p.around_suffix}?{p.before_suffix}",
        parse_func=parse_day,
        option={"mod": "BEFORE"},
    ),
    Pattern(
        re_pattern=f"{p.day}日{p.around_suffix}?{p.after_suffix}",
        parse_func=parse_day,
        option={"mod": "AFTER"},
    ),
    Pattern(
        re_pattern=f"{p.day}日{p.approx_suffix}",
        parse_func=parse_day,
        option={"mod": "APPROX"},
    ),
]

# 世紀
patterns += [
    Pattern(
        re_pattern=f"{p.ac_century}世紀{p.around_suffix}?{p.before_suffix}",
        parse_func=parse_ac_century,
        option={"mod": "BEFORE"},
    ),
    Pattern(
        re_pattern=f"{p.ac_century}世紀{p.around_suffix}?{p.after_suffix}",
        parse_func=parse_ac_century,
        option={"mod": "AFTER"},
    ),
    Pattern(
        re_pattern=f"{p.ac_century}世紀{p.approx_suffix}",
        parse_func=parse_ac_century,
        option={"mod": "APPROX"},
    ),
]

# 週
patterns += [
    Pattern(
        re_pattern=f"{p.week}週(間)?{p.around_suffix}?{p.before_suffix}",
        parse_func=parse_week,
        option={"mod": "BEFORE"},
    ),
    Pattern(
        re_pattern=f"{p.week}週(間)?{p.around_suffix}?{p.after_suffix}",
        parse_func=parse_week,
        option={"mod": "AFTER"},
    ),
    Pattern(
        re_pattern=f"{p.week}週(間)?{p.approx_suffix}",
        parse_func=parse_week,
        option={"mod": "APPROX"},
    ),
]

# 時間
patterns += [
    Pattern(
        re_pattern=f"{p.hour}時間{p.around_suffix}?{p.before_suffix}",
        parse_func=parse_hour,
        option={"mod": "BEFORE"},
    ),
    Pattern(
        re_pattern=f"{p.hour}時間{p.around_suffix}?{p.after_suffix}",
        parse_func=parse_hour,
        option={"mod": "AFTER"},
    ),
    Pattern(
        re_pattern=f"{p.hour}時間{p.approx_suffix}",
        parse_func=parse_hour,
        option={"mod": "APPROX"},
    ),
]

# 分
patterns += [
    Pattern(
        re_pattern=f"{p.minutes}分{p.around_suffix}?{p.before_suffix}",
        parse_func=parse_minutes,
        option={"mod": "BEFORE"},
    ),
    Pattern(
        re_pattern=f"{p.minutes}分{p.around_suffix}?{p.after_suffix}",
        parse_func=parse_minutes,
        option={"mod": "AFTER"},
    ),
    Pattern(
        re_pattern=f"{p.minutes}分{p.approx_suffix}",
        parse_func=parse_minutes,
        option={"mod": "APPROX"},
    ),
]

# 秒
patterns += [
    Pattern(
        re_pattern=f"{p.second}秒{p.around_suffix}?{p.before_suffix}",
        parse_func=parse_second,
        option={"mod": "BEFORE"},
    ),
    Pattern(
        re_pattern=f"{p.second}秒{p.around_suffix}?{p.after_suffix}",
        parse_func=parse_second,
        option={"mod": "AFTER"},
    ),
    Pattern(
        re_pattern=f"{p.second}秒{p.approx_suffix}",
        parse_func=parse_second,
        option={"mod": "APPROX"},
    ),
]

# 単語表現
# 日
patterns += [
    Pattern(
        re_pattern="[先前昨]日",
        parse_func=parse_word,
        option={"value": "P1D", "mod": "BEFORE"},
    ),
    Pattern(
        re_pattern="一昨日",
        parse_func=parse_word,
        option={"value": "P2D", "mod": "BEFORE"},
    ),
    Pattern(
        re_pattern="一昨[昨々]日",
        parse_func=parse_word,
        option={"value": "P3D", "mod": "BEFORE"},
    ),
    Pattern(
        re_pattern="[翌明]日",
        parse_func=parse_word,
        option={"value": "P1D", "mod": "AFTER"},
    ),
    Pattern(
        re_pattern="(翌々|明後)日",
        parse_func=parse_word,
        option={"value": "P2D", "mod": "AFTER"},
    ),
    Pattern(
        re_pattern="明[昨々]後日",
        parse_func=parse_word,
        option={"value": "P3D", "mod": "AFTER"},
    ),
]

# 週
patterns += [
    Pattern(
        re_pattern="[先前昨]週",
        parse_func=parse_word,
        option={"value": "P1W", "mod": "BEFORE"},
    ),
    Pattern(
        re_pattern="先々週",
        parse_func=parse_word,
        option={"value": "P2W", "mod": "BEFORE"},
    ),
    Pattern(
        re_pattern="[来翌]週",
        parse_func=parse_word,
        option={"value": "P1W", "mod": "AFTER"},
    ),
    Pattern(
        re_pattern="(再来|翌々)週",
        parse_func=parse_word,
        option={"value": "P2W", "mod": "AFTER"},
    ),
]

# 月
patterns += [
    Pattern(
        re_pattern="[先前昨]月",
        parse_func=parse_word,
        option={"value": "P1M", "mod": "BEFORE"},
    ),
    Pattern(
        re_pattern="先々月",
        parse_func=parse_word,
        option={"value": "P2M", "mod": "BEFORE"},
    ),
    Pattern(
        re_pattern="[来翌]月",
        parse_func=parse_word,
        option={"value": "P1M", "mod": "AFTER"},
    ),
    Pattern(
        re_pattern="(再来|翌々)月",
        parse_func=parse_word,
        option={"value": "P2M", "mod": "AFTER"},
    ),
]

# 年
patterns += [
    Pattern(
        re_pattern="(一昨年|おととし)",
        parse_func=parse_word,
        option={"value": "P2Y", "mod": "BEFORE"},
    ),
    Pattern(
        re_pattern="[去前昨]年",
        parse_func=parse_word,
        option={"value": "P1Y", "mod": "BEFORE"},
    ),
    Pattern(
        re_pattern="[来翌]年",
        parse_func=parse_word,
        option={"value": "P1Y", "mod": "AFTER"},
    ),
    Pattern(
        re_pattern="(再来|翌々)年",
        parse_func=parse_word,
        option={"value": "P2Y", "mod": "AFTER"},
    ),
]

# 今を表す言葉
patterns += [
    Pattern(
        re_pattern="[今本]日",
        parse_func=parse_word,
        option={"value": "P0D", "mod": "NOW"},
    ),
    Pattern(
        re_pattern="今週",
        parse_func=parse_word,
        option={"value": "P0W", "mod": "NOW"},
    ),
    Pattern(
        re_pattern="今月",
        parse_func=parse_word,
        option={"value": "P0M", "mod": "NOW"},
    ),
    Pattern(
        re_pattern="今年",
        parse_func=parse_word,
        option={"value": "P0Y", "mod": "NOW"},
    ),
    Pattern(
        re_pattern="[今本]日",
        parse_func=parse_word,
        option={"value": "P0D", "mod": "NOW"},
    ),
]
