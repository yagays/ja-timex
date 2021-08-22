from typing import Union

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
