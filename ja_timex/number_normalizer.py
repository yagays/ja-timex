import re

import mojimoji


class NumberNormalizer:
    def __init__(self) -> None:
        pass

    def normalize(self, text: str) -> str:
        text = self._normalize_zen_to_han(text)

        return text

    def _normalize_zen_to_han(self, text: str) -> str:
        text = mojimoji.zen_to_han(text, kana=False, ascii=False)

        re_match = re.search("[0-9][，．][0-9]", text)
        if re_match:
            number_start_i, number_end_i = re_match.span()
            replaced_text = re_match.group().replace("，", ",").replace("．", ".")
            text = text[:number_start_i] + replaced_text + text[number_end_i:]

        return text

    def _remove_comma_inside_digits(self, text: str) -> str:
        re_match = re.search("(([0-9]{1,3}(,[0-9]{3})*)(?![0-9]))", text)
        if re_match:
            number_start_i, number_end_i = re_match.span()
            replaced_text = re_match.group().replace(",", "")
            return text[:number_start_i] + replaced_text + text[number_end_i:]
        else:
            return text
