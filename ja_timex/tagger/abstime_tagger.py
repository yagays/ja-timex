import re
from typing import Optional

from ja_timex.tag import TIMEX
from ja_timex.tagger.abstime_pattern import patterns, season2id, weekday2id


def get_weekday_id(text: str) -> str:
    return weekday2id[text]


def get_season_id(text: str) -> str:
    return season2id[text]


def detect_format(args):
    if "season" in args:
        # yearを含む可能性があるので、最初に判定する
        return "season"
    elif "quarter" in args:
        return "quarter"
    elif "calendar_year" in args or "calendar_month" in args or "calendar_day" in args:
        return "absdate"
    elif "weekday" in args:
        # 曜日のみの場合
        return "weekday"
    elif "fiscal_year" in args:
        return "fiscal_year"
    elif "century" in args:
        return "century"
    elif "bc_year" in args:
        return "bc_year"
    elif "bc_century" in args:
        return "bc_century"
    else:
        raise ValueError


def construct_timex(re_match, pattern):
    args = re_match.groupdict()
    value_format = detect_format(args)

    if value_format == "absdate":
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
            value_from_surface=re_match.group(),
            value_format="absdate",
            parsed=args,
            additional_info=additional_info,
        )
    elif value_format == "weekday":
        weekday_id = get_weekday_id(args["weekday"])
        calendar_week = "XX"
        value = f"XXXX-W{calendar_week}-{weekday_id}"
        return TIMEX(type="DATE", value=value, value_from_surface=re_match.group(), value_format="weekday", parsed=args)
    elif value_format == "season":
        season_id = get_season_id(args["season"])
        if "calendar_year" in args and args["calendar_year"]:
            year = args["calendar_year"].zfill(4)
        else:
            year = "XXXX"
        value = f"{year}-{season_id}"
        return TIMEX(type="DATE", value=value, value_from_surface=re_match.group(), value_format="season", parsed=args)
    elif value_format == "quarter":
        quarter_id = args["quarter"]
        value = f"XXXX-Q{quarter_id}"
        return TIMEX(type="DATE", value=value, value_from_surface=re_match.group(), value_format="quarter", parsed=args)
    elif value_format == "fiscal_year":
        fiscal_year = args["fiscal_year"]
        value = f"FY{fiscal_year}"
        return TIMEX(
            type="DATE", value=value, value_from_surface=re_match.group(), value_format="fiscal_year", parsed=args
        )
    elif value_format == "century":
        century_num = int(args["century"])
        century_range = f"{century_num - 1}" + "XX"
        value = century_range.zfill(4)
        return TIMEX(type="DATE", value=value, value_from_surface=re_match.group(), value_format="century", parsed=args)
    elif value_format == "bc_year":
        bc_year = args["bc_year"]
        value = f"BC{bc_year.zfill(4)}"
        return TIMEX(type="DATE", value=value, value_from_surface=re_match.group(), value_format="bc_year", parsed=args)
    elif value_format == "bc_century":
        century_num = int(args["bc_century"])
        century_range = f"{century_num - 1}" + "XX"
        value = "BC" + century_range.zfill(4)
        return TIMEX(
            type="DATE", value=value, value_from_surface=re_match.group(), value_format="bc_century", parsed=args
        )


class AbstimeTagger:
    def __init__(self) -> None:
        self.patterns = patterns

    def parse(self, text: str) -> Optional[TIMEX]:
        results = []

        # preprocess text
        text = text.strip()

        for pattern in self.patterns:
            re_match = re.fullmatch(pattern["pattern"], text)
            if re_match:
                results.append(construct_timex(re_match, pattern))

        if len(results) > 0:
            # 2件以上該当した場合には、先に判定したものを優先する
            # testの `test_normal_date_multiple_detected()` を参考
            return results[0]
        else:
            return None

    def parse_with_pattern(self, re_match, pattern):
        return construct_timex(re_match, pattern)


if __name__ == "__main__":
    abstime_tagger = AbstimeTagger()
