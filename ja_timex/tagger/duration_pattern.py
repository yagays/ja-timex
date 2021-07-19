import re
from dataclasses import dataclass

from ja_timex.tagger.base_pattern import BasePlace

# 期間表現の正規表現に用いる部分パターン
@dataclass
class DurationPlace(BasePlace):
    year: str = "(?P<year>[0-9]{,4})"
    month: str = "(?P<month>[0-9]+)"  # 日付における月とは異なり、18ヶ月など任意の数字を取れる
    day: str = "(?P<day>[0-9]+\.?[0-9]*)"
    century: str = "(?P<century>[1-9]?[0-9]{,2})"
    week: str = "(?P<week>[0-9]+\.?[0-9]*)"
    hour: str = "(?P<hour>[0-9]+\.?[0-9]*)"
    minutes: str = "(?P<minutes>[0-9]+\.?[0-9]*)"
    second: str = "(?P<second>[0-9]+\.?[0-9]*)"
    second_with_ms: str = "(?P<second_with_ms>[0-9]+[秒][0-9]+)"


p = DurationPlace()

patterns = []


# 年
patterns.append({"pattern": f"{p.year}年(間)?", "value": ""})

# 月
patterns.append({"pattern": f"{p.month}[ヶ|か|ケ|箇]?月(間)?", "value": ""})

# 日
patterns.append({"pattern": f"{p.day}日(間)?", "value": ""})

# 世紀
patterns.append({"pattern": f"{p.century}世紀", "value": ""})

# 週
patterns.append({"pattern": f"{p.week}週(間)?", "value": ""})

# 時間
patterns.append({"pattern": f"{p.hour}時間", "value": ""})

# 分
patterns.append({"pattern": f"{p.minutes}分(間)?", "value": ""})

# 秒
patterns.append({"pattern": f"{p.second}秒(間)?", "value": ""})
patterns.append({"pattern": f"{p.second_with_ms}", "value": ""})

# 組み合わせ
# patterns.append({"pattern": f"{p.year}年{p.month}[ヶ|か|ケ|箇]月", "value": ""})
# patterns.append({"pattern": f"{p.year}年{p.month}[ヶ|か|ケ|箇]月{p.day}日", "value": ""})
# patterns.append({"pattern": f"{p.hour}時間{p.minutes}分", "value": ""})
# patterns.append({"pattern": f"{p.hour}時間{p.minutes}分{p.second}秒", "value": ""})
# patterns.append({"pattern": f"{p.minutes}分{p.second}秒", "value": ""})
