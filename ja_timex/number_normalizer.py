import re

import mojimoji

zero = {"零": 0}
char2int = {"〇": 0, "一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}
char2power_allow_head = {"十": 1, "百": 2, "千": 3}
char2power = {"万": 4, "億": 8, "兆": 12, "京": 16, "垓": 20}
char_int_table = str.maketrans({k: str(v) for k, v in char2int.items()})


def kansuji2number(text: str) -> str:

    if text == "零":
        return "0"

    # 位取り記数法 positional notaion
    if re.fullmatch("([〇一二三四五六七八九,.，．、・])+", text):
        return text.translate(char_int_table)

    cumulative_value = 0
    current_num = 0
    current_num_sub = 0
    for char in list(text):
        if char in char2int:
            if char != "〇":
                current_num_sub = char2int[char]
            else:
                current_num_sub = current_num_sub * 10
        elif char in char2power_allow_head:
            if current_num_sub == 0:
                current_num_sub = 1

            current_num += current_num_sub * (10 ** char2power_allow_head[char])
            current_num_sub = 0
        elif char in char2power:
            cumulative_value += (current_num + current_num_sub) * 10 ** char2power[char]
            current_num = 0
            current_num_sub = 0

    result_int = cumulative_value + current_num + current_num_sub
    return str(result_int)


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
