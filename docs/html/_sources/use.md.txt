# 使用方法

- 開発環境は、Windows 11 Pro 23H2 Python Version 3.12.3 64bit版を使用しています。
- Ubuntu 19.04でも起動できることを確認しました。(但し、文章の読み上げはできません。)
- それ以外の環境でもPythonのバージョンが合えば実行できるかと思いますが、確認は取れていないので自己責任でお願いします。
- jaconv (文字変換)ライブラリとjanome (形態素解析エンジン)ライブラリ、pyttsx3(音声合成)ライブラリ、Wikipedia-API(wikipedia検索)ライブラリ、Pillow(画像処理)ライブラリを使用しています。
- インストールされていない方は、下記のコードをターミナルエディタに記入しインストールしてください。
```
pip install jaconv
pip install Janome
pip install pyttsx3
pip install wikipedia-api
pip install Pillow
```

- sourceフォルダにnovel_editor.pyファイルが入っています。これがメインソースファイルです。

- 上記ライブラリ以外は標準ライブラリを使っていますので、上記をインストールすれば、実行できるはずです。