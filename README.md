![](docs/docs/img/logo_title_wide.png)

# ja-timex

自然言語で書かれた時間情報表現を抽出/規格化するルールベースの解析器

## 概要
`ja-timex` は、現代日本語で書かれた自然文に含まれる時間情報表現を抽出し`TIMEX3`と呼ばれるアノテーション仕様に変換することで、プログラムが利用できるような形に規格化するルールベースの解析器です。

以下の機能を持っています。

- ルールベースによる日本語テキストからの日付や時刻、期間や頻度といった時間情報表現を抽出
- アラビア数字/漢数字、西暦/和暦などの多彩なフォーマットに対応
- 時間表現のdatetime/timedeltaオブジェクトへの変換サポート

### 入力

```python
from ja_timex import TimexParser

timexes = TimexParser().parse("彼は2008年4月から週に3回ジョギングを1時間行ってきた")
```

### 出力

```python
[<TIMEX3 tid="t0" type="DATE" value="2008-04-XX" text="2008年4月">,
 <TIMEX3 tid="t1" type="SET" value="P1W" freq="3X" text="週に3回">,
 <TIMEX3 tid="t2" type="DURATION" value="PT1H" text="1時間">]
```

### datetime/timedeltaへの変換

```python
# <TIMEX3 tid="t0" type="DATE" value="2008-04-XX" text="2008年4月">
In []: timexes[0].to_datetime()
Out[]: DateTime(2008, 4, 1, 0, 0, 0, tzinfo=Timezone('Asia/Tokyo'))
```


```python
# <TIMEX3 tid="t2" type="DURATION" value="PT1H" text="1時間">
In []: timexes[2].to_duration()
Out[]: Duration(hours=1)
```

## インストール

```
pip install ja-timex
```

## ドキュメント
[ja\-timex documentation](https://ja-timex.github.io/docs/)

### 参考仕様
本パッケージは、以下の論文で提案されている時間情報アノテーションの枠組みを元に作成しています。

- [1] [小西光, 浅原正幸, & 前川喜久雄. (2013). 『現代日本語書き言葉均衡コーパス』 に対する時間情報アノテーション. 自然言語処理, 20(2), 201-221.](https://www.jstage.jst.go.jp/article/jnlp/20/2/20_201/_article/-char/ja/)
- [2] [成澤克麻 (2014)「自然言語処理における数量表現の取り扱い」東北大学大学院 修士論文](http://www.cl.ecei.tohoku.ac.jp/publications/2015/mthesis2013_narisawa_submitted.pdf)
