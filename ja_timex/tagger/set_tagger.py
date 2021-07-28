from typing import List

from ja_timex.tagger.base_tagger import BaseTagger
from ja_timex.tagger.place import Pattern
from ja_timex.tagger.set_pattern import patterns


class SetTagger(BaseTagger):
    def __init__(self, patterns: List[Pattern] = patterns) -> None:
        self.patterns = patterns


if __name__ == "__main__":
    set_tagger = SetTagger()
