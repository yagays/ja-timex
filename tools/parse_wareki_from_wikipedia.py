"""
Wikipediaの「元号一覧 (日本)」より、元号とその開始年(西暦)を取得する
"""

import json
import math

import pandas as pd

dfs = pd.read_html("https://ja.wikipedia.org/wiki/%E5%85%83%E5%8F%B7%E4%B8%80%E8%A6%A7_(%E6%97%A5%E6%9C%AC)")

results = []
for df in dfs:
    # 明治以降はテーブルのフォーマットが異なるので省略 (json出力後に手動で追加する)
    if "元号名" not in df.columns:
        break

    df = df[df["元号名"]["漢字"] != "－"]
    df = df.fillna("0")

    pairs = list(zip(df["元号名"]["漢字"].to_list(), df["期間"]["始期"].str.extract("([0-9]{3,4})年")[0].to_list()))
    results += list(set(pairs))

# nanを取り除く
results = [result for result in results if not math.isnan(float(result[1]))]
# 西暦の照準で並び替える
sorted_results = sorted(results, key=lambda x: int(x[1]))
# 10文字以上の不要な記述を取り除きdict形式に変換
output = {result[0]: int(result[1]) for result in sorted_results if len(result[0]) < 10}

with open("ja_timex/dictionary/raw/wareki_raw.json", "w") as f:
    json.dump(output, f, ensure_ascii=False, indent=4)
