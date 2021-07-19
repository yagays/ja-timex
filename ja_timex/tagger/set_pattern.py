from ja_timex.tagger.place import Place

p = Place()

patterns = []


# 基準となる単位より、繰り返しとなる単位が同じかまたは小さくなるようにする
#   e.g. 「3ヶ月に1ヶ月」「1ヶ月に1日」は言えるが「1ヶ月に1年」は言えない
# :TODO 基準となる単位の数字より、繰り返しとなる単位の数字が小さくなければいけないが、ルールが複雑で表現難しい
#   e.g. 「3日に5日」とは言えないが、「3日に5時間」「3日に5回」は言える

# 年
patterns.append({"pattern": f"{p.range}?年(に)?{p.count}年", "value_template": "P{}Y", "freq_template": "P{}Y"})
patterns.append({"pattern": f"{p.range}?年(に)?{p.count}[ヶ|か|ケ|箇]?月", "value_template": "P{}Y", "freq_template": "P{}M"})
patterns.append({"pattern": f"{p.range}?年(に)?{p.count}週", "value_template": "P{}Y", "freq_template": "P{}W"})
patterns.append({"pattern": f"{p.range}?年(に)?{p.count}日", "value_template": "P{}Y", "freq_template": "P{}D"})
patterns.append({"pattern": f"{p.range}?年(に)?{p.count}時間", "value_template": "P{}Y", "freq_template": "PT{}H"})
patterns.append({"pattern": f"{p.range}?年(に)?{p.count}分", "value_template": "P{}Y", "freq_template": "PT{}M"})
patterns.append({"pattern": f"{p.range}?年(に)?{p.count}秒", "value_template": "P{}Y", "freq_template": "PT{}S"})
patterns.append({"pattern": f"{p.range}?年(に)?{p.count}回", "value_template": "P{}Y", "freq_template": "{}X"})

# 月
patterns.append({"pattern": f"{p.range}?[ヶ|か|ケ|箇]?月(に)?{p.count}[ヶ|か|ケ|箇]?月", "value_template": "P{}M", "freq_template": "P{}M"})
patterns.append({"pattern": f"{p.range}?[ヶ|か|ケ|箇]?月(に)?{p.count}週", "value_template": "P{}M", "freq_template": "P{}W"})
patterns.append({"pattern": f"{p.range}?[ヶ|か|ケ|箇]?月(に)?{p.count}日", "value_template": "P{}M", "freq_template": "P{}D"})
patterns.append({"pattern": f"{p.range}?[ヶ|か|ケ|箇]?月(に)?{p.count}時間", "value_template": "P{}M", "freq_template": "PT{}H"})
patterns.append({"pattern": f"{p.range}?[ヶ|か|ケ|箇]?月(に)?{p.count}分", "value_template": "P{}M", "freq_template": "PT{}M"})
patterns.append({"pattern": f"{p.range}?[ヶ|か|ケ|箇]?月(に)?{p.count}秒", "value_template": "P{}M", "freq_template": "PT{}S"})
patterns.append({"pattern": f"{p.range}?[ヶ|か|ケ|箇]?月(に)?{p.count}回", "value_template": "P{}M", "freq_template": "{}X"})

# 週
patterns.append({"pattern": f"{p.range}?週(に)?{p.count}週", "value_template": "P{}W", "freq_template": "P{}W"})
patterns.append({"pattern": f"{p.range}?週(に)?{p.count}日", "value_template": "P{}W", "freq_template": "P{}D"})
patterns.append({"pattern": f"{p.range}?週(に)?{p.count}時間", "value_template": "P{}W", "freq_template": "PT{}H"})
patterns.append({"pattern": f"{p.range}?週(に)?{p.count}分", "value_template": "P{}W", "freq_template": "PT{}M"})
patterns.append({"pattern": f"{p.range}?週(に)?{p.count}秒", "value_template": "P{}W", "freq_template": "PT{}S"})
patterns.append({"pattern": f"{p.range}?週(に)?{p.count}回", "value_template": "P{}W", "freq_template": "{}X"})

# 日
patterns.append({"pattern": f"{p.range}?日(に)?{p.count}日", "value_template": "P{}D", "freq_template": "P{}D"})
patterns.append({"pattern": f"{p.range}?日(に)?{p.count}時間", "value_template": "P{}D", "freq_template": "PT{}H"})
patterns.append({"pattern": f"{p.range}?日(に)?{p.count}分", "value_template": "P{}D", "freq_template": "PT{}M"})
patterns.append({"pattern": f"{p.range}?日(に)?{p.count}秒", "value_template": "P{}D", "freq_template": "PT{}S"})
patterns.append({"pattern": f"{p.range}?日(に)?{p.count}回", "value_template": "P{}D", "freq_template": "{}X"})

# 時間
patterns.append({"pattern": f"{p.range}?時間(に)?{p.count}時間", "value_template": "PT{}H", "freq_template": "PT{}H"})
patterns.append({"pattern": f"{p.range}?時間(に)?{p.count}分", "value_template": "PT{}H", "freq_template": "PT{}M"})
patterns.append({"pattern": f"{p.range}?時間(に)?{p.count}秒", "value_template": "PT{}H", "freq_template": "PT{}S"})
patterns.append({"pattern": f"{p.range}?時間(に)?{p.count}回", "value_template": "P{}H", "freq_template": "{}X"})

# 分
patterns.append({"pattern": f"{p.range}?分(に)?{p.count}分", "value_template": "PT{}M", "freq_template": "PT{}M"})
patterns.append({"pattern": f"{p.range}?分(に)?{p.count}秒", "value_template": "PT{}M", "freq_template": "PT{}S"})
patterns.append({"pattern": f"{p.range}?分(に)?{p.count}回", "value_template": "PT{}M", "freq_template": "{}W"})

# 秒
patterns.append({"pattern": f"{p.range}?秒間に?{p.count}秒", "value_template": "PT{}S", "freq_template": "PT{}S"})
patterns.append({"pattern": f"{p.range}?秒間に?{p.count}回", "value_template": "PT{}S", "freq_template": "{}X"})


# 年100日
# 年間100回
# 年間/月間/
# 半日


# quant:EACH
patterns.append({"pattern": f"毎秒", "value": "PT1S", "quant": "EACH"})
patterns.append({"pattern": f"毎分", "value": "PT1M", "quant": "EACH"})
patterns.append({"pattern": f"毎時間", "value": "PT1H", "quant": "EACH"})
patterns.append({"pattern": f"毎日", "value": "P1D", "quant": "EACH"})
patterns.append({"pattern": f"毎月", "value": "P1M", "quant": "EACH"})
patterns.append({"pattern": f"毎年", "value": "P1Y", "quant": "EACH"})

# patterns.append({"pattern": f"毎{p.count}?(回|日|時間)", "quant": ""})

# quant:EVERY
patterns.append({"pattern": f"毎{p.count}?(回|日|時間)", "quant": ""})
