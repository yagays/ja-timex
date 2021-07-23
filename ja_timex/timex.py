import re
from collections import defaultdict
from typing import Dict, List

from ja_timex.number_normalizer import NumberNormalizer
from ja_timex.tag import TIMEX
from ja_timex.tagger.abstime_tagger import AbstimeTagger
from ja_timex.tagger.duration_tagger import DurationTagger
from ja_timex.tagger.reltime_tagger import ReltimeTagger
from ja_timex.tagger.set_tagger import SetTagger


class TimexParser:
    def __init__(
        self,
        number_normalizer=NumberNormalizer(),
        abstime_tagger=AbstimeTagger(),
        duration_tagger=DurationTagger(),
        reltime_tagger=ReltimeTagger(),
        set_tagger=SetTagger(),
    ) -> None:
        self.number_normalizer = number_normalizer
        self.abstime_tagger = abstime_tagger
        self.duration_tagger = duration_tagger
        self.reltime_tagger = reltime_tagger
        self.set_tagger = set_tagger

        self.all_patterns = {}
        self.all_patterns["abstime"] = self.abstime_tagger.patterns
        self.all_patterns["duration"] = self.duration_tagger.patterns
        self.all_patterns["reltime"] = self.reltime_tagger.patterns
        self.all_patterns["set"] = self.set_tagger.patterns

        # TODO: set default timezone by pendulum

    def parse(self, raw_text: str):
        # 数の認識/規格化
        processed_text = self._normalize_number(raw_text)

        # 時間表現の抽出
        type2extracts = self._extract(processed_text)
        # 規格化
        timex_tags = self._parse(type2extracts)

        # 修飾語によるタグの情報付与
        # modified_tags = self._modify_additional_information(normalized_tags)
        return timex_tags

    def _normalize_number(self, raw_text: str) -> str:
        return self.number_normalizer.normalize(raw_text)

    def _extract(self, processed_text: str):
        all_extracts = []

        for type_name, patterns in self.all_patterns.items():
            for pattern in patterns:
                # 文字列中からのパターン検知
                re_iter = re.finditer(pattern["pattern"], processed_text)
                for re_match in re_iter:
                    all_extracts.append({"type_name": type_name, "re_match": re_match, "pattern": pattern})

        type2extracts = defaultdict(list)
        text_coverage_flag = [False] * len(processed_text)

        long_order_extracts = sorted(all_extracts, key=lambda x: len(x["re_match"].group()), reverse=True)
        for target_extract in long_order_extracts:
            start_i, end_i = target_extract["re_match"].span()

            # すべてがまだ未使用のcharだった場合に候補に加える
            if any(text_coverage_flag[start_i:end_i]) is False:
                text_coverage_flag[start_i:end_i] = [True] * (end_i - start_i)
                type2extracts[target_extract["type_name"]].append(target_extract)

        return type2extracts

    def _parse(self, type2extracts) -> List[TIMEX]:
        results = []
        for type_name, extracts in type2extracts.items():
            for extract in extracts:
                if type_name == "abstime":
                    results.append(self.abstime_tagger.parse_with_pattern(extract["re_match"], extract["pattern"]))
                elif type_name == "duration":
                    results.append(self.duration_tagger.parse_with_pattern(extract["re_match"], extract["pattern"]))
                elif type_name == "reltime":
                    results.append(self.reltime_tagger.parse_with_pattern(extract["re_match"], extract["pattern"]))
                elif type_name == "set":
                    results.append(self.set_tagger.parse_with_pattern(extract["re_match"], extract["pattern"]))

        return results

    # def _modify_additional_information(self, normalized_tags: List[TIMEX]) -> List[TIMEX]:
    #     return [TIMEX(type="DATE", value="2020年7月7日", value_from_surface="2020年7月7日")]


if __name__ == "__main__":
    timex = TimexParser()
    # timex.parse("2021年7月23日")
