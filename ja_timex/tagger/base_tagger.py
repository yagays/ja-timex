import re

from ja_timex.tag import TIMEX


class BaseTagger:
    def __init__(self, patterns=None) -> None:
        self.patterns = patterns

    def parse(self, text: str) -> TIMEX:
        results = []

        # preprocess text
        text = text.strip()

        for pattern in self.patterns:
            re_match = re.fullmatch(pattern.re_pattern, text)
            if re_match:
                results.append(pattern.parse_func(re_match, pattern))

        if len(results) > 0:
            # 2件以上該当した場合には、先に判定したものを優先する
            # testの `test_normal_date_multiple_detected()` を参考
            return results[0]
        else:
            return None

    def parse_with_pattern(self, re_match, pattern):
        return pattern.parse_func(re_match, pattern)
