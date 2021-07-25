from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional, Tuple


class TIME_TYPE(Enum):
    DATE = 1
    TIME = 2
    DURATION = 3
    SET = 4


@dataclass
class TIMEX:
    type: str
    value: str
    value_from_surface: str
    text: str

    temporal_function: Optional[bool] = None
    # 頻度集合表現
    freq: Optional[str] = None
    quant: Optional[str] = None
    mod: Optional[str] = None
    range_start: Optional[str] = None
    range_end: Optional[str] = None
    ordinal: Optional[str] = None

    parsed: Optional[Dict] = None
    value_format: Optional[str] = None
    additional_info: Optional[str] = None
    span: Optional[Tuple[int, int]] = None  # 入力文字列中での正規表現が取得したspan

    def to_tag(self) -> str:
        attributes = [f'type="{self.type}"', f'value="{self.value}"', f'valueFromSurface="{self.value_from_surface}"']
        attributes_text = " ".join(attributes)
        tag = f"<TIMEX3 {attributes_text}>{self.text}</TIMEX3>"
        return tag
