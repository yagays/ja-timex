import re

from ja_timex.pattern.place import Pattern, Place, get_season_id, get_wareki_first_year, get_weekday_id
from ja_timex.tag import TIMEX


def parse_absdate(re_match: re.Match, pattern: Pattern) -> TIMEX:
    args = re_match.groupdict()
    span = re_match.span()

    # fill unknown position by "X"
    if "calendar_year" not in args:
        args["calendar_year"] = "XXXX"
    if "calendar_month" not in args:
        args["calendar_month"] = "XX"
    if "calendar_day" not in args:
        args["calendar_day"] = "XX"

    # 和暦を西暦に変換
    if args.get("wareki_prefix"):
        if args["calendar_year_wareki"] == "元":
            wareki_year = 1
        else:
            wareki_year = int(args["calendar_year_wareki"])
        args["calendar_year"] = str(wareki_year + get_wareki_first_year(args["wareki_prefix"]))

    # zero padding
    args["calendar_year"] = args["calendar_year"].zfill(4)
    args["calendar_month"] = args["calendar_month"].zfill(2)
    args["calendar_day"] = args["calendar_day"].zfill(2)

    return TIMEX(
        type="DATE",
        value=f'{args["calendar_year"]}-{args["calendar_month"]}-{args["calendar_day"]}',
        text=re_match.group(),
        mod=pattern.option.get("mod"),
        parsed=args,
        span=span,
        pattern=pattern,
    )


def parse_weekday(re_match: re.Match, pattern: Pattern) -> TIMEX:
    args = re_match.groupdict()
    span = re_match.span()

    weekday_id = get_weekday_id(args["weekday"])
    calendar_week = "XX"
    return TIMEX(
        type="DATE",
        value=f"XXXX-W{calendar_week}-{weekday_id}",
        text=re_match.group(),
        mod=pattern.option.get("mod"),
        parsed=args,
        span=span,
        pattern=pattern,
    )


def parse_season(re_match: re.Match, pattern: Pattern) -> TIMEX:
    args = re_match.groupdict()
    span = re_match.span()

    season_id = get_season_id(args["season"])
    year = args["calendar_year"].zfill(4)
    return TIMEX(
        type="DATE", value=f"{year}-{season_id}", text=re_match.group(), parsed=args, span=span, pattern=pattern
    )


def parse_quarter(re_match: re.Match, pattern: Pattern) -> TIMEX:
    args = re_match.groupdict()
    span = re_match.span()

    quarter_id = args["quarter"]
    return TIMEX(
        type="DATE",
        value=f"XXXX-Q{quarter_id}",
        text=re_match.group(),
        mod=pattern.option.get("mod"),
        parsed=args,
        span=span,
        pattern=pattern,
    )


def parse_fiscal_year(re_match: re.Match, pattern: Pattern) -> TIMEX:
    args = re_match.groupdict()
    span = re_match.span()

    fiscal_year = args["fiscal_year"]
    return TIMEX(
        type="DATE",
        value=f"FY{fiscal_year}",
        text=re_match.group(),
        mod=pattern.option.get("mod"),
        parsed=args,
        span=span,
        pattern=pattern,
    )


def parse_ac_century(re_match: re.Match, pattern: Pattern) -> TIMEX:
    args = re_match.groupdict()
    span = re_match.span()

    century_num = int(args["ac_century"])
    century_range = f"{century_num - 1}" + "XX"
    value = century_range.zfill(4)
    return TIMEX(
        type="DATE",
        value=value,
        text=re_match.group(),
        mod=pattern.option.get("mod"),
        parsed=args,
        span=span,
        pattern=pattern,
    )


def parse_bc_year(re_match: re.Match, pattern: Pattern) -> TIMEX:
    args = re_match.groupdict()
    span = re_match.span()

    bc_year = args["bc_year"]
    value = "BC" + bc_year.zfill(4)
    return TIMEX(
        type="DATE",
        value=value,
        text=re_match.group(),
        mod=pattern.option.get("mod"),
        parsed=args,
        span=span,
        pattern=pattern,
    )


def parse_bc_century(re_match: re.Match, pattern: Pattern) -> TIMEX:
    args = re_match.groupdict()
    span = re_match.span()

    century_num = int(args["bc_century"])
    century_range = f"{century_num - 1}" + "XX"
    value = "BC" + century_range.zfill(4)
    return TIMEX(
        type="DATE",
        value=value,
        text=re_match.group(),
        mod=pattern.option.get("mod"),
        parsed=args,
        span=span,
        pattern=pattern,
    )


def parse_time(re_match: re.Match, pattern: Pattern) -> TIMEX:
    args = re_match.groupdict()
    span = re_match.span()

    # fill unknown position by "X"
    if "clock_hour" not in args:
        args["clock_hour"] = "XX"
    if "clock_minute" not in args:
        args["clock_minute"] = "XX"
    if "clock_second" not in args:
        args["clock_second"] = "XX"

    # zero padding
    hour = args["clock_hour"].zfill(2)
    minute = args["clock_minute"].zfill(2)
    second = args["clock_second"].zfill(2)

    # AM/PMを24時間表記に変更する
    if args.get("am_prefix") or args.get("am_suffix"):
        if hour == "12":
            hour = "00"
    if args.get("pm_prefix") or args.get("pm_suffix"):
        if hour != "XX" and 1 <= int(hour) <= 11:
            hour = str(int(hour) + 12)

    if args.get("evening_prefix"):
        if int(hour) <= 12:
            hour = str(int(hour) + 12)

    # 半
    if args.get("half_suffix"):
        minute = "30"

    return TIMEX(
        type="TIME",
        value=f"T{hour}-{minute}-{second}",
        text=re_match.group(),
        mod=pattern.option.get("mod"),
        parsed=args,
        span=span,
        pattern=pattern,
    )


p = Place()
patterns = []


# 日付
date_templates = [
    f"(西暦)?{p.calendar_year}年{p.calendar_month}月{p.calendar_day}日",
    f"{p.calendar_month}月{p.calendar_day}日",  # 年は表現できる範囲が広いため、年/月より月/日を優先する
    f"(西暦)?{p.calendar_year}年{p.calendar_month}月",
    f"(西暦)?{p.calendar_year}年",
    f"{p.calendar_month}月",
    f"{p.calendar_day}日",
    # 和暦
    f"{p.wareki_prefix}{p.calendar_year_wareki}年{p.calendar_month}月{p.calendar_day}日",
    f"{p.wareki_prefix}{p.calendar_year_wareki}年{p.calendar_month}月",
    f"{p.wareki_prefix}{p.calendar_year_wareki}年",
]
for delimiter in ["/", "\\-", "・"]:
    date_templates.append(f"(西暦)?{p.calendar_year}年?{delimiter}{p.calendar_month}月?{delimiter}{p.calendar_day}日?")
    date_templates.append(f"{p.calendar_month}月?{delimiter}{p.calendar_day}日?")
    date_templates.append(f"(西暦)?{p.calendar_year}年?{delimiter}{p.calendar_month}月?")
    # 和暦
    date_templates.append(
        f"{p.wareki_prefix}{p.calendar_year_wareki}年?{delimiter}{p.calendar_month}月?{delimiter}{p.calendar_day}日?"
    )
    date_templates.append(f"{p.wareki_prefix}{p.calendar_year_wareki}年?{delimiter}{p.calendar_month}月?")

for delimiter in ["\\.", ","]:
    # 数字が2つの表現は小数点や列挙と混同するため、取得対象とはしない
    date_templates.append(f"(西暦)?{p.calendar_year}年?{delimiter}{p.calendar_month}月?{delimiter}{p.calendar_day}日?")
    # 和暦
    date_templates.append(
        f"{p.wareki_prefix}{p.calendar_year_wareki}年?{delimiter}{p.calendar_month}月?{delimiter}{p.calendar_day}日?"
    )
    date_templates.append(f"{p.wareki_prefix}{p.calendar_year_wareki}年?{delimiter}{p.calendar_month}月?")

for date_template in date_templates:
    patterns.append(
        Pattern(
            re_pattern=date_template,
            parse_func=parse_absdate,
            option={},
        )
    )


# 曜日
patterns += [
    Pattern(
        re_pattern=p.weekday_without_symbol,
        parse_func=parse_weekday,
        option={},
    ),
    Pattern(
        re_pattern=p.weekday_with_symbol,
        parse_func=parse_weekday,
        option={},
    ),
    Pattern(
        re_pattern=f"{p.calendar_year}[年|/]?{p.season}",
        parse_func=parse_season,
        option={},
    ),
    Pattern(
        re_pattern=f"(第{p.quarter}四半期)",
        parse_func=parse_quarter,
        option={},
    ),
    Pattern(
        re_pattern=f"(Q{p.quarter})",
        parse_func=parse_quarter,
        option={},
    ),
    Pattern(
        re_pattern=f"({p.quarter}Q)",
        parse_func=parse_quarter,
        option={},
    ),
    Pattern(
        re_pattern=f"{p.fiscal_year}年度",
        parse_func=parse_fiscal_year,
        option={},
    ),
    Pattern(
        re_pattern=f"{p.ac_century}世紀",
        parse_func=parse_ac_century,
        option={},
    ),
    Pattern(
        re_pattern=f"紀元前{p.bc_year}年",
        parse_func=parse_bc_year,
        option={},
    ),
    Pattern(
        re_pattern=f"紀元前{p.bc_century}世紀",
        parse_func=parse_bc_century,
        option={},
    ),
]

# 時刻
patterns += [
    Pattern(
        re_pattern=f"{p.ampm_prefix}?{p.clock_hour}時{p.clock_minute}分{p.clock_second}秒",
        parse_func=parse_time,
        option={},
    ),
    Pattern(
        re_pattern=f"{p.ampm_prefix}?{p.clock_hour}時{p.clock_minute}分{p.ampm_suffix}?",
        parse_func=parse_time,
        option={},
    ),
    Pattern(
        re_pattern=f"{p.clock_minute}分{p.clock_second}秒",
        parse_func=parse_time,
        option={},
    ),
    Pattern(
        re_pattern=f"{p.ampm_prefix}?{p.clock_hour}時{p.half_suffix}?{p.ampm_suffix}?",
        parse_func=parse_time,
        option={},
    ),
    Pattern(
        re_pattern=f"{p.clock_minute}分",
        parse_func=parse_time,
        option={},
    ),
    Pattern(
        re_pattern=f"{p.clock_second}秒",
        parse_func=parse_time,
        option={},
    ),
    Pattern(
        re_pattern=f"{p.ampm_prefix}?{p.clock_hour}[:：]{p.clock_minute}[:：]{p.clock_second}{p.ampm_suffix}?",
        parse_func=parse_time,
        option={},
    ),
    Pattern(
        re_pattern=f"{p.ampm_prefix}?{p.clock_hour}[:：]{p.clock_minute}{p.ampm_suffix}?",
        parse_func=parse_time,
        option={},
    ),
    Pattern(
        re_pattern=f"{p.clock_minute}[:：]{p.clock_second}",
        parse_func=parse_time,
        option={},
    ),
    Pattern(
        re_pattern=f"{p.times_of_day_prefix}?{p.clock_hour}時{p.clock_minute}分{p.clock_second}秒",
        parse_func=parse_time,
        option={},
    ),
    Pattern(
        re_pattern=f"{p.times_of_day_prefix}?{p.clock_hour}時{p.clock_minute}分",
        parse_func=parse_time,
        option={},
    ),
    Pattern(
        re_pattern=f"{p.times_of_day_prefix}?{p.clock_hour}時{p.half_suffix}?",
        parse_func=parse_time,
        option={},
    ),
    Pattern(
        re_pattern=f"{p.times_of_day_prefix}?{p.clock_hour}[:：]{p.clock_minute}[:：]{p.clock_second}{p.ampm_suffix}?",
        parse_func=parse_time,
        option={},
    ),
    Pattern(
        re_pattern=f"{p.times_of_day_prefix}?{p.clock_hour}[:：]{p.clock_minute}{p.ampm_suffix}?",
        parse_func=parse_time,
        option={},
    ),
]

# @mod
mod2suffix = {
    "START": p.start_suffix,
    "MID": p.mid_suffix,
    "END": p.end_suffix,
    "APPROX": p.abstime_approx_suffix,
    "ON_OR_BEFORE": p.on_or_before_suffix,
    "ON_OR_AFTER": p.on_or_after_suffix,
}

for mod, suffix in mod2suffix.items():
    patterns += [
        Pattern(
            re_pattern=f"(西暦)?{p.calendar_year}年{p.calendar_month}月{suffix}",
            parse_func=parse_absdate,
            option={"mod": mod},
        ),
        Pattern(
            re_pattern=f"(西暦)?{p.calendar_year}年{suffix}",
            parse_func=parse_absdate,
            option={"mod": mod},
        ),
        Pattern(
            re_pattern=f"{p.calendar_month}月{suffix}",
            parse_func=parse_absdate,
            option={"mod": mod},
        ),
        Pattern(
            re_pattern=f"{p.wareki_prefix}{p.calendar_year_wareki}年{p.calendar_month}月{suffix}",
            parse_func=parse_absdate,
            option={"mod": mod},
        ),
        Pattern(
            re_pattern=f"{p.wareki_prefix}{p.calendar_year_wareki}年{suffix}",
            parse_func=parse_absdate,
            option={"mod": mod},
        ),
        Pattern(
            re_pattern=f"{p.ac_century}世紀{suffix}",
            parse_func=parse_ac_century,
            option={"mod": mod},
        ),
        Pattern(
            re_pattern=f"紀元前{p.bc_year}年{suffix}",
            parse_func=parse_bc_year,
            option={"mod": mod},
        ),
        Pattern(
            re_pattern=f"紀元前{p.bc_century}世紀{suffix}",
            parse_func=parse_bc_century,
            option={"mod": mod},
        ),
    ]
