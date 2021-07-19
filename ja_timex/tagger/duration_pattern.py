from ja_timex.tagger.place import Place

p = Place()

patterns = []


# 年
patterns.append({"pattern": f"{p.year}年(間)?", "value": ""})

# 月
patterns.append({"pattern": f"{p.month}[ヶ|か|ケ|箇]?月(間)?", "value": ""})

# 日
patterns.append({"pattern": f"{p.day}日(間)?", "value": ""})

# 世紀
patterns.append({"pattern": f"{p.century}世紀", "value": ""})

# 週
patterns.append({"pattern": f"{p.week}週(間)?", "value": ""})

# 時間
patterns.append({"pattern": f"{p.hour}時間", "value": ""})

# 分
patterns.append({"pattern": f"{p.minutes}分(間)?", "value": ""})

# 秒
patterns.append({"pattern": f"{p.second}秒(間)?", "value": ""})
patterns.append({"pattern": f"{p.second_with_ms}", "value": ""})

# 組み合わせ
# patterns.append({"pattern": f"{p.year}年{p.month}[ヶ|か|ケ|箇]月", "value": ""})
# patterns.append({"pattern": f"{p.year}年{p.month}[ヶ|か|ケ|箇]月{p.day}日", "value": ""})
# patterns.append({"pattern": f"{p.hour}時間{p.minutes}分", "value": ""})
# patterns.append({"pattern": f"{p.hour}時間{p.minutes}分{p.second}秒", "value": ""})
# patterns.append({"pattern": f"{p.minutes}分{p.second}秒", "value": ""})
