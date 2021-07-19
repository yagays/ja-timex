from ja_timex.tagger.place import Place

p = Place()

patterns = []


freq_unit2template = {"年": "P{}Y", "月": "P{}M", "日": "P{}D", "時間": "PT{}H", "分": "PT{}M", "秒": "PT{}S", "回": "{}X"}
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
patterns.append({"pattern": f"{p.range}?月(に)?{p.count}[ヶ|か|ケ|箇]?月", "value_template": "P{}M", "freq_template": "P{}M"})
patterns.append({"pattern": f"{p.range}?月(に)?{p.count}週", "value_template": "P{}M", "freq_template": "P{}W"})
patterns.append({"pattern": f"{p.range}?月(に)?{p.count}日", "value_template": "P{}M", "freq_template": "P{}D"})
patterns.append({"pattern": f"{p.range}?月(に)?{p.count}時間", "value_template": "P{}M", "freq_template": "PT{}H"})
patterns.append({"pattern": f"{p.range}?月(に)?{p.count}分", "value_template": "P{}M", "freq_template": "PT{}M"})
patterns.append({"pattern": f"{p.range}?月(に)?{p.count}秒", "value_template": "P{}M", "freq_template": "PT{}S"})
patterns.append({"pattern": f"{p.range}?月(に)?{p.count}回", "value_template": "P{}M", "freq_template": "{}X"})

# 週
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
