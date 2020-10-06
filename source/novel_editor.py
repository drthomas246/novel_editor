#!/usr/bin/env python3
import wikipediaapi
from janome.tokenizer import Tokenizer

import neditor


if __name__ == "__main__":
    # 初期処理
    __version__ = 'Ver 0.6.0 Beta'
    tree_folder = [
        ['data/character', u'キャラクター'],
        ['data/occupation', u'職種'],
        ['data/space', u'場所'],
        ['data/event', u'イベント'],
        ['data/image', u'イメージ'],
        ['data/nobel', u'小説']
    ]
    # タイトルを表示する
    root = neditor.title_create()
    # Janomeを使って日本語の形態素解析を起動
    tokenizer = Tokenizer()
    # wikipediaapiを起動
    wiki_wiki = wikipediaapi.Wikipedia('ja')
    # メイン画面を削除
    root.destroy()
    # 再度メイン画面を作成
    root = neditor.window_create(
        tree_folder,
        tokenizer,
        wiki_wiki,
        __version__
    )
    # ループする
    root.mainloop()
