# ja-timex

![logo](img/logo_title_34_small.png){align=right}

`ja-timex` は、現代日本語で書かれた自然文に含まれる時間情報表現を抽出し`TIMEX3`と呼ばれるアノテーション仕様に変換することで、プログラムが利用できる形に規格化するルールベースの解析器です。

### 入力

```python
from ja_timex import TimexParser
timex_parser = TimexParser()
timex_parser.parse("彼は2008年4月から週に3回のジョギングを、朝8時から1時間行ってきた")
```

### 出力

```python
[<TIMEX3 tid="t0" type="DATE" value="2008-04-XX" text="2008年4月">,
 <TIMEX3 tid="t1" type="SET" value="P1W" freq="3X" text="週に3回">,
 <TIMEX3 tid="t2" type="TIME" value="T08-XX-XX" text="朝8時">,
 <TIMEX3 tid="t3" type="DURATION" value="PT1H" text="1時間">]
```
