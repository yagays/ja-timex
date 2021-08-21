import re
from typing import Tuple, Union

import pendulum
from pendulum.tz.timezone import Timezone


def is_parial_pattern_of_number_expression(span: Tuple[int, int], processed_text: str) -> bool:
    """対象パターンが数字表現の一部かを判定する

    正規表現の記法によっては、数字表現の一部を取得してしまう例がある。
    与えられたパターンが数字表現の一部を間違って取得していないかをチェックする

    e.g. "これは13/13です" に対して "3/13" というパターンを取得している場合 -> True
    e.g. "これは3/13です" に対して "3/13" というパターンを取得している場合 -> False

    Args:
        re_match (re.Match): 対象となる正規表現のパターン
        processed_text (str): 入力文字列

    Returns:
        bool: 数字表現の一部かを表す真偽値
    """
    start_i = span[0]
    end_i = span[1]

    target_text = processed_text[start_i:end_i]
    # 対象としている文字列が、数字と記号の表現ではなかった場合
    if not re.fullmatch(r"[0-9\.\-\.,/・]+", target_text):
        return False

    if start_i != 0 and re.match(r"[0-9\+]", processed_text[start_i - 1]):
        return True
    elif end_i != len(processed_text) and re.match(r"[0-9\+]", processed_text[end_i]):
        return True
    else:
        return False


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
