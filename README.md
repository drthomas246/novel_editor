# novel_editor

　[Explanation in English](https://github.com/drthomas246/novel_editor/wiki)

[![Build Status](https://travis-ci.org/drthomas246/novel_editor.svg?branch=master)](https://travis-ci.org/drthomas246/novel_editor)
[![coverage](https://img.shields.io/badge/coverage-97-brightgreen)](https://drthomas246.github.io/novel_editor/htmlcov/index.html)
[![ランゲージ](https://img.shields.io/badge/python-3.7.4-orange)](https://www.python.org/)
[![ソースコードサイズ](https://img.shields.io/github/languages/code-size/drthomas246/novel_editor)](https://github.com/drthomas246/novel_editor/blob/master/source/novel_editor.py)
[![ライセンス](https://img.shields.io/github/license/drthomas246/novel_editor)](https://raw.githubusercontent.com/drthomas246/novel_editor/master/LICENSE)
[![リリース](https://img.shields.io/github/v/release/drthomas246/novel_editor?include_prereleases)](https://github.com/drthomas246/novel_editor/releases)  
![ドキュメント](https://img.shields.io/badge/document-ja-green)
![コミットメッセージ](https://img.shields.io/badge/Commit_message-ja-green)
![コードコメント](https://img.shields.io/badge/code_comment-ja-green)

- python で作った、「[小説家になろう](https://syosetu.com/)」の投稿用エディタです。
- キャラクター、職種、場所、イベント、小説、をわけて管理することで小説を少しでも楽にかけるようにしてあります。
- TABキーでキャラクターに登録した、一覧を簡単に入力することができます。
- Ctrl+Rで選択文字列の漢字部分にルビを振ることができます。
- Ctrl+Uで小説家になろうのユーザーページを開くことができます。

## 使用方法

- 開発環境は、Windows 10 python Version 3.7.4 64bit版を使用しています。
- それ以外の環境でもpythonのバージョンが合えば実行できるかと思いますが、確認は取れていないので自己責任でお願いします。

- jaconv (文字変換)ライブラリとjanome (形態素解析エンジン)ライブラリを使用しています。
- インストールされていない方は、下記のコードをターミナルエディタに記入しインストールしてください。
```
$ pip install 'jaconv==0.2.4'
$ pip install 'Janome==0.3.9'
```

- sourceフォルダにnovel_editor.pyファイルが入っています。これが実行ファイルです。

- 上記ライブラリ以外は標準ライブラリを使っていますので、上記をインストールすれば、実行できるはずです。

- Windows用にコンパイルした物をdistフォルダに入れてあります。(64bit用)ダブルクリックすれば起動します。  
また、削除は、novel_editor.exeとその同じフォルダにあるdataフォルダを削除してください。レジストリは汚していません。

## コマンド一覧
- 通常時 (文字入力画面)

| コマンド | 処理内容 |
:--:|:--:
| Ctrl+E | ファイルを開く |
| Ctrl+W | 名前をつけて保存 |
| Ctrl+S | 上書き保存 |
| Ctrl+Shift+C | 文字数、行数カウントダイアログ表示 |
| Ctrl+R | 選択文字列にルビを振る |
| Ctrl+U | 小説家になろうのユーザーページを開く |
| Ctrl+X | 切り取り |
| Ctrl+C | コピー |
| Ctrl+V | ペースト |
| Ctrl+A | すべて選択 |
| Ctrl+F | 検索 |
| Ctrl+Z | UNDO |
| Ctrl+Shift+Z | REDO |
| Tab | 名前の一覧表示 |

- Tabキー押下時 (文字入力画面)

| コマンド | 処理内容 |
:--:|:--:
| Esc | 一覧表示をやめる |
| Tab | 一覧表示をやめる |
| ↑↓キー | 一覧を選択 |
| Enter | 一覧を決定 |

- 通常時 (リスト画面)

| コマンド | 処理内容 |
:--:|:--:
| キャラクター、職種、場所、イベント、小説の大項目を選択して右クリック | 小項目作成ダイアログを表示 |
| 小項目を選択して右クリック | 小項目削除ダイアログを表示 |

## その他
- py2exe.batファイルは、pyファイルをWindows等の実行ファイルに変換するためのバッチファイルです。  
使用するためには、pyinstallerを使いますので、下記のコードをターミナルエディタに記入しインストールしてください。

```
$ pip install pyinstaller
```

- 保存ファイルは.nedの拡張子をつけて保存されます。  
.nedの実体はzipファイルの拡張子を変更してあるだけですので、.zipに戻すと解凍できます。(但し、解凍ソフトによっては文字化けする恐れがあります。)  
解凍すると、dataフォルダの中に、大項目のcharacter (キャラクター)、occupation (職種)、space (場所)、event (イベント)、nobel (小説)フォルダができています。それぞれのフォルダの中に小項目のテキストフォルダができていますので、そこにデータがテキスト形式で保存されています。

- Pythonコードのカバレッジを計測するためにCoveragepyを使用しています。  
使用方法は、Coveragepyをインストールします。
```
$ pip install coverage
```
- つぎのコマンドを入力してカバレッジを計測します。
```
$ coverage run ./source/novel_editor.py arg1 arg2
```
- その後以下のコマンドを実行して、htmlcovフォルダに詳細なカバレッジレポートをHTMLで出力します。
```
$ coverage html
```

## 改変履歴

- Version 0.0.3b  
検索を追加
- Version 0.0.2b  
小説家になろうのユーザーページを開けるようにする
- Version 0.0.1b  
初版発行

## Copyright
- ファイル名：novel_editor.py、novel_editor.exe
- Version：0.0.3b
- 作者：山原　喜寛 (Yamahara Yoshihiro)
- 著作年：2019
- HP：https://www.hobofoto.net/
- E-mail：yoshihiro@yamahara.email
- ライセンス：[MIT License](https://raw.githubusercontent.com/drthomas246/novel_editor/master/LICENSE)

## Special thanks
- jaconv (文字変換)ライブラリ  
Copyright (C) 2014, Yukino Ikegami.  
Released under the MIT license  
https://raw.githubusercontent.com/ikegami-yukino/jaconv/master/LICENSE

- janome (形態素解析エンジン)ライブラリ  
Copyright(C) 2015, Tomoko Uchida. All Rights Reserved.  
This software includes the work that is distributed in the [Apache License 2.0](https://raw.githubusercontent.com/mocobeta/janome/master/LICENSE.txt).

- pyinstaller  
Copyright 2005–2019, PyInstaller Development Team.  
Distributed under the GPL license  
https://raw.githubusercontent.com/pyinstaller/pyinstaller/develop/COPYING.txt

- Coveragepy  
Copyright(C) 2009–2019, Ned Batchelder.  
This software includes the work that is distributed in the [Apache License 2.0](https://raw.githubusercontent.com/nedbat/coveragepy/v4.5.x/LICENSE.txt).


- naritoブログ  
[Tkinterで、行番号付きText](https://torina.top/detail/412/)  
[Tkinterで、検索ボックス](https://torina.top/detail/407/)  
Copyright Narito Takizawa All Rights Reserved.
