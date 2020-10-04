"""Scrutinizer用設定.

・coverageを読み取るようにするための設定。
novel_editorはtkinterが読み込まれているので、Scrutinizerではcoverageできない。
なのでローカルで.coverageを作成することにする。これは、Scrutinizer用に.coverageを読
み込んで書き込んでいるだけ。
"""
with open('.coverage') as f:
    t = f.read()

with open('.coverage', mode='w') as f:
    f.write(t)
