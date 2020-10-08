#!/usr/bin/env python3
import locale

import wikipediaapi
from janome.tokenizer import Tokenizer

import neditor
import i18n


if __name__ == "__main__":
    # 多言語化処理
    locale_var = locale.getdefaultlocale()
    dic = i18n.initialize(locale_var)
    # 初期処理
    __version__ = 'Ver 0.7.0 Beta'
    TREE_FOLDER = [
        ['data/character', dic.get_dict("Character")],
        ['data/occupation', dic.get_dict("Occupation")],
        ['data/space', dic.get_dict("Space")],
        ['data/event', dic.get_dict("Event")],
        ['data/image', dic.get_dict("Image")],
        ['data/nobel', dic.get_dict("Novel")]
    ]
    # タイトルを表示する
    root = neditor.title_create(locale_var)
    # Janomeを使って日本語の形態素解析を起動
    tokenizer = Tokenizer()
    # wikipediaapiを起動
    wiki_wiki = wikipediaapi.Wikipedia('ja')
    # メイン画面を削除
    root.destroy()
    # 再度メイン画面を作成
    root = neditor.window_create(
        locale_var,
        TREE_FOLDER,
        tokenizer,
        wiki_wiki,
        __version__
    )
    # ループする
    root.mainloop()
