import json
import re
from abc import ABCMeta, abstractmethod
from pathlib import Path
from typing import Tuple


class BaseFilter(metaclass=ABCMeta):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def filter(self, span: Tuple[int, int], text: str) -> bool:
        raise NotImplementedError()


class NumexpFilter(BaseFilter):
    def __init__(self, unit_path: str = "dictionary/filter_unit.json") -> None:
        with Path(__file__).parent.joinpath(unit_path).open(encoding="utf8") as f:
            self.units = json.load(f)

    def filter(self, span: Tuple[int, int], text: str) -> bool:
        end_i = span[1]
        for unit in self.units:
            if re.match(f"\\s?{unit}", text[end_i:]):
                return True
        return False
