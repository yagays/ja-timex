# クイックスタート

## `ja-timex`で文字列を解析する
`ja-timex`から`TimexParser`クラスをインポートして、日付や時間が含まれている文字列を解析します。

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

## `TIMEX`を利用する

各要素の`TIMEX`クラスは、TIMEX3の仕様に従って規格化された時間情報表現のdataclassです。

```python
In []: timex = timexes[0] 
# <TIMEX3 tid="t0" type="DATE" value="2008-04-XX" text="2008年4月">

In []: timex.type
Out[]: 'DATE'

In []: timex.value
Out[]: '2008-04-XX'
```

```python
In []: timex = timexes[1]
# <TIMEX3 tid="t1" type="SET" value="P1W" freq="3X" text="週に3回">

In []: timex.value
Out[]: 'P1W'

In []: timex.freq
Out[]: '3X'
```


詳しくは[TIMEX3タグの仕様](timex3.md)を参照ください。

## Pythonのdatetimeに変換する
日付表現は、`TIMEX`クラスからPythonのdatetime形式に変換することができます。
```python
In []: timex = timexes[0]
# <TIMEX3 tid="t0" type="DATE" value="2008-04-XX" text="2008年4月">

In []: timex.to_datetime()
Out[]: DateTime(2008, 4, 1, 0, 0, 0, tzinfo=Timezone('Asia/Tokyo'))
```

!!!Warning
    日付表現で不足している情報があった場合、`year`は実行時の年、`month`および`day`は`1`が補完されます。

!!!Tips
    ja-timexでは[`pendulum`](https://pendulum.eustace.io/)というdatetimeの扱いを容易するパッケージを利用しています。`pendulum`は基本的にPythonのdatetime/timedeltaを継承して実装されており、互換性があります。

## Pythonのtimedeltaに変換する
持続時間表現は、`TIMEX`クラスからPythonのtimedelta形式に変換することができます。

```python
In []: timex = timexes[2]
# <TIMEX3 tid="t2" type="DURATION" value="PT1H" text="1時間">

In []: timex.to_duration()
Out[]: Duration(hours=1)
```

通常のdatetime/timedeltaと同様に、計算が可能です。

```python
In []: from datetime import datetime

In []: datetime(2021, 7, 18, 12, 30) - timex.to_duration()
Out[]: datetime.datetime(2021, 7, 18, 11, 30)
```
