from ja_timex.tagger.place import Place

p = Place()

patterns = []


# 基準となる単位より、繰り返しとなる単位が小さくなるようにする
#   e.g. 「3日に1日」「1日に1時間」は言えるが「1日に1ヶ月」は言えない

# :TODO 基準となる単位の数字より、繰り返しとなる単位の数字が小さくなければいけないが、ルールが複雑で表現が難しい
# ここではそのバリデーションは行わない
#   e.g. 「3日に5日」とは言えないが、「3日に5時間」「3日に5回」は言える

# 年
patterns.append({"pattern": f"{p.range}?年に{p.count}[ヶ|か|ケ|箇]?月", "value_template": "P{}Y", "freq_template": "P{}M"})
patterns.append({"pattern": f"{p.range}?年に{p.count}週", "value_template": "P{}Y", "freq_template": "P{}W"})
patterns.append({"pattern": f"{p.range}?年に{p.count}日", "value_template": "P{}Y", "freq_template": "P{}D"})
patterns.append({"pattern": f"{p.range}?年に{p.count}時間", "value_template": "P{}Y", "freq_template": "PT{}H"})
patterns.append({"pattern": f"{p.range}?年に{p.count}分", "value_template": "P{}Y", "freq_template": "PT{}M"})
patterns.append({"pattern": f"{p.range}?年に{p.count}秒", "value_template": "P{}Y", "freq_template": "PT{}S"})
patterns.append({"pattern": f"{p.range}?年に{p.count}[回|度]", "value_template": "P{}Y", "freq_template": "{}X"})

# 月
patterns.append({"pattern": f"{p.range}?[ヶ|か|ケ|箇]?月に{p.count}週", "value_template": "P{}M", "freq_template": "P{}W"})
patterns.append({"pattern": f"{p.range}?[ヶ|か|ケ|箇]?月に{p.count}日", "value_template": "P{}M", "freq_template": "P{}D"})
patterns.append({"pattern": f"{p.range}?[ヶ|か|ケ|箇]?月に{p.count}時間", "value_template": "P{}M", "freq_template": "PT{}H"})
patterns.append({"pattern": f"{p.range}?[ヶ|か|ケ|箇]?月に{p.count}分", "value_template": "P{}M", "freq_template": "PT{}M"})
patterns.append({"pattern": f"{p.range}?[ヶ|か|ケ|箇]?月に{p.count}秒", "value_template": "P{}M", "freq_template": "PT{}S"})
patterns.append({"pattern": f"{p.range}?[ヶ|か|ケ|箇]?月に{p.count}[回|度]", "value_template": "P{}M", "freq_template": "{}X"})

# 週
patterns.append({"pattern": f"{p.range}?週に{p.count}週", "value_template": "P{}W", "freq_template": "P{}W"})
patterns.append({"pattern": f"{p.range}?週に{p.count}日", "value_template": "P{}W", "freq_template": "P{}D"})
patterns.append({"pattern": f"{p.range}?週に{p.count}時間", "value_template": "P{}W", "freq_template": "PT{}H"})
patterns.append({"pattern": f"{p.range}?週に{p.count}分", "value_template": "P{}W", "freq_template": "PT{}M"})
patterns.append({"pattern": f"{p.range}?週に{p.count}秒", "value_template": "P{}W", "freq_template": "PT{}S"})
patterns.append({"pattern": f"{p.range}?週に{p.count}[回|度]", "value_template": "P{}W", "freq_template": "{}X"})

# 日
patterns.append({"pattern": f"{p.range}?日に{p.count}日", "value_template": "P{}D", "freq_template": "P{}D"})
patterns.append({"pattern": f"{p.range}?日に{p.count}時間", "value_template": "P{}D", "freq_template": "PT{}H"})
patterns.append({"pattern": f"{p.range}?日に{p.count}分", "value_template": "P{}D", "freq_template": "PT{}M"})
patterns.append({"pattern": f"{p.range}?日に{p.count}秒", "value_template": "P{}D", "freq_template": "PT{}S"})
patterns.append({"pattern": f"{p.range}?日に{p.count}[回|度]", "value_template": "P{}D", "freq_template": "{}X"})

# 時間
patterns.append({"pattern": f"{p.range}?時間に{p.count}時間", "value_template": "PT{}H", "freq_template": "PT{}H"})
patterns.append({"pattern": f"{p.range}?時間に{p.count}分", "value_template": "PT{}H", "freq_template": "PT{}M"})
patterns.append({"pattern": f"{p.range}?時間に{p.count}秒", "value_template": "PT{}H", "freq_template": "PT{}S"})
patterns.append({"pattern": f"{p.range}?時間に{p.count}[回|度]", "value_template": "P{}H", "freq_template": "{}X"})

# 分
patterns.append({"pattern": f"{p.range}?分(間)?に{p.count}分", "value_template": "PT{}M", "freq_template": "PT{}M"})
patterns.append({"pattern": f"{p.range}?分(間)?に{p.count}秒", "value_template": "PT{}M", "freq_template": "PT{}S"})
patterns.append({"pattern": f"{p.range}?分(間)?に{p.count}[回|度]", "value_template": "PT{}M", "freq_template": "{}W"})

# 秒
patterns.append({"pattern": f"{p.range}?秒(間)?に{p.count}秒", "value_template": "PT{}S", "freq_template": "PT{}S"})
patterns.append({"pattern": f"{p.range}?秒(間)?に{p.count}[回|度]", "value_template": "PT{}S", "freq_template": "{}X"})


# 「年1回」「週1日」とは言うが、「2年1回」や「3週1日」とは言わない
# valueが1で省略され、「に」を省略するパターン
patterns.append({"pattern": f"年{p.count}日", "value_template": "P1Y", "freq_template": "P{}D"})
patterns.append({"pattern": f"年{p.count}[回|度]", "value_template": "P1Y", "freq_template": "{}X"})
patterns.append({"pattern": f"月{p.count}[回|度]", "value_template": "P1M", "freq_template": "{}X"})
# 週3日、週3時間
patterns.append({"pattern": f"週{p.count}日", "value_template": "P1W", "freq_template": "P{}D"})
patterns.append({"pattern": f"週{p.count}時間", "value_template": "P1W", "freq_template": "PT{}H"})
patterns.append({"pattern": f"週{p.count}[回|度]", "value_template": "P1W", "freq_template": "{}X"})


# quant:EACH
patterns.append({"pattern": f"毎秒", "value": "PT1S", "quant": "EACH"})
patterns.append({"pattern": f"毎分", "value": "PT1M", "quant": "EACH"})
patterns.append({"pattern": f"毎時間", "value": "PT1H", "quant": "EACH"})
patterns.append({"pattern": f"毎日", "value": "P1D", "quant": "EACH"})
patterns.append({"pattern": f"毎月", "value": "P1M", "quant": "EACH"})
patterns.append({"pattern": f"毎年", "value": "P1Y", "quant": "EACH"})

# patterns.append({"pattern": f"毎{p.count}?(回|日|時間)", "quant": ""})

# quant:EVERY
patterns.append({"pattern": f"毎{p.count}?(回|日|時間)", "quant": "EVERY"})
