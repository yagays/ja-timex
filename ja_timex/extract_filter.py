import json
import re
from abc import ABCMeta, abstractmethod
from pathlib import Path

from ja_timex.tag import Extract


class BaseFilter(metaclass=ABCMeta):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def filter(self, extract: Extract, text: str) -> bool:
        raise NotImplementedError()


class NumexpFilter(BaseFilter):
    """対象パターンの後に数字の単位があるかを判定する

    数字表現の一部として時間情報表現が取得されてしまうケースがあるため、
    対象パターンの後続のテキストに数値表現の単位があるかを確認する

    e.g. "7.18メートル" に対して "7.18" というパターンを取得している場合 -> True
    e.g. "7.18に開催" に対して "7.18" というパターンを取得している場合 -> False
    """

    def __init__(self, unit_path: str = "dictionary/filter_unit.json") -> None:
        with Path(__file__).parent.joinpath(unit_path).open(encoding="utf8") as f:
            self.units = json.load(f)

    def filter(self, extract: Extract, text: str) -> bool:
        start_i, end_i = extract.re_match.span()

        target_text = text[start_i:end_i]
        # 対象としている文字列が、数字と記号の表現ではなかった場合
        if not re.fullmatch(r"[0-9]+[\.\-\.,][0-9]+", target_text):
            return False

        for unit in self.units:
            if re.match(f"\\s?{unit}", text[end_i:]):
                return True
        return False


class PartialNumFilter(BaseFilter):
    """対象パターンが数字表現の一部かを判定する

    正規表現の記法によっては、数字表現の一部を取得してしまう例がある。
    与えられたパターンが数字表現の一部を間違って取得していないかをチェックする

    e.g. "これは13/13です" に対して "3/13" というパターンを取得している場合 -> True
    e.g. "これは3/13です" に対して "3/13" というパターンを取得している場合 -> False
    """

    def __init__(self) -> None:
        pass

    def filter(self, extract: Extract, text: str) -> bool:
        start_i, end_i = extract.re_match.span()

        target_text = text[start_i:end_i]
        # 対象としている文字列が、数字と記号の表現ではなかった場合
        if not re.fullmatch(r"[0-9\.\-\.,/・]+", target_text):
            return False

        if start_i != 0 and re.match(r"[0-9\+\.]", text[start_i - 1]):
            return True
        elif end_i != len(text) and re.match(r"[0-9\+\.]", text[end_i]):
            return True
        else:
            return False


class DecimalFilter(BaseFilter):
    """対象パターンが少数かを判定する

    0.1や0/1, 0-1といった表現において、0が0000年を表すことはない
    そこで、日付表現において0および記号から始まる表現かをチェックする
    """

    def __init__(self) -> None:
        pass

    def filter(self, extract: Extract, text: str) -> bool:
        start_i, end_i = extract.re_match.span()

        target_text = text[start_i:end_i]
        # 対象としている文字列が、数字と記号の表現でかつ日付表現ではなかった場合
        if not re.fullmatch(r"[0-9\.\-,/・]+", target_text) or extract.type_name != "abstime":
            return False

        if re.match(r"0[\.\-/]", target_text):
            return True
        else:
            return False
