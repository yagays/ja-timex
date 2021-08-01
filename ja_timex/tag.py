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

    @property
    def is_valid_datetime(self) -> bool:
        if self.parsed.get("calendar_year") or self.parsed.get("calendar_month") or self.parsed.get("calendar_day"):
            # DATE
            return True
        elif self.parsed.get("clock_hour") or self.parsed.get("clock_minutes") or self.parsed.get("clock_second"):
            # TIME
            # 日付が無いとdatetimeを構築できないため、今はFalseにしている
            # (pendulumでは自動で実行日の日付が付与されるが、さすがに時間表現としては不適切か)
            return False
        else:
            return False

    def to_datetime(self) -> Optional[datetime]:
        if not self.is_valid_datetime:
            return None

        # TODO: 補完するときのdefaultの設定をできるようにする
        # TODO: timezoneを設定できるようにする
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
            minutes=float(self.parsed.get("minutes", 0)),
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
