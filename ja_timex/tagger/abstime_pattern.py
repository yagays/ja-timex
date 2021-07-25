from ja_timex.tagger.place import Place

p = Place()
patterns = []


# 日付
date_templates = [
    f"{p.calendar_year}年{p.calendar_month}月{p.calendar_day}日",
    f"{p.calendar_month}月{p.calendar_day}日",  # 年は表現できる範囲が広いため、年/月より月/日を優先する
    f"{p.calendar_year}年{p.calendar_month}月",
    f"{p.calendar_year}年",
    f"{p.calendar_month}月",
    f"{p.calendar_day}日",
]
for delimiter in ["/", "\-", "\.", "・", ","]:
    date_templates.append(f"{p.calendar_year}年?{delimiter}{p.calendar_month}月?{delimiter}{p.calendar_day}日?")
    date_templates.append(f"{p.calendar_month}月?{delimiter}{p.calendar_day}日?")
    date_templates.append(f"{p.calendar_year}年?{delimiter}{p.calendar_month}月?")

# 日付がある表記には曜日が記載される場合がある
date_templates += [
    f"{p.calendar_year}年{p.calendar_month}月{p.calendar_day}日{p.weekday_with_symbol}",
    f"{p.calendar_month}月{p.calendar_day}日{p.weekday_with_symbol}",
    f"{p.calendar_day}日{p.weekday_with_symbol}",
]
for delimiter in ["/", "\-", "\.", "・", ","]:
    date_templates.append(
        f"{p.calendar_year}年?{delimiter}{p.calendar_month}月?{delimiter}{p.calendar_day}日?{p.weekday_with_symbol}"
    )
    date_templates.append(f"{p.calendar_month}月?{delimiter}{p.calendar_day}日?{p.weekday_with_symbol}")


for date_template in date_templates:
    add_pattern = {
        "pattern": date_template,
        "value": "",
    }
    patterns.append(add_pattern)


# 曜日
weekday2id = {"月": "1", "火": "2", "水": "3", "木": "4", "金": "5", "土": "6", "日": "7"}
patterns.append({"pattern": p.weekday_with_symbol, "value": ""})

# 季節
season2id = {"春": "SP", "夏": "SU", "秋": "FA", "冬": "WI"}
patterns.append({"pattern": f"({p.calendar_year}[年|/]?)?{p.season}", "value": ""})

# 四半期
patterns.append({"pattern": f"(第{p.quarter}四半期)", "value": ""})
patterns.append({"pattern": f"(Q{p.quarter})", "value": ""})
patterns.append({"pattern": f"({p.quarter}Q)", "value": ""})

# 年度
patterns.append({"pattern": p.fiscal_year, "value": ""})

# 世紀
patterns.append({"pattern": p.ac_century, "value": ""})

# 年 (紀元前)
patterns.append({"pattern": p.bc_year, "value": ""})

# 世紀 (紀元前)
patterns.append({"pattern": p.bc_century, "value": ""})
