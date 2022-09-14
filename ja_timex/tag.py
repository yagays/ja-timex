import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple, Union

import pendulum
from pendulum.tz.timezone import Timezone

from ja_timex.pattern.place import Pattern
from ja_timex.util import set_timezone


@dataclass
class TIMEX:
    type: str
    value: str
    text: str
    span: Tuple[int, int]

    # 正規化前の抽出テキストと開始終了位置
    raw_text: Optional[str] = None
    raw_span: Optional[Tuple[int, int]] = None

    parsed: Dict[str, str] = field(default_factory=dict)

    tid: Optional[str] = None
    freq: Optional[str] = None
    quant: Optional[str] = None
    mod: Optional[str] = None
    range_start: Optional[bool] = None
    range_end: Optional[bool] = None

    pattern: Optional[Pattern] = None
    reference: Optional[pendulum.DateTime] = None

    def to_tag(self) -> str:
        """TIMEX3のタグ文字列を生成する

        Returns:
            str: タグで囲まれた文字列
        """
        attributes = []
        if self.tid:
            attributes.append(f'tid="{self.tid}"')
        attributes += [f'type="{self.type}"', f'value="{self.value}"']
        if self.freq:
            attributes.append(f'freq="{self.freq}"')
        if self.quant:
            attributes.append(f'quant="{self.quant}"')
        if self.mod:
            attributes.append(f'mod="{self.mod}"')
        attributes_text = " ".join(attributes)
        tag = f"<TIMEX3 {attributes_text}>{self.text}</TIMEX3>"
        return tag

    def fill_target_value(self, target: str, fill_str: str, default_value: int) -> int:
        """正規表現で取得した情報の中からtargetの値を取得する

        Args:
            target (str): self.parsedのkey文字列
            fill_str (str): 特定できない場合に入る文字列
            default_value (int): 値を取得できなかった場合に返却する値

        Returns:
            int: 取得した値
        """
        if self.parsed.get(target) and self.parsed[target] != fill_str:
            value = int(self.parsed[target])
        else:
            value = default_value
        return value

    @property
    def is_valid_datetime(self) -> bool:
        if self.type == "DATE":
            return True
        elif self.type == "TIME":
            return True
        elif self.type == "DURATION":
            return True
        else:
            return False

    def to_datetime(self, tz: Union[str, Timezone] = "Asia/Tokyo") -> Optional[datetime]:
        if not self.is_valid_datetime:
            return None

        default_timezone = set_timezone(tz)

        if self.type == "DATE":
            # 世紀や曜日はdatetimeでの表現が不可能なため変換しない
            for exclude_pattern in ["ac_century", "bc_century", "weekday"]:
                if exclude_pattern in self.parsed:
                    return None

            year = self.fill_target_value(target="calendar_year", fill_str="XXXX", default_value=pendulum.now().year)
            month = self.fill_target_value(target="calendar_month", fill_str="XX", default_value=1)
            day = self.fill_target_value(target="calendar_day", fill_str="XX", default_value=1)

            if self.reference:
                # 詳細な挙動は test_reference_datetime_default_year を参照
                if self.parsed.get("calendar_year") == "XXXX":
                    year = self.reference.year
                    if self.parsed.get("calendar_month") == "XX":
                        month = self.reference.month

            return pendulum.datetime(year=year, month=month, day=day, tz=default_timezone)
        elif self.type == "TIME" and self.reference:
            hour = self.fill_target_value(target="clock_hour", fill_str="XX", default_value=0)
            minute = self.fill_target_value(target="clock_minute", fill_str="XX", default_value=0)
            second = self.fill_target_value(target="clock_second", fill_str="XX", default_value=0)

            # 24時を超える表現
            if hour >= 24:
                hour = hour - 24
                day_add = 1
            else:
                day_add = 0

            # "半"という表記がある場合
            if self.parsed.get("half_suffix"):
                minute = 30

            return pendulum.datetime(
                year=self.reference.year,
                month=self.reference.month,
                day=self.reference.day + day_add,
                hour=hour,
                minute=minute,
                second=second,
                tz=self.reference.tz,
            )
        elif self.type == "DURATION" and self.reference:
            sign = 1
            if self.mod == "BEFORE":
                sign = -1

            duration = self.to_duration()
            return self.reference + sign * duration

        else:
            return None

    @property
    def is_valid_duration(self) -> bool:
        if self.type in ("DURATION") and self.parsed != {}:
            return True

        else:
            return False

    def to_duration(self) -> timedelta:

        unit_args = {
            "years": float(self.parsed.get("year", 0)),
            "months": float(self.parsed.get("month", 0)),
            "weeks": float(self.parsed.get("week", 0)),
            "days": float(self.parsed.get("day", 0)),
            "hours": float(self.parsed.get("hour", 0)),
            "minutes": float(self.parsed.get("minute", 0)),
            "seconds": float(self.parsed.get("second", 0)),
            "microseconds": float(self.parsed.get("micorsecond", 0)),
        }

        # pendulumはyearsとmonthsはintでなければならないため、
        # 小数点表記を分解して解釈する必要がある
        month_i, month_d = divmod(unit_args["months"], 1)
        unit_args["months"] = int(month_i)
        if month_d != 0.0:
            # 小数点分を日に追加
            unit_args["days"] += 30 * month_d

        year_i, year_d = divmod(unit_args["years"], 1)
        unit_args["years"] = int(year_i)
        if year_d != 0.0:
            # 小数点分を月に追加
            unit_args["months"] += int(12 * year_d)

        # "半"という表記がある場合
        if self.parsed.get("half_suffix"):
            for unit in ["week", "day", "hour", "minute", "sescond"]:
                if self.parsed.get(unit):
                    unit_args[unit + "s"] += 0.5
            if self.parsed.get("year"):
                unit_args["months"] += 6
            if self.parsed.get("month"):
                # 半月という期間は月によって異なるが、pendulumの1ヶ月は30日として計算されるため、ここでは一律で15日の期間とする
                unit_args["days"] += 15

        return pendulum.duration(**unit_args)

    def __repr__(self) -> str:
        attributes = []
        if self.tid:
            attributes.append(f'tid="{self.tid}"')
        attributes += [
            f'type="{self.type}"',
            f'value="{self.value}"',
        ]
        if self.freq:
            attributes.append(f'freq="{self.freq}"')
        if self.quant:
            attributes.append(f'quant="{self.quant}"')
        if self.mod:
            attributes.append(f'mod="{self.mod}"')
        if self.range_start:
            attributes.append('range_start="True"')
        if self.range_end:
            attributes.append('range_end="True"')
        attributes.append(f'text="{self.text}"')

        attributes_text = " ".join(attributes)
        return f"<TIMEX3 {attributes_text}>"


@dataclass
class AnnotatedTIMEX(TIMEX):
    """アノテーションされたTIMEXタグの情報を表現する際に用いるTIMEX拡張"""

    valueFromSurface: Optional[str] = None
    temporalFunction: Optional[str] = None


@dataclass
class Extract:
    type_name: str
    re_match: re.Match
    pattern: Pattern
