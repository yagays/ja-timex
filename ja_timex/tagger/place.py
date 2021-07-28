import re
from dataclasses import dataclass


class Pattern:
    def __init__(self, re_pattern, parse_func, option=None) -> None:
        self.re_pattern = re_pattern
        self.parse_func = parse_func
        self.option = option

    def __repr__(self) -> str:
        return f"<Pattern: {self.re_pattern} / parse_func:{self.parse_func.__name__} / option:{self.option}>"


# 正規表現に用いる部分パターン
@dataclass
class Place:
    # abstime: 時間表現
    calendar_year: str = "(?P<calendar_year>[0-9]{,4})"  # 暦の年
    calendar_month: str = "(?P<calendar_month>1[0-2]|0?[1-9])"  # 暦の月
    calendar_day: str = "(?P<calendar_day>[12][0-9]|3[01]|0?[1-9])"  # 暦の日
    weekday: str = "(?P<weekday>[月火水木金土日])"
    season: str = "(?P<season>(春|夏|秋|冬))"
    quarter: str = "(?P<quarter>[1-4])"
    fiscal_year: str = "(?P<fiscal_year>[0-9]{4})年度"
    ac_century: str = "(?P<ac_century>[1-9]?[0-9]{,2})世紀"
    bc_year: str = "紀元前(?P<bc_year>[0-9]{,4})年"
    bc_century: str = "紀元前(?P<bc_century>[1-9]?[0-9]{,2})世紀"

    @property
    def weekday_with_suffix(self):
        # (日曜日)などの記号付きの表記
        return self.weekday + "(曜日|曜)?"

    @property
    def weekday_with_symbol(self):
        # (日曜日)などの記号付きの表記
        return "\\s{,1}\\(?\\s{,1}" + self.weekday_with_suffix + "\\s{,1}\\)?"

    # duraton: 期間表現
    year: str = "(?P<year>[0-9]{,4})"
    month: str = "(?P<month>[0-9]+)"  # 日付における月とは異なり、18ヶ月など任意の数字を取れる
    day: str = "(?P<day>[0-9]+\\.?[0-9]*)"
    century: str = "(?P<century>[1-9]?[0-9]{,2})"
    week: str = "(?P<week>[0-9]+\\.?[0-9]*)"
    hour: str = "(?P<hour>[0-9]+\\.?[0-9]*)"
    minutes: str = "(?P<minutes>[0-9]+\\.?[0-9]*)"
    second: str = "(?P<second>[0-9]+\\.?[0-9]*)"
    second_with_ms: str = "(?P<second_with_ms>[0-9]+[秒][0-9]+)"

    # reltime: 相対的な時間における曖昧表現
    around_prefix = "(以上|[くぐ]らい|ほど|程度|ばかり|近く|より(も)?)"

    # duration: 持続時間
    count: str = "(?P<count>[0-9]+\\.?[0-9]*)"
    year_range: str = "(?P<year_range>[0-9]+\\.?[0-9]*)"  # 期間としての月
    month_range: str = "(?P<month_range>[0-9]+\\.?[0-9]*)"
    day_range: str = "(?P<day_range>[0-9]+\\.?[0-9]*)"
    range: str = "(?P<range>[0-9]+\\.?[0-9]*)"  # 頻度における数値としての表現

    def is_valid(self, target, text):
        # for tests
        re_pattern = getattr(self, target)
        if re.fullmatch(re_pattern, text):
            return True
        else:
            return False


weekday2id = {"月": "1", "火": "2", "水": "3", "木": "4", "金": "5", "土": "6", "日": "7"}
season2id = {"春": "SP", "夏": "SU", "秋": "FA", "冬": "WI"}


def get_weekday_id(text: str) -> str:
    """曜日の文字表現からidを取得

    Args:
        text (str): 曜日の文字表現

    Returns:
        str: 曜日に対応するid文字列
    """
    return weekday2id[text]


def get_season_id(text: str) -> str:
    """季節の文字表かからidを取得

    Args:
        text (str): 季節の文字表現

    Returns:
        str: 季節に対応するid文字列
    """
    return season2id[text]
