import json
from typing import Optional

from ja_timex.tag import TIMEX


class Modifier:
    def __init__(self, dict_path="ja_timex/dictionary/mod.json") -> None:
        self._build_index(dict_path)

    def _build_index(self, dict_path) -> None:
        with open(dict_path) as f:
            self.pattern2mod_by_type = json.load(f)

    def parse(self, text, timex: TIMEX) -> Optional[str]:
        timex = self._moidfy_mod(text, timex)

        return timex

    def _moidfy_mod(self, text, timex: TIMEX) -> Optional[str]:
        mod_add = None
        span = timex.span
        timex_type = timex.type
        timex_start_i = span[0]
        timex_end_i = span[1]

        # check prefix
        for pattern2mod in self.pattern2mod_by_type[timex_type]["prefix"]:
            prefix = pattern2mod["pattern"]
            prefix_word_len = len(prefix)

            timex_prefix = text[timex_start_i - prefix_word_len : timex_start_i]
            if timex_prefix == prefix:
                mod_add = pattern2mod["mod"]
                break

        # check suffix
        for pattern2mod in self.pattern2mod_by_type[timex_type]["suffix"]:
            suffix = pattern2mod["pattern"]
            suffix_word_len = len(suffix)

            timex_suffix = text[timex_end_i + 1 : timex_end_i + 1 + suffix_word_len]
            if timex_suffix == suffix:
                mod_add = pattern2mod["mod"]
                break

        # TODO: prefixとsuffixどちらもあったときにどうするか？
        timex.mod = mod_add
        return timex
