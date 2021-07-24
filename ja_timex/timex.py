import re
from collections import defaultdict
from typing import Dict, List, Optional

from ja_timex.modifier import Modifier
from ja_timex.number_normalizer import NumberNormalizer
from ja_timex.tag import TIMEX
from ja_timex.tagger.abstime_tagger import AbstimeTagger
from ja_timex.tagger.duration_tagger import DurationTagger
from ja_timex.tagger.reltime_tagger import ReltimeTagger
from ja_timex.tagger.set_tagger import SetTagger


def is_parial_pattern_of_number_expression(re_match: re.Match, processed_text: str) -> bool:
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
    start_i, end_i = re_match.span()
    has_number_list = []

    if start_i != 0:
        has_number_list.append(re.match("[0-9]", processed_text[start_i - 1]))
    if len(processed_text) != end_i:
        has_number_list.append(re.match("[0-9]", processed_text[end_i]))

    return any(has_number_list)


class TimexParser:
    def __init__(
        self,
        number_normalizer=NumberNormalizer(),
        abstime_tagger=AbstimeTagger(),
        duration_tagger=DurationTagger(),
        reltime_tagger=ReltimeTagger(),
        set_tagger=SetTagger(),
        modifier=Modifier(),
    ) -> None:
        self.number_normalizer = number_normalizer
        self.abstime_tagger = abstime_tagger
        self.duration_tagger = duration_tagger
        self.reltime_tagger = reltime_tagger
        self.set_tagger = set_tagger
        self.modifier = modifier

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
        all_extracts = self._extract(processed_text)
        type2extracts = self._drop_duplicates(processed_text, all_extracts)
        # 規格化
        timex_tags = self._parse(type2extracts)

        # 修飾語によるタグの情報付与
        modified_timex_tags = self._modify_additional_information(timex_tags, processed_text)
        return modified_timex_tags

    def _normalize_number(self, raw_text: str) -> str:
        return self.number_normalizer.normalize(raw_text)

    def _extract(self, processed_text: str):
        all_extracts = []

        for type_name, patterns in self.all_patterns.items():
            for pattern in patterns:
                # 文字列中からのパターン検知
                re_iter = re.finditer(pattern["pattern"], processed_text)
                for re_match in re_iter:
                    if is_parial_pattern_of_number_expression(re_match, processed_text):
                        continue
                    all_extracts.append({"type_name": type_name, "re_match": re_match, "pattern": pattern})
        return all_extracts

    def _drop_duplicates(self, processed_text, all_extracts):
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

    def _modify_additional_information(self, timex_tags: List[TIMEX], processed_text: str) -> List[TIMEX]:
        # add tid

        # update mod
        modified_tags = []
        for timex in timex_tags:
            print(timex.type)
            parsed_mod = self.modifier.parse(processed_text, timex.span, timex.type)
            if parsed_mod:
                timex.mod = parsed_mod

            modified_tags.append(timex)

        return timex_tags


if __name__ == "__main__":
    timex = TimexParser()
    # timex.parse("2021年7月23日")
