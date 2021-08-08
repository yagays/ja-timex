import re

from ja_timex.pattern.place import Pattern, Place
from ja_timex.tag import TIMEX

p = Place()

patterns = []


# 基準となる単位より、繰り返しとなる単位が小さくなるようにする
#   e.g. 「3日に1日」「1日に1時間」は言えるが「1日に1ヶ月」は言えない

# :TODO 基準となる単位の数字より、繰り返しとなる単位の数字が小さくなければいけないが、ルールが複雑で表現が難しい
# ここではそのバリデーションは行わない
#   e.g. 「3日に5日」とは言えないが、「3日に5時間」「3日に5回」は言える


def parse_count_range(re_match: re.Match, pattern: Pattern) -> TIMEX:
    args = re_match.groupdict()
    span = re_match.span()

    # 「週1回」などrangeが存在しない場合は、1で埋める
    if not args.get("range"):
        args["range"] = "1"

    value = pattern.option["value_template"].format(args["range"])
    freq = pattern.option["freq_template"].format(args["count"])
    return TIMEX(
        type="SET",
        value=value,
        text=re_match.group(),
        freq=freq,
        parsed=args,
        span=span,
        pattern=pattern,
    )


def parse_quant(re_match: re.Match, pattern: Pattern) -> TIMEX:
    args = re_match.groupdict()
    span = re_match.span()

    if "value" in pattern.option:
        # EACHの場合
        value = pattern.option["value"]
    else:
        # EVERYの場合
        value = pattern.option["value_template"].format(args["range"])

    return TIMEX(
        type="SET",
        value=value,
        text=re_match.group(),
        quant=pattern.option["quant"],
        parsed=args,
        span=span,
        pattern=pattern,
    )


# 年
patterns += [
    Pattern(
        re_pattern=f"{p.range}?年に{p.count}[ヶ|か|カ|ケ|箇]?月",
        parse_func=parse_count_range,
        option={"value_template": "P{}Y", "freq_template": "P{}M"},
    ),
    Pattern(
        re_pattern=f"{p.range}?年に{p.count}週",
        parse_func=parse_count_range,
        option={"value_template": "P{}Y", "freq_template": "P{}W"},
    ),
    Pattern(
        re_pattern=f"{p.range}?年に{p.count}日",
        parse_func=parse_count_range,
        option={"value_template": "P{}Y", "freq_template": "P{}D"},
    ),
    Pattern(
        re_pattern=f"{p.range}?年に{p.count}時間",
        parse_func=parse_count_range,
        option={"value_template": "P{}Y", "freq_template": "PT{}H"},
    ),
    Pattern(
        re_pattern=f"{p.range}?年に{p.count}分",
        parse_func=parse_count_range,
        option={"value_template": "P{}Y", "freq_template": "PT{}M"},
    ),
    Pattern(
        re_pattern=f"{p.range}?年に{p.count}秒",
        parse_func=parse_count_range,
        option={"value_template": "P{}Y", "freq_template": "PT{}S"},
    ),
    Pattern(
        re_pattern=f"{p.range}?年に{p.count}[回|度]",
        parse_func=parse_count_range,
        option={"value_template": "P{}Y", "freq_template": "{}X"},
    ),
]

# 月
patterns += [
    Pattern(
        re_pattern=f"{p.range}?[ヶ|か|カ|ケ|箇]?月に{p.count}週",
        parse_func=parse_count_range,
        option={"value_template": "P{}M", "freq_template": "P{}W"},
    ),
    Pattern(
        re_pattern=f"{p.range}?[ヶ|か|カ|ケ|箇]?月に{p.count}日",
        parse_func=parse_count_range,
        option={"value_template": "P{}M", "freq_template": "P{}D"},
    ),
    Pattern(
        re_pattern=f"{p.range}?[ヶ|か|カ|ケ|箇]?月に{p.count}時間",
        parse_func=parse_count_range,
        option={"value_template": "P{}M", "freq_template": "PT{}H"},
    ),
    Pattern(
        re_pattern=f"{p.range}?[ヶ|か|カ|ケ|箇]?月に{p.count}分",
        parse_func=parse_count_range,
        option={"value_template": "P{}M", "freq_template": "PT{}M"},
    ),
    Pattern(
        re_pattern=f"{p.range}?[ヶ|か|カ|ケ|箇]?月に{p.count}秒",
        parse_func=parse_count_range,
        option={"value_template": "P{}M", "freq_template": "PT{}S"},
    ),
    Pattern(
        re_pattern=f"{p.range}?[ヶ|か|カ|ケ|箇]?月に{p.count}[回|度]",
        parse_func=parse_count_range,
        option={"value_template": "P{}M", "freq_template": "{}X"},
    ),
]

# 週
patterns += [
    Pattern(
        re_pattern=f"{p.range}?週に{p.count}週",
        parse_func=parse_count_range,
        option={"value_template": "P{}W", "freq_template": "P{}W"},
    ),
    Pattern(
        re_pattern=f"{p.range}?週に{p.count}日",
        parse_func=parse_count_range,
        option={"value_template": "P{}W", "freq_template": "P{}D"},
    ),
    Pattern(
        re_pattern=f"{p.range}?週に{p.count}時間",
        parse_func=parse_count_range,
        option={"value_template": "P{}W", "freq_template": "PT{}H"},
    ),
    Pattern(
        re_pattern=f"{p.range}?週に{p.count}分",
        parse_func=parse_count_range,
        option={"value_template": "P{}W", "freq_template": "PT{}M"},
    ),
    Pattern(
        re_pattern=f"{p.range}?週に{p.count}秒",
        parse_func=parse_count_range,
        option={"value_template": "P{}W", "freq_template": "PT{}S"},
    ),
    Pattern(
        re_pattern=f"{p.range}?週に{p.count}[回|度]",
        parse_func=parse_count_range,
        option={"value_template": "P{}W", "freq_template": "{}X"},
    ),
]

# 日
patterns += [
    Pattern(
        re_pattern=f"{p.range}?日に{p.count}日",
        parse_func=parse_count_range,
        option={"value_template": "P{}D", "freq_template": "P{}D"},
    ),
    Pattern(
        re_pattern=f"{p.range}?日に{p.count}時間",
        parse_func=parse_count_range,
        option={"value_template": "P{}D", "freq_template": "PT{}H"},
    ),
    Pattern(
        re_pattern=f"{p.range}?日に{p.count}分",
        parse_func=parse_count_range,
        option={"value_template": "P{}D", "freq_template": "PT{}M"},
    ),
    Pattern(
        re_pattern=f"{p.range}?日に{p.count}秒",
        parse_func=parse_count_range,
        option={"value_template": "P{}D", "freq_template": "PT{}S"},
    ),
    Pattern(
        re_pattern=f"{p.range}?日に{p.count}[回|度]",
        parse_func=parse_count_range,
        option={"value_template": "P{}D", "freq_template": "{}X"},
    ),
]

# 時間
patterns += [
    Pattern(
        re_pattern=f"{p.range}?時間に{p.count}時間",
        parse_func=parse_count_range,
        option={"value_template": "PT{}H", "freq_template": "PT{}H"},
    ),
    Pattern(
        re_pattern=f"{p.range}?時間に{p.count}分",
        parse_func=parse_count_range,
        option={"value_template": "PT{}H", "freq_template": "PT{}M"},
    ),
    Pattern(
        re_pattern=f"{p.range}?時間に{p.count}秒",
        parse_func=parse_count_range,
        option={"value_template": "PT{}H", "freq_template": "PT{}S"},
    ),
    Pattern(
        re_pattern=f"{p.range}?時間に{p.count}[回|度]",
        parse_func=parse_count_range,
        option={"value_template": "PT{}H", "freq_template": "{}X"},
    ),
]

# 分
patterns += [
    Pattern(
        re_pattern=f"{p.range}?分(間)?に{p.count}分",
        parse_func=parse_count_range,
        option={"value_template": "PT{}M", "freq_template": "PT{}M"},
    ),
    Pattern(
        re_pattern=f"{p.range}?分(間)?に{p.count}秒",
        parse_func=parse_count_range,
        option={"value_template": "PT{}M", "freq_template": "PT{}S"},
    ),
    Pattern(
        re_pattern=f"{p.range}?分(間)?に{p.count}[回|度]",
        parse_func=parse_count_range,
        option={"value_template": "PT{}M", "freq_template": "{}X"},
    ),
]

# 秒
patterns += [
    Pattern(
        re_pattern=f"{p.range}?秒(間)?に{p.count}秒",
        parse_func=parse_count_range,
        option={"value_template": "PT{}S", "freq_template": "PT{}S"},
    ),
    Pattern(
        re_pattern=f"{p.range}?秒(間)?に{p.count}[回|度]",
        parse_func=parse_count_range,
        option={"value_template": "PT{}S", "freq_template": "{}X"},
    ),
]


# 「年1回」「週1日」とは言うが、「2年1回」や「3週1日」とは言わない
patterns += [
    Pattern(
        re_pattern=f"年に?{p.count}[ヶ|か|カ|ケ|箇]月",
        parse_func=parse_count_range,
        option={"value_template": "P{}Y", "freq_template": "P{}M"},
    ),
    Pattern(
        re_pattern=f"年に?{p.count}日",
        parse_func=parse_count_range,
        option={"value_template": "P{}Y", "freq_template": "P{}D"},
    ),
    Pattern(
        re_pattern=f"年に?{p.count}時間",
        parse_func=parse_count_range,
        option={"value_template": "P{}Y", "freq_template": "PT{}H"},
    ),
    Pattern(
        re_pattern=f"年に?{p.count}[回|度]",
        parse_func=parse_count_range,
        option={"value_template": "P{}Y", "freq_template": "{}X"},
    ),
    Pattern(
        re_pattern=f"月に?{p.count}[回|度]",
        parse_func=parse_count_range,
        option={"value_template": "P{}M", "freq_template": "{}X"},
    ),
    Pattern(
        re_pattern=f"週に?{p.count}日",
        parse_func=parse_count_range,
        option={"value_template": "P{}W", "freq_template": "P{}D"},
    ),
    Pattern(
        re_pattern=f"週に?{p.count}時間",
        parse_func=parse_count_range,
        option={"value_template": "P{}W", "freq_template": "PT{}H"},
    ),
    Pattern(
        re_pattern=f"週に?{p.count}[回|度]",
        parse_func=parse_count_range,
        option={"value_template": "P{}W", "freq_template": "{}X"},
    ),
]

# 「に」を省略するパターン
# 「1日1時間」とは言うが、「日1時間」とは言わない
patterns += [
    Pattern(
        re_pattern=f"1日{p.count}時間",
        parse_func=parse_count_range,
        option={"value_template": "P{}D", "freq_template": "PT{}H"},
    ),
    Pattern(
        re_pattern=f"1日{p.count}分",
        parse_func=parse_count_range,
        option={"value_template": "P{}D", "freq_template": "PT{}M"},
    ),
    Pattern(
        re_pattern=f"1日{p.count}秒",
        parse_func=parse_count_range,
        option={"value_template": "P{}D", "freq_template": "PT{}S"},
    ),
    Pattern(
        re_pattern=f"1日{p.count}[回|度]",
        parse_func=parse_count_range,
        option={"value_template": "P{}D", "freq_template": "{}X"},
    ),
]


# quant:EACH
patterns += [
    Pattern(
        re_pattern="毎秒",
        parse_func=parse_quant,
        option={"value": "PT1S", "quant": "EACH"},
    ),
    Pattern(
        re_pattern="毎分",
        parse_func=parse_quant,
        option={"value": "PT1M", "quant": "EACH"},
    ),
    Pattern(
        re_pattern="毎時(間)?",
        parse_func=parse_quant,
        option={"value": "PT1H", "quant": "EACH"},
    ),
    Pattern(
        re_pattern="毎日",
        parse_func=parse_quant,
        option={"value": "P1D", "quant": "EACH"},
    ),
    Pattern(
        re_pattern="毎週",
        parse_func=parse_quant,
        option={"value": "P1W", "quant": "EACH"},
    ),
    Pattern(
        re_pattern="毎月",
        parse_func=parse_quant,
        option={"value": "P1M", "quant": "EACH"},
    ),
    Pattern(
        re_pattern="毎年",
        parse_func=parse_quant,
        option={"value": "P1Y", "quant": "EACH"},
    ),
]

# quant:EVERY
patterns += [
    Pattern(
        re_pattern=f"{p.range}秒(おき|ごと)",
        parse_func=parse_quant,
        option={"value_template": "PT{}S", "quant": "EVERY"},
    ),
    Pattern(
        re_pattern=f"{p.range}分(おき|ごと)",
        parse_func=parse_quant,
        option={"value_template": "PT{}M", "quant": "EVERY"},
    ),
    Pattern(
        re_pattern=f"{p.range}時間(おき|ごと)",
        parse_func=parse_quant,
        option={"value_template": "PT{}H", "quant": "EVERY"},
    ),
    Pattern(
        re_pattern=f"{p.range}日(おき|ごと)",
        parse_func=parse_quant,
        option={"value_template": "P{}D", "quant": "EVERY"},
    ),
    Pattern(
        re_pattern=f"{p.range}週(おき|ごと)",
        parse_func=parse_quant,
        option={"value_template": "P{}W", "quant": "EVERY"},
    ),
    Pattern(
        re_pattern=f"{p.range}[ヶ|か|カ|ケ|箇]月(おき|ごと)",
        parse_func=parse_quant,
        option={"value_template": "P{}M", "quant": "EVERY"},
    ),
    Pattern(
        re_pattern="{p.range}年(おき|ごと)",
        parse_func=parse_quant,
        option={"value_template": "P{}Y", "quant": "EVERY"},
    ),
]
