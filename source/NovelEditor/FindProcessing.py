#!/usr/bin/env python3
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
from . import Definition


class FindProcessingClass(Definition.DefinitionClass):
    """検索置換のクラス.

    ・検索置換するためのプログラム群

    Args:
        app (instance): MainProcessingClass のインスタンス
        locale_var (str): ロケーション
        master (instance): toplevel のインスタンス
    """

    replacement_check = False
    """検索ダイアログが表示されているTrue."""
    next_pos = ""
    """次の検索位置 例.(1.0)."""
    find_text = ""
    """検索文字列."""

    def __init__(self, app, locale_var, master=None):
        super().__init__(locale_var, master)
        self.app = app

    def push_keys(self, event=None):
        """キーが押されたときの処理.

        ・何かキーが押されたときに検索処理を中断する。

        Args:
            event (instance): tkinter.Event のインスタンス
        """
        # 検索処理を中断する
        self.replacement_check_input(False)

    def find_dialog(self, event=None):
        """検索ダイアログを作成.

        ・検索ダイアログを作成する。

        Args:
            event (instance): tkinter.Event のインスタンス
        """
        search_win = tk.Toplevel(self.app)
        self.text_var = ttk.Entry(search_win, width=40)
        self.text_var.grid(
            row=0, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W + tk.E, ipady=3
        )
        button = ttk.Button(
            search_win,
            text=self.app.dic.get_dict("Find"),
            width=str(self.app.dic.get_dict("Find")),
            padding=(10, 5),
            command=self.search,
        )
        button.grid(row=1, column=0)
        button2 = ttk.Button(
            search_win,
            text=self.app.dic.get_dict("Asc find"),
            width=str(self.app.dic.get_dict("Asc find")),
            padding=(10, 5),
            command=self.search_forward,
        )
        button2.grid(row=1, column=1)
        # 最前面に表示し続ける
        search_win.attributes("-topmost", True)
        search_win.resizable(False, False)
        search_win.title(self.app.dic.get_dict("Find"))
        self.text_var.focus()

    def replacement_dialog(self, event=None):
        """置換ダイアログを作成.

        ・置換ダイアログを作成する。

        Args:
            event (instance): tkinter.Event のインスタンス
        """
        self.replacement_win = tk.Toplevel(self.app)
        self.text_var = ttk.Entry(self.replacement_win, width=40)
        self.text_var.grid(
            row=0, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W + tk.E, ipady=3
        )
        self.replacement_var = ttk.Entry(self.replacement_win, width=40)
        self.replacement_var.grid(
            row=1, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W + tk.E, ipady=3
        )
        button = ttk.Button(
            self.replacement_win,
            text=self.app.dic.get_dict("Find"),
            width=str(self.app.dic.get_dict("Find")),
            padding=(10, 5),
            command=self.search,
        )
        button.grid(row=2, column=0)
        button2 = ttk.Button(
            self.replacement_win,
            text=self.app.dic.get_dict("Replacement"),
            width=str(self.app.dic.get_dict("Replacement")),
            padding=(10, 5),
            command=self.replacement,
        )
        button2.grid(row=2, column=1)
        # 最前面に表示し続ける
        self.replacement_win.attributes("-topmost", True)
        self.replacement_win.resizable(False, False)
        self.replacement_win.title(self.app.dic.get_dict("Replacement"))
        self.text_var.focus()
        # ウインドウが閉じられたときの処理
        self.replacement_win.protocol(
            "WM_DELETE_WINDOW", self.replacement_dialog_on_closing
        )

    def replacement_dialog_on_closing(self):
        """検索ウインドウが閉じられたときの処理.

        ・検索ダイアログが閉じられたことがわかるようにする。
        """
        self.replacement_check_input(False)
        self.replacement_win.destroy()

    def search(self, event=None):
        """検索処理.

        ・検索処理をする。空欄なら処理しない、違うなら最初から、
        同じなら次のを検索する。

        Args:
            event (instance): tkinter.Event のインスタンス
        """
        # 現在選択中の部分を解除
        self.app.NovelEditor.tag_remove("sel", "1.0", "end")

        # 現在検索ボックスに入力されてる文字
        now_text = self.text_var.get()
        if not now_text:
            # 空欄だったら処理しない
            pass
        elif now_text != self.find_text:
            # 前回の入力と違う文字なら、検索を最初から行う
            index = "0.0"
            self.search_next(now_text, index, 0)
        else:
            # 前回の入力と同じなら、検索の続きを行う
            self.search_next(now_text, self.next_pos, 1)

        # 今回の入力を、「前回入力文字」にする
        self.find_text_input(now_text)

    def replacement(self, event=None):
        """置換処理.

        ・置換処理をする。空欄なら処理しない、違うなら初めから、
        同じなら次を検索する。

        Args:
            event (instance): tkinter.Event のインスタンス
        """
        # 現在選択中の部分を解除
        self.app.NovelEditor.tag_remove("sel", "1.0", "end")

        # 現在検索ボックスに入力されてる文字
        now_text = self.text_var.get()
        replacement_text = self.replacement_var.get()
        if not now_text or not replacement_text:
            # 空欄だったら処理しない
            pass
        elif now_text != self.find_text:
            # 前回の入力と違う文字なら、検索を最初から行う
            self.replacement_check_input(True)
            index = "0.0"
            self.search_next(now_text, index, 0)
        else:
            # 前回の入力と同じなら、検索の続きを行う
            self.replacement_check_input(True)
            # 検索文字の置換を行なう
            start = self.next_pos
            end = "{0} + {1}c".format(self.next_pos, len(now_text))
            self.app.NovelEditor.delete(start, end)
            self.app.NovelEditor.insert(start, replacement_text)
            self.search_next(now_text, self.next_pos, 1)

        # 今回の入力を、「前回入力文字」にする
        self.find_text_input(now_text)

    def search_forward(self, event=None):
        """昇順検索処理.

        ・昇順検索をする。空欄なら処理しない、違うなら初めから、
        同じなら次を検索する。

        Args:
            event (instance): tkinter.Event のインスタンス
        """
        # 現在選択中の部分を解除
        self.app.NovelEditor.tag_remove("sel", "1.0", "end")

        # 現在検索ボックスに入力されてる文字
        text = self.text_var.get()
        if not text:
            # 空欄だったら処理しない
            pass
        elif text != self.find_text:
            # 前回の入力と違う文字なら、検索を最初から行う
            index = "end"
            self.search_next(text, index, 2)
        else:
            # 前回の入力と同じなら、検索の続きを行う
            self.search_next(text, self.next_pos, 2)

        # 今回の入力を、「前回入力文字」にする
        self.find_text_input(text)

    def search_next(self, search, index, case):
        """検索のメイン処理.

        ・検索できれば選択をする。できなければ、ダイアログを出して終了。

        Args:
            search (str): 検索文字列
            index (str): 検索位置 ex. (1.0)
            case (int): 0.初めから検索 1.次に検索 2.昇順検索
        """
        if case == 2:
            backwards = True
            stopindex = "0.0"
            index = "{0}".format(index)
        elif case == 0:
            backwards = False
            stopindex = "end"
            index = "{0}".format(index)
        else:
            backwards = False
            stopindex = "end"
            index = "{0} + 1c".format(index)

        pos = self.app.NovelEditor.search(
            search, index, stopindex=stopindex, backwards=backwards
        )
        if not pos:
            if case == 2:
                index = "end"
            else:
                index = "0.0"

            pos = self.app.NovelEditor.search(
                search, index, stopindex=stopindex, backwards=backwards
            )
            if not pos:
                messagebox.showinfo(
                    self.app.dic.get_dict("Find"),
                    self.app.dic.get_dict(
                        "I searched to the end," " but there were no search characters."
                    ),
                )
                self.replacement_check_input(False)
                return

        self.next_pos_input(pos)
        start = pos
        end = "{0} + {1}c".format(pos, len(search))
        self.app.NovelEditor.tag_add("sel", start, end)
        self.app.NovelEditor.mark_set("insert", start)
        self.app.NovelEditor.see("insert")
        self.app.NovelEditor.focus()

    @classmethod
    def replacement_check_input(cls, replacement_check):
        """検索ダイアログが表示されているかを入力.

        ・検索ダイアログが表示されているかを入力する。

        Args:
            replacement_check (bool): 検索ダイアログが表示されているTrue
        """
        cls.replacement_check = replacement_check

    @classmethod
    def find_text_input(cls, find_text):
        """検索文字を入力.

        ・検索文字をクラス変数に入力する。

        Args:
            find_text (str): 検索文字
        """
        cls.find_text = find_text

    @classmethod
    def next_pos_input(cls, next_pos):
        """検索位置を入力.

        ・検索位置をクラス変数に入力する。

        Args:
            next_pos (str): 検索位置
        """
        cls.next_pos = next_pos
