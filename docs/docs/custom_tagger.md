# 独自パターンの抽出

`ja-timex`では、ユーザが独自の時間情報表現の抽出パターンを記述することができます。

独自の時間情報表現のために必要な要素は以下の3つです。

- ルールを記述した`Pattern`クラスのリスト
- `Pattern`クラスで抽出した結果を`TIMEX`クラスに変換する関数
- パターンを持つ`BaseTagger`を継承したクラス


## 方法

ここでは、「皇紀XXXX年」という過去に用いられていた紀年法を抽出する方法を例に説明します。

### 1. CustomTaggerを作成する
下記のように、`CustomTagger`を作成します。

```python
import re
from typing import List

from ja_timex.tag import TIMEX
from ja_timex.tagger import BaseTagger
from ja_timex.pattern.place import Pattern

custom_pattern = [
    Pattern(
        re_pattern="皇紀(?P<kouki_year>[0-9]{1,4})年",
        parse_func=parse_kouki,
        option={},
    )
]

def parse_kouki(re_match: re.Match, pattern: Pattern) -> TIMEX:
    args = re_match.groupdict()
    span = re_match.span()

    # 皇紀から西暦に変換
    year = int(args["kouki_year"]) - 660

    return TIMEX(
        type="DATE",
        value=f"{year}-XX-XX",
        text=re_match.group(),
        mod=pattern.option.get("mod"),
        parsed=args,
        span=span,
        pattern=pattern,
    )

class CustomTagger(BaseTagger):
    def __init__(self, patterns: List[Pattern] = custom_pattern) -> None:
        self.patterns = patterns
```

抽出したい表現のパターンを`Pattern`クラスとして作成します。1つのクラスが1つの抽出パターンおよび変換方法を表し、抽出のための正規表現`re_pattern`、その変換方法のロジックを実装した`parse_func`、付加情報の`option`から構成されます。

`parse_func`に指定する関数では、正規表現で抽出した結果をもとに`TIMEX`タグを構築します。抽出する数値を利用するためには、正規表現の中で名前付きグループ`(?P<name>...)`といった表記を利用します。例として挙げた`parse_kouki()`では、`kouki_year`という名前で皇紀の年号を取得し、西暦に変換するために660を引くという操作をしています。

そして`BaseTagger`クラスを継承した`CustomTagger`クラスを作成し、コンストラクタの引数として`List[Pattern]`の変数を指定します。


### 2. TimexParserの引数に指定する
1.で作成した`CustomTagger`のインスタンスを、`TimexParser`の`custom_tagger`引数に指定します。

```python
from ja_timex.timex import TimexParser

timex_parser = TimexParser(custom_tagger=CustomTagger())
```

それ以外は同じように処理をし、抽出した結果を取得することができます。

```python
In []: timex_parser.parse("西暦2021年は皇紀2681年です")
Out[]:
[<TIMEX3 tid="t0" type="DATE" value="2021-XX-XX" text="西暦2021年">,
 <TIMEX3 tid="t1" type="DATE" value="2021-XX-XX" text="皇紀2681年">]
```

