from typing import List

from ja_timex.tagger.base_tagger import BaseTagger
from ja_timex.tagger.place import Pattern
from ja_timex.tagger.reltime_pattern import patterns


class ReltimeTagger(BaseTagger):
    def __init__(self, patterns: List[Pattern] = patterns) -> None:
        self.patterns = patterns


if __name__ == "__main__":
    reltime_tagger = ReltimeTagger()
