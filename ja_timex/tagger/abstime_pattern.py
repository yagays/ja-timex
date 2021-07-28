from ja_timex.tag import TIMEX
from ja_timex.tagger.place import Pattern, Place

weekday2id = {"月": "1", "火": "2", "水": "3", "木": "4", "金": "5", "土": "6", "日": "7"}
season2id = {"春": "SP", "夏": "SU", "秋": "FA", "冬": "WI"}


def get_weekday_id(text: str) -> str:
    return weekday2id[text]


def get_season_id(text: str) -> str:
    return season2id[text]


def parse_absdate(re_match, pattern):
    args = re_match.groupdict()
    span = re_match.span()

    # fill unknown position by "X"

    if "calendar_year" not in args:
        args["calendar_year"] = "XXXX"
    if "calendar_month" not in args:
        args["calendar_month"] = "XX"
    if "calendar_day" not in args:
        args["calendar_day"] = "XX"
    # zero padding
    args["calendar_year"] = args["calendar_year"].zfill(4)
    args["calendar_month"] = args["calendar_month"].zfill(2)
    args["calendar_day"] = args["calendar_day"].zfill(2)

    additional_info = None
    if "weekday" in args:
        additional_info = {"weekday_text": args["weekday"], "weekday_id": get_weekday_id(args["weekday"])}

    return TIMEX(
        type="DATE",
        value=f'{args["calendar_year"]}-{args["calendar_month"]}-{args["calendar_day"]}',
        value_from_surface=f'{args["calendar_year"]}-{args["calendar_month"]}-{args["calendar_day"]}',
        text=re_match.group(),
        value_format="absdate",
        parsed=args,
        additional_info=additional_info,
        span=span,
    )


def parse_weekday(re_match, pattern):
    args = re_match.groupdict()
    span = re_match.span()

    weekday_id = get_weekday_id(args["weekday"])
    calendar_week = "XX"
    value = f"XXXX-W{calendar_week}-{weekday_id}"
    return TIMEX(
        type="DATE",
        value=value,
        value_from_surface=value,
        text=re_match.group(),
        value_format="weekday",
        parsed=args,
        span=span,
    )


def parse_season(re_match, pattern):
    args = re_match.groupdict()
    span = re_match.span()

    season_id = get_season_id(args["season"])
    if "calendar_year" in args and args["calendar_year"]:
        year = args["calendar_year"].zfill(4)
    else:
        year = "XXXX"
    value = f"{year}-{season_id}"
    return TIMEX(
        type="DATE",
        value=value,
        value_from_surface=value,
        text=re_match.group(),
        value_format="season",
        parsed=args,
        span=span,
    )


def parse_quarter(re_match, pattern):
    args = re_match.groupdict()
    span = re_match.span()

    quarter_id = args["quarter"]
    value = f"XXXX-Q{quarter_id}"
    return TIMEX(
        type="DATE",
        value=value,
        value_from_surface=value,
        text=re_match.group(),
        value_format="quarter",
        parsed=args,
        span=span,
    )


def parse_fiscal_year(re_match, pattern):
    args = re_match.groupdict()
    span = re_match.span()

    fiscal_year = args["fiscal_year"]
    value = f"FY{fiscal_year}"
    return TIMEX(
        type="DATE",
        value=value,
        value_from_surface=value,
        text=re_match.group(),
        value_format="fiscal_year",
        parsed=args,
        span=span,
    )


def parse_ac_century(re_match, pattern):
    args = re_match.groupdict()
    span = re_match.span()

    century_num = int(args["ac_century"])
    century_range = f"{century_num - 1}" + "XX"
    value = century_range.zfill(4)
    return TIMEX(
        type="DATE",
        value=value,
        value_from_surface=value,
        text=re_match.group(),
        value_format="century",
        parsed=args,
        span=span,
    )


def parse_bc_year(re_match, pattern):
    args = re_match.groupdict()
    span = re_match.span()

    bc_year = args["bc_year"]
    value = f"BC{bc_year.zfill(4)}"
    return TIMEX(
        type="DATE",
        value=value,
        value_from_surface=value,
        text=re_match.group(),
        value_format="bc_year",
        parsed=args,
        span=span,
    )


def parse_bc_century(re_match, pattern):
    args = re_match.groupdict()
    span = re_match.span()

    century_num = int(args["bc_century"])
    century_range = f"{century_num - 1}" + "XX"
    value = "BC" + century_range.zfill(4)
    return TIMEX(
        type="DATE",
        value=value,
        value_from_surface=value,
        text=re_match.group(),
        value_format="bc_century",
        parsed=args,
        span=span,
    )


p = Place()
patterns = []


# 日付
date_templates = [
    f"{p.calendar_year}年{p.calendar_month}月{p.calendar_day}日",
    f"{p.calendar_month}月{p.calendar_day}日",  # 年は表現できる範囲が広いため、年/月より月/日を優先する
    f"{p.calendar_year}年{p.calendar_month}月",
    f"{p.calendar_year}年",
    f"{p.calendar_month}月",
    f"{p.calendar_day}日",
]
for delimiter in ["/", "\-", "\.", "・", ","]:
    date_templates.append(f"{p.calendar_year}年?{delimiter}{p.calendar_month}月?{delimiter}{p.calendar_day}日?")
    date_templates.append(f"{p.calendar_month}月?{delimiter}{p.calendar_day}日?")
    date_templates.append(f"{p.calendar_year}年?{delimiter}{p.calendar_month}月?")

# 日付がある表記には曜日が記載される場合がある
date_templates += [
    f"{p.calendar_year}年{p.calendar_month}月{p.calendar_day}日{p.weekday_with_symbol}",
    f"{p.calendar_month}月{p.calendar_day}日{p.weekday_with_symbol}",
    f"{p.calendar_day}日{p.weekday_with_symbol}",
]
for delimiter in ["/", "\-", "\.", "・", ","]:
    date_templates.append(
        f"{p.calendar_year}年?{delimiter}{p.calendar_month}月?{delimiter}{p.calendar_day}日?{p.weekday_with_symbol}"
    )
    date_templates.append(f"{p.calendar_month}月?{delimiter}{p.calendar_day}日?{p.weekday_with_symbol}")


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
        re_pattern=p.weekday_with_symbol,
        parse_func=parse_weekday,
        option={},
    ),
    Pattern(
        re_pattern=f"({p.calendar_year}[年|/]?)?{p.season}",
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
        re_pattern=p.fiscal_year,
        parse_func=parse_fiscal_year,
        option={},
    ),
    Pattern(
        re_pattern=p.ac_century,
        parse_func=parse_ac_century,
        option={},
    ),
    Pattern(
        re_pattern=p.bc_year,
        parse_func=parse_bc_year,
        option={},
    ),
    Pattern(
        re_pattern=p.bc_century,
        parse_func=parse_bc_century,
        option={},
    ),
]
