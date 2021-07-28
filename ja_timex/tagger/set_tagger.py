from ja_timex.tagger.base_tagger import BaseTagger
from ja_timex.tagger.set_pattern import patterns


class SetTagger(BaseTagger):
    def __init__(self, patterns=patterns) -> None:
        self.patterns = patterns


if __name__ == "__main__":
    set_tagger = SetTagger()
