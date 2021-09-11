from typing import List, Optional, Union

import pendulum
from pendulum.tz.timezone import Timezone


def set_timezone(tz: Union[str, Timezone]) -> Timezone:
    """デフォルトのtimezoneを設定する

    Args:
        tz (Union[str, Timezone]): タイムゾーンのstrまたはTimezone

    Raises:
        TypeError: tzの型がstrまたはTimezoneではなかった場合

    Returns:
        Timezone: 設定されたTimezone
    """
    if isinstance(tz, str):
        default_timezone = pendulum.timezone(tz)
    elif isinstance(tz, Timezone):
        default_timezone = tz
    else:
        raise TypeError("tz must be a `str` or `pendulum.timezone`")

    return default_timezone


def detect_range_expression_before_timex(
    span_start_i: int,
    text: str,
    range_expressions: List[str] = [
        "〜",
        "~",
        "-",
        "から",
        "から翌",
        "から同",
    ],
) -> Optional[str]:
    maxlen_range_expression = max([len(r) for r in range_expressions])
    for range_expression in range_expressions:
        if text[span_start_i - maxlen_range_expression : span_start_i].endswith(range_expression):
            return range_expression
    return None
