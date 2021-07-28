from typing import List

from ja_timex.tagger.abstime_pattern import patterns
from ja_timex.tagger.base_tagger import BaseTagger
from ja_timex.tagger.place import Pattern


class AbstimeTagger(BaseTagger):
    def __init__(self, patterns: List[Pattern] = patterns) -> None:
        self.patterns = patterns


if __name__ == "__main__":
    abstime_tagger = AbstimeTagger()
