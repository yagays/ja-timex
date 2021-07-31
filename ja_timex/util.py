import re


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
    start_i = re_match.span()[0]

    if start_i != 0 and re.match("[0-9]", processed_text[start_i - 1]):
        return True
    else:
        return False
