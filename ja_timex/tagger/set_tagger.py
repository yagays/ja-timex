import re

from ja_timex.tag import TIMEX
from ja_timex.tagger.set_pattern import patterns


class SetTagger:
    def __init__(self) -> None:
        self.patterns = patterns

    def parse(self, text: str) -> TIMEX:
        result = None

        # preprocess text
        text = text.strip()

        for pattern in self.patterns:
            re_match = re.fullmatch(pattern.re_pattern, text)
            if re_match:
                result = pattern.parse_func(re_match, pattern)
        return result

    def parse_with_pattern(self, re_match, pattern):
        return pattern.parse_func(re_match, pattern)


if __name__ == "__main__":
    set_tagger = SetTagger()
