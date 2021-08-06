import re
from collections import defaultdict
from typing import DefaultDict, Dict, List, Optional

import pendulum

from ja_timex.number_normalizer import NumberNormalizer
from ja_timex.tag import TIMEX
from ja_timex.tagger import AbstimeTagger, DurationTagger, ReltimeTagger, SetTagger
from ja_timex.util import is_parial_pattern_of_number_expression


class TimexParser:
    def __init__(
        self,
        number_normalizer=NumberNormalizer(),
        abstime_tagger=AbstimeTagger(),
        duration_tagger=DurationTagger(),
        reltime_tagger=ReltimeTagger(),
        set_tagger=SetTagger(),
        custom_tagger=None,
        reference: Optional[pendulum.DateTime] = None,
    ) -> None:
        self.number_normalizer = number_normalizer
        self.abstime_tagger = abstime_tagger
        self.duration_tagger = duration_tagger
        self.reltime_tagger = reltime_tagger
        self.set_tagger = set_tagger
        self.custom_tagger = custom_tagger
        self.reference = reference

        self.all_patterns = {}
        self.all_patterns["abstime"] = self.abstime_tagger.patterns
        self.all_patterns["duration"] = self.duration_tagger.patterns
        self.all_patterns["reltime"] = self.reltime_tagger.patterns
        self.all_patterns["set"] = self.set_tagger.patterns
        if self.custom_tagger:
            self.all_patterns["custom"] = self.custom_tagger.patterns

    def parse(self, raw_text: str) -> List[TIMEX]:
        # 数の認識/規格化
        processed_text = self._normalize_number(raw_text)

        # 時間表現の抽出
        all_extracts = self._extract(processed_text)
        type2extracts = self._drop_duplicates(processed_text, all_extracts)
        # 規格化
        timex_tags = self._parse(type2extracts)

        # 規格化後のタグの情報付与
        timex_tags = self._modify_additional_information(timex_tags, processed_text)

        return timex_tags

    def _normalize_number(self, raw_text: str) -> str:
        return self.number_normalizer.normalize(raw_text)

    def _extract(self, processed_text: str) -> List[Dict]:
        all_extracts = []

        # すべてのtaggerのパターンの正規表現を順に適用していく
        for type_name, patterns in self.all_patterns.items():
            for pattern in patterns:
                # 文字列中からのパターン検知
                re_iter = re.finditer(pattern.re_pattern, processed_text)
                for re_match in re_iter:
                    if is_parial_pattern_of_number_expression(re_match, processed_text):
                        continue
                    all_extracts.append({"type_name": type_name, "re_match": re_match, "pattern": pattern})
        return all_extracts

    def _drop_duplicates(self, processed_text: str, all_extracts: List[Dict]) -> DefaultDict[str, List[Dict]]:
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

    def _parse(self, type2extracts: DefaultDict[str, List[Dict]]) -> List[TIMEX]:
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
                elif type_name == "custom":
                    results.append(self.custom_tagger.parse_with_pattern(extract["re_match"], extract["pattern"]))

        return results

    def _modify_additional_information(self, timex_tags: List[TIMEX], processed_text: str) -> List[TIMEX]:
        # update @tid and reference
        modified_tags = []
        sorted_timex_tags = sorted(timex_tags, key=lambda x: x.span[0] if x.span else 0)
        for i, timex in enumerate(sorted_timex_tags):
            timex.tid = f"t{i}"
            if self.reference:
                timex.reference = self.reference
            modified_tags.append(timex)

        return modified_tags
