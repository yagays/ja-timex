import json
from typing import Optional


class Modifier:
    def __init__(self, dict_path="ja_timex/dictionary/mod.json") -> None:
        self._build_index(dict_path)

    def _build_index(self, dict_path) -> None:
        with open(dict_path) as f:
            self.pattern2mod_by_type = json.load(f)

    def parse(self, text, span, type: str) -> Optional[str]:
        result = None
        timex_start_i = span[0]
        timex_end_i = span[1]

        # check prefix
        for pattern2mod in self.pattern2mod_by_type[type]["prefix"]:
            prefix = pattern2mod["pattern"]
            prefix_word_len = len(prefix)

            timex_prefix = text[timex_start_i - prefix_word_len : timex_start_i]
            if timex_prefix == prefix:
                result = pattern2mod["mod"]
                break

        # check suffix
        for pattern2mod in self.pattern2mod_by_type[type]["suffix"]:
            suffix = pattern2mod["pattern"]
            suffix_word_len = len(suffix)

            timex_suffix = text[timex_end_i + 1 : timex_end_i + 1 + suffix_word_len]
            if timex_suffix == suffix:
                result = pattern2mod["mod"]
                break

        # TODO: prefixとsuffixどちらもあったときにどうするか？
        return result
