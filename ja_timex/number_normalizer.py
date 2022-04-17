import re
from dataclasses import dataclass
from typing import List, Tuple

import mojimoji

zero = {"零": 0}
char2int = {"〇": 0, "一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}
char2power_allow_head = {"十": 1, "百": 2, "千": 3}
char2power = {"万": 4, "億": 8, "兆": 12, "京": 16, "垓": 20}
char_int_table = str.maketrans({k: str(v) for k, v in char2int.items()})


@dataclass
class IgnorePhrase:
    """漢数字を含む慣用句で変換しないパターン

    pattern: 慣用句のパターン
    relative_position_to_ref: 漢数字を基準として、パターンの文字列の取りうるインデックスの相対位置
    """

    pattern: str
    relative_position_to_ref: Tuple[int, int]


@dataclass
class DiffIndex:
    """漢数字やコンマなどを対象にした文字列の正規化によって生まれたインデックスの差

    aabbbbcc (before)
    ↓
    aabbbcc  (after)
      ↑ here

    index: 正規化によって差が生まれた置換文字列の開始位置
    diff: インデックスの差異
    """

    index: int
    diff: int


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
        self.ignore_kansuji_phrase = {
            "一": [
                IgnorePhrase(pattern="一時的", relative_position_to_ref=(0, 3)),
                IgnorePhrase(pattern="一昨年", relative_position_to_ref=(0, 3)),
                IgnorePhrase(pattern="一昨日", relative_position_to_ref=(0, 3)),
                IgnorePhrase(pattern="一時代", relative_position_to_ref=(0, 3)),
                IgnorePhrase(pattern="一昨々日", relative_position_to_ref=(0, 4)),
                IgnorePhrase(pattern="一昨昨日", relative_position_to_ref=(0, 4)),
            ],
            "三": [
                IgnorePhrase(pattern="三春", relative_position_to_ref=(0, 2)),
            ],
            "四": [
                IgnorePhrase(pattern="四半世紀", relative_position_to_ref=(0, 4)),
            ],
            "六": [
                IgnorePhrase(pattern="六本木", relative_position_to_ref=(0, 3)),
            ],
            "十": [IgnorePhrase(pattern="不十分", relative_position_to_ref=(-1, 2))],
            "千": [
                IgnorePhrase(pattern="千代", relative_position_to_ref=(0, 2)),  # 千代田区
                IgnorePhrase(pattern="千春", relative_position_to_ref=(0, 2)),
                IgnorePhrase(pattern="千夏", relative_position_to_ref=(0, 2)),
                IgnorePhrase(pattern="千秋", relative_position_to_ref=(0, 2)),
                IgnorePhrase(pattern="千冬", relative_position_to_ref=(0, 2)),
            ],
        }
        self.ignore_kansuji = False
        self.diff_index_list: List[DiffIndex] = []

    def set_ignore_kansuji(self, ignore_kansuji: bool) -> None:
        """漢数字を変換しないかのパラメータをセットする

        Args:
            ignore_kansuji (bool): 漢数字の変換を無視する場合はTrue
        """
        self.ignore_kansuji = ignore_kansuji

    def normalize(self, text: str) -> str:
        self.diff_index_list = []

        text = self._normalize_zen_to_han(text)
        if not self.ignore_kansuji:
            text = self._normalize_kansuji(text)
        text = self._remove_comma_inside_digits(text)

        return text

    def _normalize_zen_to_han(self, text: str) -> str:
        """半角数字に正規化する

        全角文字の数字および全角内に含まれる句点および句読点を、すべて半角にする

        Args:
            text (str): 入力文字列

        Returns:
            str: 半角に正規化した文字列
        """
        text = mojimoji.zen_to_han(text, kana=False, ascii=False)

        # 数字の間にはいる,や.の全角文字を半角にする
        re_match = re.search("[0-9][，．][0-9]", text)
        if re_match:
            number_start_i, number_end_i = re_match.span()
            replaced_text = re_match.group().replace("，", ",").replace("．", ".")
            text = text[:number_start_i] + replaced_text + text[number_end_i:]

        return text

    def _normalize_kansuji(self, text: str) -> str:
        """漢数字をアラビア数字に正規化する

        Args:
            text (str): 入力文字列

        Returns:
            [str]: アラビア数字に正規化した文字列
        """
        re_matches = list(re.finditer("[〇一二三四五六七八九十百千万億兆京垓]+", text))
        for re_iter in reversed(re_matches):
            start_i, end_i = re_iter.span()
            replaced_text = kansuji2number(re_iter.group())

            # 慣用句などの無視すべき表現をチェックする
            should_ignore = False
            if re_iter.group() in self.ignore_kansuji_phrase:
                for ignore_phrase in self.ignore_kansuji_phrase[re_iter.group()]:
                    text_start_i = start_i + ignore_phrase.relative_position_to_ref[0]
                    text_end_i = start_i + ignore_phrase.relative_position_to_ref[1]
                    if text[text_start_i:text_end_i] == ignore_phrase.pattern:
                        should_ignore = True

            # 単体での利用ができない表現を除外
            if re_iter.group() in ("万", "億", "兆", "京", "垓"):
                should_ignore = True

            if not should_ignore:
                text = text[:start_i] + replaced_text + text[end_i:]
                self._set_diff_index(start_i, end_i, len(replaced_text))
        return text

    def _remove_comma_inside_digits(self, text: str) -> str:
        """可読性のために挿入されるカンマを削除する

        Args:
            text (str): 入力文字列

        Returns:
            str: カンマを削除した文字列
        """
        re_matches = list(re.finditer("(([0-9]{1,3}(,[0-9]{3})*)(?![0-9]))", text))
        for re_match in reversed(re_matches):
            start_i, end_i = re_match.span()
            replaced_text = re_match.group().replace(",", "")
            text = text[:start_i] + replaced_text + text[end_i:]
            self._set_diff_index(start_i, end_i, len(replaced_text))
        else:
            return text

    def _set_diff_index(self, start_i: int, end_i: int, len_replace_text: int) -> None:
        """正規化により文字列の長さに差が出た箇所を記録

        Args:
            start_i (int): 正規化文字列の開始位置
            end_i (int): 正規化文字列の終了位置
            len_replace_text (int): 正規化文字列長
        """
        diff_index = end_i - start_i - len_replace_text
        if diff_index != 0:
            self.diff_index_list.append(DiffIndex(start_i, diff_index))
