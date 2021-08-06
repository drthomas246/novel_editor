# 使用方法

- 開発環境は、Windows 10 Python Version 3.7.4 64bit版を使用しています。
- Ubuntu 19.04でも起動できることを確認しました。(但し、文章の読み上げはできません。)
- それ以外の環境でもPythonのバージョンが合えば実行できるかと思いますが、確認は取れていないので自己責任でお願いします。
- jaconv (文字変換)ライブラリとjanome (形態素解析エンジン)ライブラリ、pyttsx3(音声合成)ライブラリ、Wikipedia-API(wikipedia検索)ライブラリ、Pillow(画像処理)ライブラリ、requests(HTTP)ライブラリを使用しています。
- インストールされていない方は、下記のコードをターミナルエディタに記入しインストールしてください。
```
python -m pip install jaconv
python -m pip install Janome
python -m pip install 'pyttsx3==2.71'
python -m pip install wikipedia-api
python -m pip install Pillow
python -m pip install requests
```

- sourceフォルダにnovel_editor.pyファイルが入っています。これがメインソースファイルです。

- 上記ライブラリ以外は標準ライブラリを使っていますので、上記をインストールすれば、実行できるはずです。
