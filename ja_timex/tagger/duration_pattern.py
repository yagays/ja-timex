import re
from dataclasses import dataclass


# 時間表現の正規表現に用いる部分パターン
@dataclass
class DurationPlace:
    year: str = "(?P<year>[0-9]{,4})"
    month: str = "(?P<month>[0-9]+)"  # 日付における月とは異なり、18ヶ月など任意の数字を取れる
    day: str = "(?P<day>0?[1-9]|[12][0-9]|3[01])"
    century: str = "(?P<century>[1-9]?[0-9]{,2})"
    week: str = "(?P<week>[0-9]+\.?[0-9]*)"
    hour: str = "(?P<hour>[0-9]+\.?[0-9]*)"
    minutes: str = "(?P<minutes>[0-9]+\.?[0-9]*)"
    second: str = "(?P<second>[0-9]+\.?[0-9]*)"

    def is_valid(self, target, text):
        re_pattern = getattr(self, target)
        if re.fullmatch(re_pattern, text):
            return True
        else:
            return False


p = DurationPlace()

patterns = []
