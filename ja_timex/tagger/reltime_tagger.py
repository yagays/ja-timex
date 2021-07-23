import re

from ja_timex.tag import TIMEX
from ja_timex.tagger.reltime_pattern import patterns


def detect_format(args):
    if "year" in args:
        return "year"
    elif "month" in args:
        return "month"
    elif "day" in args:
        return "day"
    elif "century" in args:
        return "century"
    elif "week" in args:
        return "week"
    elif "hour" in args:
        return "hour"
    elif "minutes" in args:
        return "minutes"
    elif "second" in args:
        return "second"
    elif "second_with_ms" in args:
        return "second_with_ms"
    else:
        raise ValueError


def construct_reltime_timex(re_match, pattern):
    args = re_match.groupdict()
    value_format = detect_format(args)

    if value_format == "year":
        value = args["year"]
        return TIMEX(
            type="TIME",
            value=f"P{value}Y",
            value_from_surface=re_match.group(),
            mod=pattern["mod"],
            value_format="year",
            parsed=args,
        )
    if value_format == "month":
        value = args["month"]
        return TIMEX(
            type="TIME",
            value=f"P{value}M",
            value_from_surface=re_match.group(),
            mod=pattern["mod"],
            value_format="month",
            parsed=args,
        )
    if value_format == "day":
        value = args["day"]
        return TIMEX(
            type="TIME",
            value=f"P{value}D",
            value_from_surface=re_match.group(),
            mod=pattern["mod"],
            value_format="day",
            parsed=args,
        )
    if value_format == "hour":
        value = args["hour"]
        return TIMEX(
            type="TIME",
            value=f"PT{value}H",
            value_from_surface=re_match.group(),
            mod=pattern["mod"],
            value_format="hour",
            parsed=args,
        )
    if value_format == "minutes":
        value = args["minutes"]
        return TIMEX(
            type="TIME",
            value=f"PT{value}M",
            value_from_surface=re_match.group(),
            mod=pattern["mod"],
            value_format="minutes",
            parsed=args,
        )
    if value_format == "second":
        value = args["second"]
        return TIMEX(
            type="TIME",
            value=f"PT{value}S",
            value_from_surface=re_match.group(),
            mod=pattern["mod"],
            value_format="second",
            parsed=args,
        )
    if value_format == "second_with_ms":
        value = args["second_with_ms"].replace("秒", ".")
        return TIMEX(
            type="TIME",
            value=f"PT{value}S",
            value_from_surface=re_match.group(),
            mod=pattern["mod"],
            value_format="second_with_ms",
            parsed=args,
        )
    if value_format == "week":
        value = args["week"]
        return TIMEX(
            week="TIME",
            value=f"P{value}W",
            value_from_surface=re_match.group(),
            mod=pattern["mod"],
            value_format="week",
            parsed=args,
        )


class ReltimeTagger:
    def __init__(self) -> None:
        self.patterns = patterns

    def parse(self, text: str) -> TIMEX:
        result = None

        # preprocess text
        text = text.strip()

        for pattern in self.patterns:
            re_match = re.fullmatch(pattern["pattern"], text)
            if re_match:
                result = construct_reltime_timex(re_match, pattern)
        return result

    def parse_with_pattern(self, re_match, pattern):
        return construct_reltime_timex(re_match, pattern)


if __name__ == "__main__":
    reltime_tagger = ReltimeTagger()
