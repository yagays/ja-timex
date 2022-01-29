# 時刻表現の数値の正規化

`ja-timex`では時刻表現を取得する前に、時刻表現の数値の正規化を行います。

## 正規化とTIMEXの関係
時刻表現の数値の正規化では、下記のような処理が行われます。

| 処理内容               | 正規化前     | 正規化後 |
| ---------------------- | ------------ | -------- |
| 全角から半角への変換   | ２０２１年   | 2021年   |
| 漢数字の算用数字化     | 明治二十六年 | 明治26年 |
| 桁数を表すコンマの削除 | 1,000時間    | 1000時間 |

`TIMEX`クラスのクラス変数である`text`および`span`は、**正規化後**のテキストおよび開始/終了位置が利用されます。下記の例では、「明治二十六年」ではなく正規化後の「明治26年」と、その文字列長に対応した開始/終了位置が利用されます。

```python
In []: timex_parser = TimexParser()
  ...: timexes = timex_parser.parse("明治二十六年")

In []: timexes[0].text
Out[]: '明治26年'

In []: timexes[0].span
Out[]: (0, 5)
```

## 正規化前の数値の取得方法
正規化前のテキストや開始/終了位置を取得するには、`TIMEX`クラスの`raw_text`および`raw_span`のクラス変数を利用します。

```python
In []: timexes[0].raw_text
Out[]: '明治二十六年'

In []: timexes[0].raw_span
Out[]: (0, 6)
```

なお、正規化が行われない時刻表現に関しては、それぞれのクラス変数`text`と`raw_text`および`span`と`raw_span`は一致します。

## 正規化前後の入力文の取得
正規化前後の入力文を取得するには、`TimexParser`のインスタンスの`raw_text`および`processed_text`を利用します。

```python
In []: timex_parser.raw_text
Out[]: '明治二十六年'

In []: timex_parser.processed_text
Out[]: '明治26年'
```