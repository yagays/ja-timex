# クイックスタート

## `ja_timex`で文字列をパースする
`ja_timex`から`TimexParser`クラスをインポートして、日付や時間が含まれている文字列を解析します。

```python
from ja_timex import TimexParser

timex_parser = TimexParser()
timexes = timex_parser.parse("彼は2008年4月から週に3回ジョギングを1時間行ってきた")
```

解析結果は`List[TIMEX]`で得られます。

```python
In []: timexes
Out[]:
[<TIMEX3 tid="t0" type="DATE" value="2008-04-XX" text="2008年4月">,
 <TIMEX3 tid="t1" type="SET" value="P1W" freq="3X" text="週に3回">,
 <TIMEX3 tid="t2" type="DURATION" value="PT1H" text="1時間">]
```

## 規格化された時間情報表現`TIMEX`

各要素の`TIMEX`クラスは、TIMEX3の仕様に従って規格化された時間情報表現のdataclassです。

```python
In []: timexes[0].type
Out[]: 'DATE'

In []: timexes[0].value
Out[]: '2008-04-XX'
```

詳しくは[TIMEXの仕様](timex3.md)を参照ください。

## Pythonのdatetimeに変換する
`TIMEX`クラスからPythonのdatetime形式に変換することができます。

```python
In []: timex_date = timex.parse("2021年7月18日")[0]

In []: timex_date.to_datetime()
Out[]: datetime.datetime(2021, 7, 18, 0, 0)
```

なお、`DATE`の場合は年,月,日が、`TIME`の場合は時間,分が揃っていなければエラーとなります。