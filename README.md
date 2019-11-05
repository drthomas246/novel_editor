# novel_editor

　[Explanation in English](https://github.com/drthomas246/novel_editor/wiki)

[![Build Status](https://travis-ci.org/drthomas246/novel_editor.svg?branch=master)](https://travis-ci.org/drthomas246/novel_editor)
[![coverage](https://img.shields.io/badge/coverage-95-brightgreen)](https://www.hobofoto.net/htmlcov/index.html)
[![ランゲージ](https://img.shields.io/badge/python-3.7.4-orange)](https://www.python.org/)
[![ソースコードサイズ](https://img.shields.io/github/languages/code-size/drthomas246/novel_editor)](https://github.com/drthomas246/novel_editor/blob/master/source/novel_editor.py)
[![ライセンス](https://img.shields.io/badge/license-MIT-green)](https://raw.githubusercontent.com/drthomas246/novel_editor/master/LICENSE)
[![PEP8](https://img.shields.io/badge/PEP8-Correspondence-green)](https://pep8-ja.readthedocs.io/ja/latest/)
[![リリース](https://img.shields.io/github/v/release/drthomas246/novel_editor?include_prereleases)](https://github.com/drthomas246/novel_editor/releases)  
![ドキュメント](https://img.shields.io/badge/document-ja-green)
![コミットメッセージ](https://img.shields.io/badge/Commit_message-ja-green)
![コードコメント](https://img.shields.io/badge/code_comment-ja-green)

- python で作った、「[小説家になろう](https://syosetu.com/)」の投稿用エディタです。
- キャラクター、職種、場所、イベント、小説、をわけて管理することで小説を少しでも楽にかけるようにしてあります。
- TABキーでキャラクターに登録した、一覧を簡単に入力することができます。
- Ctrl+Rで選択文字列の漢字部分にルビを振ることができます。
- Ctrl+Uで小説家になろうのユーザーページを開くことができます。
- 登場人物がシンタックスハイライトされます。

## 使用方法

- 開発環境は、Windows 10 python Version 3.7.4 64bit版を使用しています。
- Ubuntu 19.04でも起動できることを確認しました。(但し、文章の読み上げ、文章校正はできません。)
- それ以外の環境でもpythonのバージョンが合えば実行できるかと思いますが、確認は取れていないので自己責任でお願いします。

- jaconv (文字変換)ライブラリとjanome (形態素解析エンジン)ライブラリ、pyttsx3(音声合成)ライブラリ、Wikipedia-API(wikipedia検索)ライブラリ、Pillow(画像処理)ライブラリ、requests(HTTP)ライブラリを使用しています。
- インストールされていない方は、下記のコードをターミナルエディタに記入しインストールしてください。
```
$ pip install 'jaconv==0.2.4'
$ pip install 'Janome==0.3.9'
$ pip install 'pyttsx3==2.71'
$ pip install 'wikipedia-api==0.5.3'
$ pip install 'Pillow==6.2.1'
$ pip install 'requests==2.22.0'
```

- sourceフォルダにnovel_editor.pyファイルが入っています。これが実行ファイルです。

- 上記ライブラリ以外は標準ライブラリを使っていますので、上記をインストールすれば、実行できるはずです。

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

## その他
### 実行ファイルに変換
- py2exe.batファイルは、pyファイルをWindows等の実行ファイルに変換するためのバッチファイルです。  
使用するためには、pyinstallerを使いますので、下記のコードをターミナルエディタに記入しインストールしてください。

```
$ pip install pyinstaller
```

### 保存ファイルについて
- 保存ファイルは.nedの拡張子をつけて保存されます。  
.nedの実体はzipファイルの拡張子を変更してあるだけですので、.zipに戻すと解凍できます。(但し、解凍ソフトによっては文字化けする恐れがあります。)  
解凍すると、dataフォルダの中に、大項目のcharacter (キャラクター)、occupation (職種)、space (場所)、event (イベント)、nobel (小説)フォルダができています。それぞれのフォルダの中に小項目のテキストフォルダができていますので、そこにデータがテキスト形式で保存されています。

### カバレッジの計測について
- Pythonコードのカバレッジを計測するためにCoveragepyを使用しています。  
使用方法は、Coveragepyをインストールします。
```
$ pip install coverage
```
- つぎのコマンドを入力してカバレッジを計測します。
```
$ coverage run ./source/novel_editor.py
```
- その後以下のコマンドを実行して、htmlcovフォルダに詳細なカバレッジレポートをHTMLで出力します。
```
$ coverage html
```
### Yahoo! 校正支援
- Yahoo! 校正支援を使って校正をしています。  
そのためには、[https://www.yahoo-help.jp/app/answers/detail/p/537/a_id/43398](https://www.yahoo-help.jp/app/answers/detail/p/537/a_id/43398)を参考にアプリケーションIDを作成し、Releaseフォルダにあるappid.txtのデータに、Client IDを記入してください。

## 改変履歴
- Version 0.3.0bAM1  
Yahoo！デベロッパーネットワークへの接続方法を変更
- Version 0.3.0bAM  
文章校正ができるようになる(要:Yahoo！デベロッパーネットワーク Client ID)
- Version 0.2.4bAM2  
似顔絵の画像処理を変更
- Version 0.2.4bAM1  
言葉の意味検索をgooからwikipediaへ変更
- Version 0.2.4bAM  
文章の読み上げ処理を改善
- Version 0.2.3bAM2  
軽微な変更
- Version 0.2.3bAM1  
言葉の意味検索を向上
- Version 0.2.3bAM  
似顔絵の機能を追加する
- Version 0.2.2bAM  
文章の読み上げ機能を追加
- Version 0.2.1bAM  
各OSに対応
- Version 0.2.0bAM1  
軽微な変更、PEP8に対応
- Version 0.2.0bAM  
ファイル形式を変更。キャラクター欄を充実  
今までのファイルと互換性がありません。
- Version 0.1.2b2AM  
バージョン情報の表示
- Version 0.1.2bAM1  
原稿用紙で何枚かか数えれるようになる
- Version 0.1.2bAM  
タイトルを挿入
- Version 0.1.1bAM1  
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
- Version：0.3.0bAM
- 作者：山原　喜寛 (Yamahara Yoshihiro)
- 著作年：2019
- HP：https://www.hobofoto.net/
- E-mail：yoshihiro@yamahara.email
- ライセンス：[MIT License](https://raw.githubusercontent.com/drthomas246/novel_editor/master/LICENSE)

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
This software is distributed under the terms of the [GNU GPL3](https://raw.githubusercontent.com/nateshmbhat/pyttsx3/master/LICENSE).

- Wikipedia-API (wikipedia検索)ライブラリ  
Copyright (c) 2017 Martin Majlis  
Released under the MIT license  
[https://raw.githubusercontent.com/martin-majlis/Wikipedia-API/master/LICENSE](https://raw.githubusercontent.com/martin-majlis/Wikipedia-API/master/LICENSE)

- Pillow(画像処理)ライブラリ  
Copyright © 2010-2019 by Alex Clark and contributors  
Released under the PIL licens
[https://raw.githubusercontent.com/python-pillow/Pillow/master/LICENSE](https://raw.githubusercontent.com/python-pillow/Pillow/master/LICENSE)

- requests(HTTP)ライブラリ  
Copyright 2019 Kenneth Reitz  
This software includes the work that is distributed in the [Apache License 2.0](https://raw.githubusercontent.com/psf/requests/master/LICENSE)

- Yahoo! 校正支援  
Web Services by Yahoo! JAPAN （[https://developer.yahoo.co.jp/about](https://developer.yahoo.co.jp/about)）

- pyinstaller  
Copyright 2005–2019, PyInstaller Development Team.  
Distributed under the GPL license  
[https://raw.githubusercontent.com/pyinstaller/pyinstaller/develop/COPYING.txt](https://raw.githubusercontent.com/pyinstaller/pyinstaller/develop/COPYING.txt)

- Coveragepy  
Copyright(C) 2009–2019, Ned Batchelder.  
This software includes the work that is distributed in the [Apache License 2.0](https://raw.githubusercontent.com/nedbat/coveragepy/v4.5.x/LICENSE.txt).

### 参考文献
- naritoブログ  
[Tkinterで、行番号付きText](https://torina.top/detail/412/)  
[Tkinterで、検索ボックス](https://torina.top/detail/407/)  
[Tkinterで、Pythonコードをハイライトする](https://torina.top/detail/415/)  
Copyright Narito Takizawa All Rights Reserved.

### 使用フォント
- 数式フォント　ver1.3  
Copyright(C) 2016-2019 [キユマヤ園](http://sapphire.hacca.jp/font/fontabout.html)

- あいでぃーぽっぷまる  
Copyright(C) 2017 [Masaru Inoue](http://idfont.jp/infos_mb.htm) All Rights Reserved.

### 使用アイコン
- accessories text editor  
Copyright(C) BlueMalboro  
Creative Commons ([Attribution-Noncommercial-No Derivative Works 3.0 Unported](https://creativecommons.org/licenses/by-nc-nd/3.0/))