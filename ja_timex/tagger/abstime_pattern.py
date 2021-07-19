import re
from dataclasses import dataclass

from ja_timex.tagger.base_pattern import BasePlace


# 時間表現の正規表現に用いる部分パターン
@dataclass
class Place(BasePlace):
    year: str = "(?P<year>[0-9]{,4})"
    month: str = "(?P<month>0?[1-9]|1[0-2])"  # 日付における月
    day: str = "(?P<day>0?[1-9]|[12][0-9]|3[01])"
    weekday: str = "(?P<weekday>[月火水木金土日])"
    season: str = "(?P<season>(春|夏|秋|冬))"
    quarter: str = "(?P<quarter>[1-4])"

    @property
    def weekday_with_suffix(self):
        # (日曜日)などの記号付きの表記
        return self.weekday + "(曜日|曜)?"

    @property
    def weekday_with_symbol(self):
        # (日曜日)などの記号付きの表記
        return "\s{,1}\(?\s{,1}" + self.weekday_with_suffix + "\s{,1}\)?"


p = Place()

# corresponding_time_position不要かも
patterns = [
    # {"pattern": f"{p.year}年{p.month}月{p.day}日", "corresponding_time_position": ["year", "momth", "day"], "value": "",},
    # {"pattern": f"(?P<weekday>水曜日)", "corresponding_time_position": [], "value": "3",},
    # {"pattern": "(?P<season>冬)", "corresponding_time_position": [], "value": "WI",},
    # {"pattern": "(?P<quarter>Q1)", "corresponding_time_position": [], "value": "Q1",},
    {
        "pattern": "(?P<fiscal_year>[0-9]{,4})年度",
        "corresponding_time_position": [],
        "value": "",
    },
    {
        "pattern": "(?P<century>[0-9]{,4})世紀",
        "corresponding_time_position": [],
        "value": "",
    },
    {
        "pattern": "紀元前(?P<bc_year>[0-9]{,4})年",
        "corresponding_time_position": [],
        "value": "",
    },
    {
        "pattern": "紀元前(?P<bc_century>[0-9]{,4})世紀",
        "corresponding_time_position": [],
        "value": "",
    },
]


# 日付
date_templates = [
    f"{p.year}年{p.month}月{p.day}日",
    f"{p.year}年{p.month}月",
    f"{p.month}月{p.day}日",
    f"{p.year}年",
    f"{p.month}月",
    f"{p.day}日",
]
for delimiter in ["/", "\-", "\.", "・", ","]:
    date_templates.append(f"{p.year}年?{delimiter}{p.month}月?{delimiter}{p.day}日?")
    date_templates.append(f"{p.year}年?{delimiter}{p.month}月?")
    date_templates.append(f"{p.month}月?{delimiter}{p.day}日?")

# 日付がある表記には曜日が記載される場合がある
date_templates += [
    f"{p.year}年{p.month}月{p.day}日{p.weekday_with_symbol}",
    f"{p.month}月{p.day}日{p.weekday_with_symbol}",
    f"{p.day}日{p.weekday_with_symbol}",
]
for delimiter in ["/", "\-", "\.", "・", ","]:
    date_templates.append(f"{p.year}年?{delimiter}{p.month}月?{delimiter}{p.day}日?{p.weekday_with_symbol}")
    date_templates.append(f"{p.month}月?{delimiter}{p.day}日?{p.weekday_with_symbol}")


for date_template in date_templates:
    add_pattern = {
        "pattern": date_template,
        "value": "",
    }
    patterns.append(add_pattern)


# 曜日
weekday2id = {"月": "1", "火": "2", "水": "3", "木": "4", "金": "5", "土": "6", "日": "7"}
patterns.append({"pattern": p.weekday_with_symbol, "value": ""})

# 季節
season2id = {"春": "SP", "夏": "SU", "秋": "FA", "冬": "WI"}
patterns.append({"pattern": f"({p.year}[年|/]?)?{p.season}", "value": ""})

# 四半期
patterns.append({"pattern": f"(第{p.quarter}四半期)", "value": ""})
patterns.append({"pattern": f"(Q{p.quarter})", "value": ""})
patterns.append({"pattern": f"({p.quarter}Q)", "value": ""})
