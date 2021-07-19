from ja_timex.tagger.place import Place

p = Place()

patterns = []


# 年
patterns.append({"pattern": f"年(に)?{p.count}?(回|日|時間)", value: "Y", "quant": ""})
patterns.append({"pattern": f"週(に)?{p.count}?(回|日|時間|分|秒)", value: "W", "quant": ""})
patterns.append({"pattern": f"日(に)?{p.count}?(回|日|時間|分|秒)", value: "D", "quant": ""})
patterns.append({"pattern": f"{p.second}秒間に{p.count}回", value: "D", "quant": ""})

# 年100日
# 年間100回
# 年間/月間/


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
