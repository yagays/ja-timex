import re


class BasePlace:
    def __init__(self) -> None:
        pass

    def is_valid(self, target, text):
        re_pattern = getattr(self, target)
        if re.fullmatch(re_pattern, text):
            return True
        else:
            return False
