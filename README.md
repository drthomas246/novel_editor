# Novel Editor

　[Explanation in English](https://github.com/drthomas246/novel_editor/wiki)

[![ビルドステータス](https://scrutinizer-ci.com/g/drthomas246/novel_editor/badges/build.png?b=master)](https://scrutinizer-ci.com/g/drthomas246/novel_editor/build-status/master)
[![scrutinizerコード品質](https://scrutinizer-ci.com/g/drthomas246/novel_editor/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/drthomas246/novel_editor/?branch=master)
[![カバレッジ](https://scrutinizer-ci.com/g/drthomas246/novel_editor/badges/coverage.png?b=master)](https://drthomas246.github.io/novel_editor/htmlcov/index.html)
[![Pythonバージョン](https://img.shields.io/badge/python-3.7.4-orange)](https://www.python.org/)
[![ソースコードサイズ](https://img.shields.io/github/languages/code-size/drthomas246/novel_editor)](https://github.com/drthomas246/novel_editor/blob/master/source/novel_editor.py)
[![ライセンス](https://img.shields.io/github/license/drthomas246/novel_editor)](https://github.com/drthomas246/novel_editor/blob/master/LICENSE.md)
[![PEP8](https://img.shields.io/badge/PEP8-Correspondence-green)](https://pep8-ja.readthedocs.io/ja/latest/)
[![リリース](https://img.shields.io/github/v/release/drthomas246/novel_editor?include_prereleases)](https://github.com/drthomas246/novel_editor/releases)  
![ドキュメント](https://img.shields.io/badge/document-ja-green)
![コミットメッセージ](https://img.shields.io/badge/Commit_message-ja-green)
![コードコメント](https://img.shields.io/badge/code_comment-ja-green)

- Python で作った、「[小説家になろう](https://syosetu.com/)」の投稿用エディタです。
- 「キャラクター」、「職種」、「場所」、「イベント」、「イメージ」、「小説」をわけて管理することで小説を少しでも楽にかけるようにしてあります。
- TABキーでキャラクターに登録した、一覧を簡単に入力することができます。
- Ctrl+Rで選択文字列の漢字部分にルビを振ることができます。
- Ctrl+Shift+Rで文章を読み上げることができます。
- Ctrl+Uで小説家になろうのユーザーページを開くことができます。
- 登場人物がシンタックスハイライトされます。

## 使用方法

- Windows用にコンパイルした物がReleasesにあります(64bit用)。ダブルクリックすれば起動します。  
また、削除は、novel_editorフォルダを削除してください。レジストリは汚していません。

- __ver0.2.0b以降からセーブファイルの保存形式が変更になっています。今までのファイルを開くと最悪セーブファイル自身が破壊されてしまいます。  
ver0.2.0b以降を初めて使う場合は、申し訳ありませんが、Releasesにあるchange.exeでファイルの保存形式を変換してからご使用ください。  
一度変更するとその後は、change.exeを使用せずに保存できるようになります。__

## コマンド一覧

### 通常時 (文字入力画面)

| コマンド | 処理内容 |
:--:|:--:
| Ctrl+N | 新規作成 |
| Ctrl+E | ファイルを開く |
| Ctrl+W | 名前をつけて保存 |
| Ctrl+S | 上書き保存 |
| Ctrl+Shift+C | 文字数、行数カウントダイアログ表示 |
| Ctrl+Shift+F | フォントサイズの変更 |
| Ctrl+Shift+R | 文章の読み上げ |
| Ctrl+R | 選択文字列にルビを振る |
| Ctrl+U | 小説家になろうのユーザーページを開く |
| Ctrl+Y | 文章校正を行う |
| Ctrl+X | 切り取り |
| Ctrl+C | コピー |
| Ctrl+V | ペースト |
| Ctrl+A | すべて選択 |
| Ctrl+F | 検索 |
| Ctrl+L | 置換 |
| Ctrl+Z | UNDO |
| Ctrl+Shift+Z | REDO |
| Tab | 名前の一覧表示 |
| Ctrl+H | ヘルプを表示する |
| Ctrl+Shift+V | バージョン情報 |

### Tabキー押下時 (文字入力画面)

| コマンド | 処理内容 |
:--:|:--:
| Esc | 一覧表示をやめる |
| Tab | 一覧表示をやめる |
| ↑↓キー | 一覧を選択 |
| Enter | 一覧を決定 |

### 通常時 (リスト画面)

| コマンド | 処理内容 |
:--:|:--:
| キャラクター、職種、場所、イベント、小説の大項目を選択して右クリック | 小項目作成ダイアログを表示 |
| 小項目を選択して右クリック | 小項目削除ダイアログを表示 |
| Ctrl+G | ファイル名の変更 |

### 通常時 (イメージ画面)

| コマンド | 処理内容 |
:--:|:--:
| スクロール | 画像の上下移動 |
| Ctrl+スクロール | 画像の拡大縮小 |

## その他
### Yahoo! 校正支援
- Yahoo! 校正支援を使って校正をしています。  
そのためには、[https://www.yahoo-help.jp/app/answers/detail/p/537/a_id/43398](https://www.yahoo-help.jp/app/answers/detail/p/537/a_id/43398)を参考にアプリケーションIDを作成し、Releaseフォルダにあるappid.txtのデータに、Client IDを記入してください。

## 開発者向け
### Documentationについて
- 開発者用に[Documentation](https://drthomas246.github.io/novel_editor/html/)を置いてあります。
- 作成はsphinxを使っています。sphinxをインストールしてフォルダとプロジェクトを作成します。 

```
pip install sphinx
pip install sphinx-rtd-theme
pip install recommonmark
mkdir sphinx
sphinx-quickstart sphinx
```

- ./sphinx/conf.pyを変更します。

```python
import os
import sys
sys.path.insert(0, os.path.abspath('../source'))
# ～～～～～～～～～～～～～～～～～～～～～～～～～～
extensions = [
    'recmmonmark',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode'
]
# ～～～～～～～～～～～～～～～～～～～～～～～～～～
html_theme = 'sphinx_rtd_theme'
```

- 
- ドキュメントを生成します。

```
sphinx-apidoc -o ./sphinx ./docs
```

- htmlファイルを生成します。

```
./sphinx/make.bat html
```

## 改変履歴
- Version 0.6.0b  
置換をできるようにする
- Version 0.5.0b  
昇順検索をできるようにする
- Version 0.4.3b2  
imageの拡大縮小を保存できるようにする
- Version 0.4.3b  
imageを拡大縮小できるようにする
- Version 0.4.2b  
imageに横スクロールをつける
- Version 0.4.1b  
バージョン情報の描画方法を変える
- Version 0.4.0b2  
imageをマウスで縦スクロールできるようにする
- Version 0.4.0b  
GIFファイルを取り込めるようにする
- Version 0.3.0b2  
ハイライトのための形態素解析を見直す
- Version 0.3.0b1  
Yahoo！デベロッパーネットワークへの接続方法を変更
- Version 0.3.0b  
文章校正ができるようになる(要:Yahooデベロッパーネットワーク Client ID)
- Version 0.2.4bAM2  
似顔絵の画像処理を変更
- Version 0.2.4b1  
言葉の意味検索をgooからwikipediaへ変更
- Version 0.2.4b  
文章の読み上げ処理を改善
- Version 0.2.3b2  
軽微な変更
- Version 0.2.3b1  
言葉の意味検索を向上
- Version 0.2.3b  
似顔絵の機能を追加する
- Version 0.2.2b  
文章の読み上げ機能を追加
- Version 0.2.1b  
各OSに対応
- Version 0.2.0b1  
軽微な変更、PEP8に対応
- Version 0.2.0b  
ファイル形式を変更。キャラクター欄を充実  
今までのファイルと互換性がありません。
- Version 0.1.2b2  
バージョン情報の表示
- Version 0.1.2b1  
原稿用紙で何枚かか数えれるようになる
- Version 0.1.2b  
タイトルを挿入
- Version 0.1.1b1  
ソースを見直し
- Version 0.1.1b  
ファイル名の変更を追加
- Version 0.1.0b1  
メニューの充実
- Version 0.1.0b  
メニューを追加
- Version 0.0.7b2  
保存に関する重大な欠陥を修復
- Version 0.0.7b1  
新規作成時に変更があれば聞くようにする
- Version 0.0.7b  
新規作成を追加
- Version 0.0.6b1  
画像ファイルを取り込み
- Version 0.0.6b  
フォントサイズの変更を追加
- Version 0.0.5b1  
行番号の処理を変更
- Version 0.0.5b  
終了処理を追加
- Version 0.0.4b1  
名前のシンタックスハイライトを追加
- Version 0.0.3b  
検索を追加
- Version 0.0.2b  
小説家になろうのユーザーページを開けるようにする
- Version 0.0.1b  
初版発行

## Copyright
- ファイル名：novel_editor.py,novel_editor.exe,change.py,change.exe
- Version：0.6.0b
- 作者：山原　喜寛 (Yamahara Yoshihiro)
- 著作年：2019-2020
- HP：https://www.hobofoto.net/
- E-mail：yoshihiro@yamahara.email
- ライセンス：[GNU GPL3 License](https://github.com/drthomas246/novel_editor/blob/master/LICENSE.md)

## Special thanks
- jaconv (文字変換)ライブラリ  
Copyright (C) 2014, Yukino Ikegami.  
Released under the MIT license  
[https://raw.githubusercontent.com/ikegami-yukino/jaconv/master/LICENSE](https://raw.githubusercontent.com/ikegami-yukino/jaconv/master/LICENSE)

- janome (形態素解析エンジン)ライブラリ  
Copyright(C) 2015, Tomoko Uchida. All Rights Reserved.  
This software includes the work that is distributed in the [Apache License 2.0](https://raw.githubusercontent.com/mocobeta/janome/master/LICENSE.txt).

- pyttsx3 (音声合成)ライブラリ  
Copyright (C) 2007 Free Software Foundation, Inc.  
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.  
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.  
You should have received a copy of the GNU General Public License along with this program.  If not, see <[http://www.gnu.org/licenses/](http://www.gnu.org/licenses/)>.

- Wikipedia-API (wikipedia検索)ライブラリ  
Copyright (c) 2017 Martin Majlis  
Released under the MIT license  
[https://raw.githubusercontent.com/martin-majlis/Wikipedia-API/master/LICENSE](https://raw.githubusercontent.com/martin-majlis/Wikipedia-API/master/LICENSE)

- Pillow(画像処理)ライブラリ  
The Python Imaging Library (PIL) is  
　　Copyright © 1997-2011 by Secret Labs AB  
　　Copyright © 1995-2011 by Fredrik Lundh  
Pillow is the friendly PIL fork. It is  
　　Copyright © 2010-2020 by Alex Clark and contributors  
Released under the PIL licens  
[https://raw.githubusercontent.com/python-pillow/Pillow/master/LICENSE](https://raw.githubusercontent.com/python-pillow/Pillow/master/LICENSE)

- requests(HTTP)ライブラリ  
Copyright 2019 Kenneth Reitz  
This software includes the work that is distributed in the [Apache License 2.0](https://raw.githubusercontent.com/psf/requests/master/LICENSE)

- Yahoo! 校正支援  
Web Services by Yahoo! JAPAN （[https://developer.yahoo.co.jp/about](https://developer.yahoo.co.jp/about)）

- pyinstaller  
Copyright (c) 2010-2020, PyInstaller Development Team  
Copyright (c) 2005–2019, Giovanni Bajo  
Distributed under the GPL license  
[https://raw.githubusercontent.com/pyinstaller/pyinstaller/develop/COPYING.txt](https://raw.githubusercontent.com/pyinstaller/pyinstaller/develop/COPYING.txt)

- Coveragepy  
Copyright(C) 2009–2020, Ned Batchelder.  
This software includes the work that is distributed in the [Apache License 2.0](https://raw.githubusercontent.com/nedbat/coveragepy/v4.5.x/LICENSE.txt).

- Sphinx  
Copyright(C) 2007-2020 by the Sphinx team (see AUTHOS file).  
Released under the Sphinx licens  
[https://raw.githubusercontent.com/sphinx-doc/sphinx/3.x/LICENSE](https://raw.githubusercontent.com/sphinx-doc/sphinx/3.x/LICENSE)

### 参考文献
- naritoブログ  
[Tkinterで、行番号付きText](https://torina.top/detail/412/)  
[Tkinterで、検索ボックス](https://torina.top/detail/407/)  
[Tkinterで、Pythonコードをハイライトする](https://torina.top/detail/415/)  
Copyright Narito Takizawa All Rights Reserved.

### 使用フォント
- 数式フォント　ver1.3  
Copyright(C) 2016-2020 [キユマヤ園](http://sapphire.hacca.jp/font/fontabout.html)

- あいでぃーぽっぷまる  
Copyright(C) 2017 [Masaru Inoue](http://idfont.jp/infos_mb.htm) All Rights Reserved.

### 使用アイコン
- accessories text editor  
Copyright(C) BlueMalboro  
Creative Commons ([Attribution-Noncommercial-No Derivative Works 3.0 Unported](https://creativecommons.org/licenses/by-nc-nd/3.0/))