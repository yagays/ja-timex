from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple

import pendulum

from ja_timex.pattern.place import Pattern


@dataclass
class TIMEX:
    type: str
    value: str
    text: str

    tid: Optional[str] = None
    freq: Optional[str] = None
    quant: Optional[str] = None
    mod: Optional[str] = None

    parsed: Dict[str, str] = field(default_factory=dict)
    span: Optional[Tuple[int, int]] = None  # 入力文字列中での正規表現が取得したspan
    pattern: Optional[Pattern] = None
    reference: Optional[pendulum.datetime] = None

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

    def fill_target_value(self, target: str, fill_str: str, default_value: int):
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

    def to_datetime(self) -> Optional[datetime]:
        if not self.is_valid_datetime:
            return None

        if self.type == "DATE":
            if self.parsed.get("calendar_year") and self.parsed["calendar_year"] != "XXXX":
                year = int(self.parsed["calendar_year"])
            else:
                year = pendulum.now().year
            if self.parsed.get("calendar_month") and self.parsed["calendar_month"] != "XX":
                month = int(self.parsed["calendar_month"])
            else:
                month = 1
            if self.parsed.get("calendar_day") and self.parsed["calendar_day"] != "XX":
                day = int(self.parsed["calendar_day"])
            else:
                day = 1

            return pendulum.datetime(year=year, month=month, day=day, tz="Asia/Tokyo")
        elif self.type == "TIME" and self.reference:
            day_add = 0
            if self.parsed.get("clock_hour") and self.parsed["clock_hour"] != "XX":
                hour = int(self.parsed.get("clock_hour", 0))
                if hour >= 24:
                    hour = hour - 24
                    day_add = 1
            else:
                hour = 0
            if self.parsed.get("clock_minute") and self.parsed["clock_minute"] != "XX":
                minute = int(self.parsed.get("clock_minute", 0))
            else:
                minute = 0
            if self.parsed.get("clock_second") and self.parsed["clock_second"] != "XX":
                second = int(self.parsed.get("clock_second", 0))
            else:
                second = 0
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

            duration_years = self.fill_target_value(target="year", fill_str="XXXX", default_value=0)
            duration_months = self.fill_target_value(target="month", fill_str="XX", default_value=0)
            duration_days = self.fill_target_value(target="day", fill_str="XX", default_value=0)
            duration_hours = self.fill_target_value(target="hour", fill_str="XX", default_value=0)
            duration_minute = self.fill_target_value(target="minute", fill_str="XX", default_value=0)
            duration_seconds = self.fill_target_value(target="second", fill_str="XX", default_value=0)

            duration = pendulum.duration(
                years=duration_years,
                months=duration_months,
                days=duration_days,
                hours=duration_hours,
                minutes=duration_minute,
                seconds=duration_seconds,
            )
            return self.reference + sign * duration
        else:
            return None

    @property
    def is_valid_duration(self) -> bool:
        if self.type in ("DURATION") and self.parsed != {}:
            return True

        else:
            return False

    def to_duration(self) -> Optional[timedelta]:
        if not self.is_valid_duration:
            return None

        # pendulum: Float year and months are not supported
        return pendulum.duration(
            years=int(self.parsed.get("year", 0)),
            months=int(self.parsed.get("month", 0)),
            weeks=float(self.parsed.get("week", 0)),
            days=float(self.parsed.get("day", 0)),
            hours=float(self.parsed.get("hour", 0)),
            minutes=float(self.parsed.get("minute", 0)),
            seconds=float(self.parsed.get("second", 0)),
            microseconds=float(self.parsed.get("micorsecond", 0)),
        )

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
        attributes.append(f'text="{self.text}"')

        attributes_text = " ".join(attributes)
        return f"<TIMEX3 {attributes_text}>"


@dataclass
class AnnotatedTIMEX(TIMEX):
    """アノテーションされたTIMEXタグの情報を表現する際に用いるTIMEX拡張"""

    valueFromSurface: Optional[str] = None
    temporalFunction: Optional[str] = None
    rangeStart: Optional[str] = None
    rangeEnd: Optional[str] = None
