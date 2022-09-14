# 更新履歴

## v0.2.6(2022-09-14)
### 🐛 Bug Fixes

* to_datetime()時に「半」が考慮されない問題を修正 (#85) @yagays

## v0.2.6(2022-06-11)
### 🚀 Features

* 特定の慣用句や固有名詞をフィルターで除外する (#83) @yagays

## v0.2.5(2022-04-17)
### 🐛 Bug Fixes

* 文字列正規化により文字列長が長くなる場合にspanが補正されない問題を修正 (#82) @yagays

### 📖 Documentation and examples

* ドキュメントを更新 (#81) @yagays
* update docs (#78) @yagays
* ドキュメントを更新 (#77) @yagays

### 🚧 Maintenance

* release-drafterが対象とするデフォルトブランチ名を変更 (#80) @yagays
* ブランチ名がfeatureかfixの場合のみCIでtoxを実行 (#79) @yagays

## v.0.2.4(2022-02-23)
### 🐛 Bug Fixes

* to\_datetimeで曜日や世紀の日付表現を対象外にする (#76) @yagays

## v.0.2.3(2022-02-04)

### 🚀 Features

* 今世紀という表現をサポート (#74) @yagays
* 範囲表現でも期間を表す場合に対応 (#73) @yagays

## v.0.2.2(2022-01-29)

### 🐛 Bug Fixes

* 漢数字やコンマなどの正規化前の時刻表現の文字列とスパンをTIMEXタグに含める (#70) @yagays

### 📖 Documentation and examples

* ドキュメントに時刻表現の数値の正規化の追加 (#71) @yagays

### 🚧 Maintenance

* dev-dependenciesのバージョンを一括で上げる (#69) @yagays
* 現在の年を補完するテストを修正 (#68) @yagays

## v.0.2.1(2021-10-17)

### 🚀 Features

* Xから翌Yという表現を範囲表現として取得する (#65) @yagays
* 12:00〜17:30といった時間表現の抽出ミスを修正 (#64) @yagays

### 🐛 Bug Fixes

* 年表記で数字が小さいときもDATEとして抽出される問題を修正 (#66) @yagays

### 📖 Documentation and examples

* ドキュメントを修正 (#59) @yagays

## v.0.2.0(2021-09-05)

### 🚀 Features

* TIMEXタグの\_\_repr\_\_にrangeStart, rangeEndを追加 (#57) @yagays
* "1,2ヶ月"や"1~2分"といった複数の日付表現が列挙された場合に対応 (#56) @yagays
* TIMEXタグのrangeStartとrangeEndを追加し、抽出ルールを実装 (#55) @yagays

### 📖 Documentation and examples

* rangeStartとrangeEndに対応 (#58) @yagays

## v0.1.9(2021-08-29)

### 🚀 Features

* 数字正規化済みのテキストを利用できるように変更 (#52) @yagays

### 🐛 Bug Fixes

* 複数の漢数字を処理できない問題を修正 (#53) @yagays

### 📖 Documentation and examples

* ユーザが独自にルールを指定できるCustomTaggerのテストとドキュメントを追加 (#54) @yagays

### 🚧 Maintenance

* ユーザが独自にルールを指定できるCustomTaggerのテストとドキュメントを追加 (#54) @yagays


## v0.1.8(2021-08-22)

### 🚀 Features

* Filterの導入により対象外の表現を除外 (#49) @yagays

### 🐛 Bug Fixes

* 0.5ヶ月や3.5年前といった表現の取得ミスを修正 (#50) @yagays
* 数字の途中を日付と誤認識する問題を修正 (#48) @yagays

### 📖 Documentation and examples

* 抽出例の具体例および既存研究との差異を追加 (#47) @yagays

### 🚧 Maintenance

* stop poetry install before running tox (#51) @yagays
* Fix typos (#46) @shirayu

## v0.1.7(2021-08-15)

### 🚀 Features

* 漢数字を変換しない`ignore_kansuji`パラメータを追加 (#44) @yagays
* 末日という表現をサポート (#42) @yagays
* 16世紀頃, 紀元前2世紀近くといった表現をサポート (#40) @yagays
* 早朝6時や10時半といった表現をサポート (#36) @yagays
* 深夜0時や深夜25時といった表現をサポート (#35) @yagays
* 3日ぶりや10年ぶりといった表現をサポート (#32) @yagays
* 8日目や30年もの間といった表現をサポート (#30) @yagays

### 🐛 Bug Fixes

* 一時代を時間として取得してしまう問題を修正 (#45) @yagays
* 翌週28日が週28日と取得される問題を修正 (#39) @yagays
* remove JUST mod (#38) @yagays
* 数字が複数含まれるときに桁数のコンマ処理がされない問題を修正 (#37) @yagays
* 12：30といった全角コロンの時間表記を取得できるように修正 (#34) @yagays
* 時刻表現の後にスペースがある際にTimex.textに含まれないように修正 (#33) @yagays
* 東京・千代田区や千春,千夏,千秋,千冬といった表現を取得してしまうバグを修正 (#31) @yagays
* 全角括弧の囲みを取得するように修正 (#29) @yagays

### 📖 Documentation and examples

* update docs (#41) @yagays

## v0.1.6(2021-08-09)

### 🚀 Features

* `to_datetime()`でデフォルトのtimezoneを設定可能にする (#27) @yagays
* 1年半後や1時間半前、半年といった表現をサポート (#23) @yagays
* "半"という表現をサポート (#22) @yagays

### 🐛 Bug Fixes

* 先月や半年前などの数字を伴わない表現でto\_duration()の計算を修正 (#25) @yagays
* "世紀"の前に数字が無いとエラーが出る問題を修正 (#24) @yagays

### 📖 Documentation and examples

* 日付型/時間型への変換方法の説明を追加 (#28) @yagays
* typoを修正 (#18) @yagays

### 🚧 Maintenance

* テストを追加 (#26) @yagays
* enable to trigger with release drafter (#17) @yagays

## v0.1.5(2021-08-06)

### 🚀 Features

* 基準日を設定できるようにする (#14) @yagays
* 夜9時・今夜9時のような表現をサポート (#13) @yagays

### 📖 Documentation and examples

* 基準日時の説明を追加 (#16) @yagays

### 🚧 Maintenance

* streamlitのアプリでto\_datetime/to\_durationに対応 (#15) @yagays
* add release-drafter (#12) @yagays

## v0.1.4 (2021-08-05)

### 🐛 Bug fixes

* "毎年6月"が"年6月"と判定されるバグを修正 #4
* Windows環境でテストが通らないエラーを修正 #8

### 🚧 Maintenance

* CIを整備 #6 #10

## v0.1.3 (2021-08-01)

* バグ修正

## v0.1.2 (2021-08-01)

* 「先月」「一昨年」といった表現を追加

## v0.1.1 (2021-08-01)

* `ja-timex`リリース
* `ja-timex/docs`でドキュメント公開