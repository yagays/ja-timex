from dataclasses import dataclass

from ja_timex.tagger.base_pattern import BasePlace


@dataclass
class ReltimePlace(BasePlace):
    year: str = "(?P<year>[0-9]{,4})"
    month: str = "(?P<month>[0-9]+)"  # 日付における月とは異なり、18ヶ月など任意の数字を取れる
    day: str = "(?P<day>[0-9]+\.?[0-9]*)"
    century: str = "(?P<century>[1-9]?[0-9]{,2})"
    week: str = "(?P<week>[0-9]+\.?[0-9]*)"
    hour: str = "(?P<hour>[0-9]+\.?[0-9]*)"
    minutes: str = "(?P<minutes>[0-9]+\.?[0-9]*)"
    second: str = "(?P<second>[0-9]+\.?[0-9]*)"
    second_with_ms: str = "(?P<second_with_ms>[0-9]+[秒][0-9]+)"

    around_prefix = "(以上|[くぐ]らい|ほど|程度|ばかり|近く|より(も)?)"


p = ReltimePlace()

patterns = []


# 年
patterns.append({"pattern": f"{p.year}年{p.around_prefix}?(前|まえ)", "mod": "BEFORE"})
patterns.append({"pattern": f"{p.year}年{p.around_prefix}?(後|あと)", "mod": "AFTER"})
patterns.append({"pattern": f"{p.year}年(はじめ|初め|始め|初頭|初期|前半|前記|頭)", "mod": "START"})
patterns.append({"pattern": f"{p.year}年(なかば|半ば|中ごろ|中頃|中盤|中旬|中期|頭)", "mod": "MID"})
patterns.append({"pattern": f"{p.year}年(後半|後期|終盤|終わり|末)", "mod": "END"})
patterns.append({"pattern": f"{p.year}年([こご]ろ|頃|近く|前後|くらい|ばかり)", "mod": "APPROX"})

# 月
patterns.append({"pattern": f"{p.month}月{p.around_prefix}?(前|まえ)", "mod": "BEFORE"})
patterns.append({"pattern": f"{p.month}月{p.around_prefix}?(後|あと)", "mod": "AFTER"})

# 日
patterns.append({"pattern": f"{p.day}日{p.around_prefix}?(前|まえ)", "mod": "BEFORE"})
patterns.append({"pattern": f"{p.day}日{p.around_prefix}?(後|あと)", "mod": "AFTER"})

# 世紀
patterns.append({"pattern": f"{p.century}世紀{p.around_prefix}?(前|まえ)", "mod": "BEFORE"})
patterns.append({"pattern": f"{p.century}世紀{p.around_prefix}?(後|あと)", "mod": "AFTER"})

# 週
patterns.append({"pattern": f"{p.week}週{p.around_prefix}?(前|まえ)", "mod": "BEFORE"})
patterns.append({"pattern": f"{p.week}週{p.around_prefix}?(後|あと)", "mod": "AFTER"})

# 時間
patterns.append({"pattern": f"{p.hour}時間{p.around_prefix}?(前|まえ)", "mod": "BEFORE"})
patterns.append({"pattern": f"{p.hour}時間{p.around_prefix}?(後|あと)", "mod": "AFTER"})

# 分
patterns.append({"pattern": f"{p.minutes}分{p.around_prefix}?(前|まえ)", "mod": "BEFORE"})
patterns.append({"pattern": f"{p.minutes}分{p.around_prefix}?(後|あと)", "mod": "AFTER"})

# 秒
patterns.append({"pattern": f"{p.second}秒{p.around_prefix}?(前|まえ)", "mod": "BEFORE"})
patterns.append({"pattern": f"{p.second}秒{p.around_prefix}?(後|あと)", "mod": "AFTER"})


# {"pattern":"以前", "process_type":"or_less"}
# {"pattern":"まで", "process_type":"made"}
# {"pattern":"迄", "process_type":"or_less"}
# {"pattern":"より前", "process_type":"less"}
# {"pattern":"以降", "process_type":"or_over"}
# {"pattern":"より後", "process_type":"over"}
# {"pattern":"~", "process_type":"kara_suffix"}
# {"pattern":"〜", "process_type":"kara_suffix"}
# {"pattern":"～", "process_type":"kara_suffix"}
# {"pattern":"-", "process_type":"kara_suffix"}
# {"pattern":"−", "process_type":"kara_suffix"}
# {"pattern":"ー", "process_type":"kara_suffix"}
# {"pattern":"から", "process_type":"kara_suffix"}
# {"pattern":"上旬", "process_type":"joujun"}
# {"pattern":"中旬", "process_type":"tyujun"}
# {"pattern":"下旬", "process_type":"gejun"}
# {"pattern":"PM", "process_type":"gogo"}
# {"pattern":"AM", "process_type":"gozen"}
# {"pattern":"ＰＭ", "process_type":"gogo"}
# {"pattern":"ＡＭ", "process_type":"gozen"}
# {"pattern":"PM", "process_type":"gogo"}
# {"pattern":"AM", "process_type":"gozen"}
# {"pattern":"　ＰＭ", "process_type":"gogo"}
# {"pattern":"　ＡＭ", "process_type":"gozen"}
