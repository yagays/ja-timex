import re

from ja_timex.tag import TIMEX
from ja_timex.tagger.set_pattern import patterns


def detect_format(args):
    if "count" in args:
        if args["range"] is None:
            return "count"
        else:
            return "count_range"
    # elif "month" in args:
    #     return "month"
    # elif "day" in args:
    #     return "day"
    # elif "century" in args:
    #     return "century"
    # elif "week" in args:
    #     return "week"
    # elif "hour" in args:
    #     return "hour"
    # elif "minutes" in args:
    #     return "minutes"
    # elif "second" in args:
    #     return "second"
    # elif "second_with_ms" in args:
    #     return "second_with_ms"
    else:
        raise ValueError


def construct_set_timex(re_match, pattern):
    args = re_match.groupdict()
    value_format = detect_format(args)

    if value_format == "count_range":
        value = pattern["value_template"].format(args["range"])
        freq = pattern["freq_template"].format(args["count"])
        return TIMEX(
            type="SET",
            value=value,
            value_from_surface=re_match.group(),
            freq=freq,
            value_format="count",
            parsed=args,
        )
    if value_format == "count":
        value = pattern["value_template"].format("1")
        freq = pattern["freq_template"].format(args["count"])
        return TIMEX(
            type="SET",
            value=value,
            value_from_surface=re_match.group(),
            freq=freq,
            value_format="count",
            parsed=args,
        )


class SetTagger:
    def __init__(self) -> None:
        pass

    def parse(self, text: str) -> TIMEX:
        result = None

        # preprocess text
        text = text.strip()

        for pattern in patterns:
            re_match = re.fullmatch(pattern["pattern"], text)
            if re_match:
                result = construct_set_timex(re_match, pattern)
        return result


if __name__ == "__main__":
    reltime_tagger = SetTagger()