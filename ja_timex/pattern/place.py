import json
import re
from dataclasses import dataclass
from pathlib import Path

weekday2id = {"月": "1", "火": "2", "水": "3", "木": "4", "金": "5", "土": "6", "日": "7"}
season2id = {"春": "SP", "夏": "SU", "秋": "FA", "冬": "WI"}
with Path(__file__).parent.parent.joinpath("dictionary/wareki.json").open(encoding="utf8") as f:
    wareki2year = json.load(f)


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
    # abstime: 日付表現
    calendar_year: str = "(?P<calendar_year>[0-9]{1,4})"  # 暦の年
    calendar_year_wareki: str = "(?P<calendar_year_wareki>([1-9][0-9]{0,1}|0[1-9]|元))"  # 和暦の年 (0年は除外)
    calendar_month: str = "(?P<calendar_month>1[0-2]|0?[1-9])"  # 暦の月
    calendar_day: str = "(?P<calendar_day>[12][0-9]|3[01]|0?[1-9])"  # 暦の日
    weekday: str = "(?P<weekday>[月火水木金土日])"
    season: str = "(?P<season>(春|夏|秋|冬))"
    quarter: str = "(?P<quarter>[1-4])"
    fiscal_year: str = "(?P<fiscal_year>[0-9]{4})"
    ac_century: str = "(?P<ac_century>[1-9]?[0-9]{1,2})"
    bc_year: str = "(?P<bc_year>[0-9]{1,4})"
    bc_century: str = "(?P<bc_century>[1-9]?[0-9]{1,2})"

    # abstime: 時刻表現
    am_prefix: str = "(?P<am_prefix>(午前|am|AM|))"
    am_suffix: str = "(?P<am_suffix>(am|AM))"
    pm_prefix: str = "(?P<pm_prefix>(午後|pm|PM))"
    pm_suffix: str = "(?P<pm_suffix>(pm|PM))"
    ampm_prefix: str = f"({am_prefix}|{pm_prefix})"
    ampm_suffix: str = f"(\\s?({am_suffix}|{pm_suffix}))"
    clock_hour: str = "(?P<clock_hour>[0-2]?[0-9])"
    clock_minute: str = "(?P<clock_minute>[0-5]?[0-9])"
    clock_second: str = "(?P<clock_second>[0-5]?[0-9])"
    morning_prefix: str = "(?P<morning_prefix>([今|早]?朝))"
    evening_prefix: str = "(?P<evening_prefix>(今?[夜晩]))"
    midnight_prefix: str = "(?P<midnight_prefix>(深夜))"
    times_of_day_prefix = f"({morning_prefix}|{evening_prefix}|{midnight_prefix})"

    # 曜日付きの表記
    weekday_without_symbol: str = f"{weekday}(曜日|曜)"
    # (日曜日)などの記号付きの表記
    weekday_with_symbol: str = "\\s{,1}[\\(（]\\s{,1}" + f"{weekday}(曜日|曜)?" + "\\s{,1}[\\)）]"

    # duraton: 期間表現
    year: str = "(?P<year>[0-9]+\\.?[0-9]*)"
    month: str = "(?P<month>[0-9]+\\.?[0-9]*)"  # 日付における月とは異なり、18ヶ月など任意の数字を取れる
    day: str = "(?P<day>[0-9]+\\.?[0-9]*)"
    century: str = "(?P<century>[1-9]?[0-9]{1,2})"
    week: str = "(?P<week>[0-9]+\\.?[0-9]*)"
    hour: str = "(?P<hour>[0-9]+\\.?[0-9]*)"
    minute: str = "(?P<minute>[0-9]+\\.?[0-9]*)"
    second: str = "(?P<second>[0-9]+\\.?[0-9]*)"
    second_with_ms: str = "(?P<second_with_ms>[0-9]+[秒][0-9]+)"

    # duration: 持続時間
    count: str = "(?P<count>[0-9]+\\.?[0-9]*)"
    year_range: str = "(?P<year_range>[0-9]+\\.?[0-9]*)"  # 期間としての月
    month_range: str = "(?P<month_range>[0-9]+\\.?[0-9]*)"
    day_range: str = "(?P<day_range>[0-9]+\\.?[0-9]*)"
    range: str = "(?P<range>[0-9]+\\.?[0-9]*)"  # 頻度における数値としての表現

    # prefix and suffix for mod
    before_suffix: str = "(?P<before_suffix>(前|まえ))"
    after_suffix: str = "(?P<after_suffix>(後|あと))"
    start_suffix: str = "(?P<start_suffix>((はじ|初|始)め|初[頭期旬]|前[半期]|頭))"
    mid_suffix: str = "(?P<mid_suffix>((なか|半)ば|中(ごろ|頃|盤|旬|期)))"
    end_suffix: str = "(?P<end_suffix>(後[半期]|終盤|[終お]わり|末日?))"
    abstime_approx_suffix: str = "(?P<abstime_approx_suffix>(近く|前後|くらい|頃|ごろ))"
    on_or_before_suffix: str = "(?P<on_or_before_suffix>(以前))"
    on_or_after_suffix: str = "(?P<on_or_after_suffix>(以[来降後]))"

    approx_suffix: str = "(?P<approx_suffix>(近く|前後|くらい|ばかり))"

    # reltime: 相対的な時間におけるsuffix
    around_suffix: str = "([くぐ]らい|ほど|程度|ばかり|近く|より(も)?)"
    just_suffix: str = "(?P<just_suffix>(目|もの間|ぶり))"

    # 和暦の元号
    wareki_prefix: str = f"(?P<wareki_prefix>({'|'.join(wareki2year.keys())}))"

    # 半分の表現
    half_suffix: str = "(?P<half_suffix>半)"

    def is_valid(self, target, text):
        # for tests
        re_pattern = getattr(self, target)
        if re.fullmatch(re_pattern, text):
            return True
        else:
            return False


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


def get_wareki_first_year(text: str) -> int:
    """和暦の元号のゼロ年に対応する西暦を取得

    和暦から西暦に変換するために、和暦における元年に-1をした西暦を計算する

    Args:
        text (str): 和暦の元号

    Returns:
        int: 対応する元号のゼロ年の西暦
    """

    return wareki2year[text] - 1
