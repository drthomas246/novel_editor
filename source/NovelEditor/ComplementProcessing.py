#!/usr/bin/env python3
import tkinter as tk

from . import Definition


class ComplementProcessingClass(Definition.DefinitionClass):
    """ 補完処理のクラス.

    ・補完処理にあるプログラム群

    Args:
        app (instance): MainProcessingClass のインスタンス
        tokenizer (instance): Tokenizer のインスタンス
        locale_var (str): ロケーション
        master (instance): toplevel のインスタンス
    """
    def __init__(self, app, tokenizer, locale_var, master=None):
        super().__init__(locale_var, master)
        self.app = app
        self.tokenizer = tokenizer

    def tab(self, event=None):
        """タブ押下時の処理.

        ・タブキーを押したときに補完リストを出す。

        Args:
            event (instance): tkinter.Event のインスタンス
        """
        # 文字を選択していないとき
        sel_range = self.app.NovelEditor.tag_ranges('sel')
        if not sel_range:
            return self.auto_complete()
        else:
            return

    def auto_complete(self):
        """補完リストの設定.

        ・補完リストの設定をする。
        """
        self.auto_complete_list = tk.Listbox(self.app.NovelEditor)
        # エンターでそのキーワードを選択
        self.auto_complete_list.bind('<Return>', self.selection)
        self.auto_complete_list.bind('<Double-1>', self.selection)
        # エスケープ、タブ、他の場所をクリックで補完リスト削除
        self.auto_complete_list.bind('<Escape>', self.remove_list)
        self.auto_complete_list.bind('<Tab>', self.remove_list)
        self.auto_complete_list.bind('<FocusOut>', self.remove_list)
        # (x,y,width,height,baseline)
        x, y, width, height, _ = self.app.NovelEditor.dlineinfo(
            'insert'
        )
        # 現在のカーソル位置のすぐ下に補完リストを貼る
        self.auto_complete_list.place(x=x+width, y=y+height)
        # 補完リストの候補を作成
        for word in self.get_keywords():
            self.auto_complete_list.insert(tk.END, word)

        # 補完リストをフォーカスし、0番目を選択している状態に
        self.auto_complete_list.focus_set()
        self.auto_complete_list.selection_set(0)
        return 'break'

    def get_keywords(self):
        """補完リストの候補キーワードを作成.

        ・補完リストに表示するキーワードを得る。

        Returns:
            str: 補完リスト配列
        """
        text = ''
        text, _, _ = self.get_current_insert_word()
        my_func_and_class = set()
        # コード補完リストをTreeviewにある'名前'から得る
        children = self.app.tree.get_children('data/character')
        for child in children:
            childname = self.app.tree.item(child, "text")
            # 前列の文字列と同じものを選び出す
            if childname.startswith(text) or childname.startswith(
                text.title()
            ):
                my_func_and_class.add(childname)

        result = list(my_func_and_class)
        return result

    def remove_list(self, event=None):
        """補完リストの削除処理.

        ・補完リストを削除し、テキストボックスにフォーカスを戻す。

        Args:
            event (instance): tkinter.Event のインスタンス
        """
        self.auto_complete_list.destroy()
        self.app.NovelEditor.focus()  # テキストウィジェットにフォーカスを戻す

    def selection(self, event=None):
        """補完リストでの選択後の処理.

        ・補完リストを選択したときにその文字を入力する。

        Args:
            event (instance): tkinter.Event のインスタンス
        """
        # リストの選択位置を取得
        select_index = self.auto_complete_list.curselection()
        if select_index:
            # リストの表示名を取得
            value = self.auto_complete_list.get(select_index)

            # 現在入力中の単語位置の取得
            _, start, end = self.get_current_insert_word()
            self.app.NovelEditor.delete(start, end)
            self.app.NovelEditor.insert('insert', value)
            self.remove_list()

    def get_current_insert_word(self):
        """現在入力中の単語と位置を取得.

        ・現在入力している単語とその位置を取得する。
        """
        text = ''
        start_i = 1
        end_i = 0
        while True:
            start = 'insert-{0}c'.format(start_i)
            end = 'insert-{0}c'.format(end_i)
            text = self.app.NovelEditor.get(start, end)
            # 1文字ずつ見て、スペース、改行、タブ、空文字、句読点にぶつかったら終わり
            if text in (' ', '　', '\t', '\n', '', '、', '。'):
                text = self.app.NovelEditor.get(end, 'insert')

                # 最終単語を取得する
                pri = [
                    token.surface for token in self.tokenizer.tokenize(
                        text
                    )
                ]
                hin = [
                    token.part_of_speech.split(',')[0] for token
                    in self.tokenizer.tokenize(text)
                ]
                if len(pri) > 0:
                    if hin[len(pri)-1] == u'名詞':
                        text = pri[len(pri)-1]
                    else:
                        text = ""
                else:
                    text = ""

                end = 'insert-{0}c'.format(len(text))
                return text, end, 'insert'

            start_i += 1
            end_i += 1
