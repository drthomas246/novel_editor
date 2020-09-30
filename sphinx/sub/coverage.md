# カバレッジの計測について
- Pythonコードのカバレッジを計測するためにCoveragepyを使用しています。  
使用方法は、Coveragepyをインストールします。

```
pip install coverage
```

- つぎのコマンドを入力してカバレッジを計測します。

```
coverage run ./source/novel_editor.py
```

- その後以下のコマンドを実行して、htmlcovフォルダに詳細なカバレッジレポートをHTMLで出力します。

```
coverage html
```