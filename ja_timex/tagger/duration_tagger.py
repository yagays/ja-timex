import re
from typing import Dict

from ja_timex.tag import TIMEX
from ja_timex.tagger.duration_pattern import patterns


def detect_format(args: Dict) -> str:
    """正規表現patternから抽出したフォーマットを判定する

    p : 日付表現 (年/月/週/日)
    pt: 時間表現 (時間/分/秒)

    Args:
        args (Dict): 正規表現パターンのgroupdict()

    Raises:
        ValueError: どのパターンにも判定されなかった場合

    Returns:
        str: 判定したフォーマット
    """

    if "year" in args:
        return "p"
    elif "month" in args:
        return "p"
    elif "day" in args:
        return "p"
    elif "century" in args:
        return "p"
    elif "week" in args:
        return "p"
    elif "hour" in args:
        return "pt"
    elif "minutes" in args:
        return "pt"
    elif "second" in args:
        return "pt"
    elif "second_with_ms" in args:
        return "pt"
    else:
        raise ValueError


def construct_duration_timex(re_match, pattern):
    args = re_match.groupdict()
    span = re_match.span()
    value_format = detect_format(args)

    if value_format == "p":
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
            value_from_surface=value,
            text=re_match.group(),
            value_format="p",
            parsed=args,
            span=span,
        )
    elif value_format == "pt":
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
            value_from_surface=value,
            text=re_match.group(),
            value_format="pt",
            parsed=args,
            span=span,
        )


class DurationTagger:
    def __init__(self) -> None:
        self.patterns = patterns

    def parse(self, text: str) -> TIMEX:
        result = None

        # preprocess text
        text = text.strip()

        for pattern in self.patterns:
            re_match = re.fullmatch(pattern["pattern"], text)
            if re_match:
                result = construct_duration_timex(re_match, pattern)
        return result

    def parse_with_pattern(self, re_match, pattern):
        return construct_duration_timex(re_match, pattern)


if __name__ == "__main__":
    duration_tagger = DurationTagger()
