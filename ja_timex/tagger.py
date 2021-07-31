import re
from typing import List, Optional

from ja_timex.pattern.abstime import patterns as abstime_patterns
from ja_timex.pattern.duration import patterns as duration_patterns
from ja_timex.pattern.place import Pattern
from ja_timex.pattern.reltime import patterns as reltime_patterns
from ja_timex.pattern.set import patterns as set_patterns
from ja_timex.tag import TIMEX


class BaseTagger:
    def __init__(self, patterns=None) -> None:
        self.patterns = patterns

    def parse(self, text: str) -> Optional[TIMEX]:
        """すべてのPatternを用いてパースする

        入力文字列に対して、すべてのパータンをチェックして結果をTIMEX形式に変換する。
        任意のTagger単体で実行するときに利用する。

        Args:
            text (str): 入力文字列

        Returns:
            Optional[TIMEX]: 抽出された時間情報表現
        """
        results = []

        # preprocess text
        text = text.strip()

        for pattern in self.patterns:
            re_match = re.fullmatch(pattern.re_pattern, text)
            if re_match:
                results.append(pattern.parse_func(re_match, pattern))

        if len(results) > 0:
            # 2件以上該当した場合には、先に判定したものを優先する
            return results[0]
        else:
            return None

    def parse_with_pattern(self, re_match, pattern):
        return pattern.parse_func(re_match, pattern)


class AbstimeTagger(BaseTagger):
    def __init__(self, patterns: List[Pattern] = abstime_patterns) -> None:
        self.patterns = patterns


class DurationTagger(BaseTagger):
    def __init__(self, patterns: List[Pattern] = duration_patterns) -> None:
        self.patterns = patterns


class ReltimeTagger(BaseTagger):
    def __init__(self, patterns: List[Pattern] = reltime_patterns) -> None:
        self.patterns = patterns


class SetTagger(BaseTagger):
    def __init__(self, patterns: List[Pattern] = set_patterns) -> None:
        self.patterns = patterns
