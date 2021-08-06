# 基準日時と補完
`TimexParser`クラスには基準日時（Reference datetime）を設定することができます。これにより`TIMEX`クラスにおける日付や期間への変換において、表層表現からは判定することができない情報を補完します。解析対象の文書が書かれた日時が既知の場合において、明示的に基準日時を指定することで、より情報を付加した状態の日付/時間抽出が可能になります。

## 基準日時の設定
`TimexParser`クラスの`reference`引数に`pendulum`の`DateTime`インスタンスを指定します。

```py
import pendulum
from ja_timex import TimexParser

timex_parser = TimexParser(reference=pendulum.datetime(2010, 7, 18, tz="Asia/Tokyo"))
```

## 基準日時による日付/時刻表現の補完
日付や時間の解析では、Pythonの日付型/時間型に変換する`to_datetime()`メソッドにおいて、基準日時を元にして補完されます。

例として、2010年7月18日を基準日時としたときに、`12月30日`という文字列を解析します。

```py
In []: timexes = timex_parser.parse("12月30日")

In []: timexes[0]
Out[]: <TIMEX3 tid="t0" type="DATE" value="XXXX-12-30" text="12月30日">

In []: timexes[0].to_datetime()
Out[]: DateTime(2010, 12, 30, 0, 0, 0, tzinfo=Timezone('Asia/Tokyo'))
```

`TIMEX`クラスの`value`には基準日時に関係なく表層表現による値が入りますが、`to_datetime()`メソッドでdatetimeに変換した際には基準日時の2010年が補完されます。


## 基準日時による期間表現の補完
期間表現の解析では、基準日時が設定されていない場合にはPythonの日付型/時間型に`to_duration()`メソッドのみで変換できますが、設定されている場合には`to_datetime()`メソッドによって期間を考慮した変換も可能になります。

例として、2021年7月18日を基準日時としたときに、`1日前`という文字列を解析します。

```py
In []: timex_parser = TimexParser(reference=pendulum.datetime(2021, 7, 18, tz="Asia/Tokyo"))

In []: timex_parser.parse("1日前")[0].to_duration()
Out[]: Duration(days=1)

In []: timex_parser.parse("1日前")[0].to_datetime()
Out[]: DateTime(2021, 7, 17, 0, 0, 0, tzinfo=Timezone('Asia/Tokyo'))
```

以上のように、2021年7月18日の1日前である2021年7月17日が返ります。

一方、基準日時を設定していない場合には、`to_datetime()`メソッドでは下記のように`None`が返ります。

```py
In []: timex_parser = TimexParser()

In []: timex_parser.parse("1日前")[0].to_duration()
Out[]: Duration(days=1)

In []: timex_parser.parse("1日前")[0].to_datetime()
# None
```
