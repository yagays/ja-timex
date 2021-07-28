from ja_timex.tagger.base_tagger import BaseTagger
from ja_timex.tagger.duration_pattern import patterns


class DurationTagger(BaseTagger):
    def __init__(self, patterns=patterns) -> None:
        self.patterns = patterns


if __name__ == "__main__":
    duration_tagger = DurationTagger()
