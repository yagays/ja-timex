import re

from ja_timex.tag import TIMEX
from ja_timex.tagger.duration_pattern import patterns


def construct_duration_timex(re_match, pattern):
    args = re_match.groupdict()
    return TIMEX(type="DURATION", value="1時間", value_from_surface=re_match.group(), value_format="season", parsed=args)


class DurationTagger:
    def __init__(self) -> None:
        pass

    def parse(self, text: str) -> TIMEX:
        result = None

        # preprocess text
        text = text.strip()

        for pattern in patterns:
            re_match = re.fullmatch(pattern["pattern"], text)
            if re_match:
                result = construct_duration_timex(re_match, pattern)
        return result


if __name__ == "__main__":
    abstime_tagger = DurationTagger()
