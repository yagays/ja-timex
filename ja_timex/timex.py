from typing import List

from ja_timex.tag import TIMEX


class Timex:
    def __init__(self) -> None:
        self.number_normalizer = ""
        self.abstime_tagger = ""
        self.duration_tagger = ""
        self.reltime_tagger = ""

        # TODO: set default timezone by pendulum

    def tagging(self, raw_text: str):
        # 数の認識/規格化
        processed_text = self._normalize_number(raw_text)

        # 時間表現の抽出
        extracted_phrases = self._extract_phrases(processed_text)
        # 規格化
        normalized_tags = self._parse(extracted_phrases)

        # 修飾語によるタグの情報付与
        modified_tags = self._modify_additional_information(normalized_tags)
        return modified_tags

    def _normalize_number(self, raw_text: str) -> str:
        return raw_text

    def _extract_phrases(self, processed_text: str) -> List[str]:
        return ["2020年7月7日"]

    def _parse(self, extracted_phrases: List[str]) -> List[TIMEX]:
        return [TIMEX(type="DATE", value="2020年7月7日", value_from_surface="2020年7月7日")]

    def _modify_additional_information(self, normalized_tags: List[TIMEX]) -> List[TIMEX]:
        return [TIMEX(type="DATE", value="2020年7月7日", value_from_surface="2020年7月7日")]
