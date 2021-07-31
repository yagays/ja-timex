from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple, Union

from dateutil.relativedelta import relativedelta

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
            return True
        else:
            return False

    def to_datetime(self) -> Optional[datetime]:
        if self.is_valid_datetime:
            return datetime(
                int(self.parsed["calendar_year"]), int(self.parsed["calendar_month"]), int(self.parsed["calendar_day"])
            )
        else:
            return None

    @property
    def is_valid_timedelta(self) -> bool:
        if self.type == "DURATION" and self.parsed != {}:
            return True
        else:
            return False

    def to_delta(self) -> Union[timedelta, relativedelta, None]:
        if not self.is_valid_timedelta:
            return None

        if self.value[:2] == "PT":
            args = {}
            for arg_name in ["hour", "minutes", "second"]:
                args[arg_name] = 0.0
                if self.parsed.get(arg_name):
                    args[arg_name] = float(self.parsed[arg_name])
            # timedeltaはint/float
            return timedelta(hours=args["hour"], minutes=args["minutes"], seconds=args["second"])
        else:
            relative_args = {}
            for arg_name in ["year", "month", "week", "day"]:
                relative_args[arg_name] = 0
                if self.parsed.get(arg_name):
                    relative_args[arg_name] = int(self.parsed[arg_name])
            # relaivedeltaはint
            return relativedelta(
                years=relative_args["year"],
                months=relative_args["month"],
                weeks=relative_args["week"],
                days=relative_args["day"],
            )  # noqa

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
