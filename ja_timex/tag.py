from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional, Tuple

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

    parsed: Optional[Dict] = None
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

    def to_datetime(self) -> Optional[datetime]:
        if self.parsed:
            return datetime(
                int(self.parsed["calendar_year"]), int(self.parsed["calendar_month"]), int(self.parsed["calendar_day"])
            )
        else:
            return None

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
