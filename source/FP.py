import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox


class FindProcessingClass():
    """検索置換のクラス

    ・検索置換するためのプログラム群

    Attributes:
        replacement_check (bool): 検索ダイアログが表示されているTrue
        next_pos (str): 次の検索位置 例.(1.0)
        find_text (str): 検索文字列

    """
    def __init__(self, app):
        """
        Args:
            app (instance): lineframeインスタンス

        """
        self.replacement_check = 0
        self.next_pos = ""
        self.find_text = ""
        self.APP = app

    def push_keys(self, event=None):
        """キーが押されたときの処理

        ・何かキーが押されたときに検索処理を中断する。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        # 検索処理を中断する
        self.replacement_check = 0

    def find_dialog(self, event=None):
        """検索ダイアログを作成

        ・検索ダイアログを作成する。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        search_win = tk.Toplevel(self.APP)
        self.text_var = ttk.Entry(search_win, width=40)
        self.text_var.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=5,
            pady=5,
            sticky=tk.W+tk.E,
            ipady=3
        )
        button = ttk.Button(
            search_win,
            text=u'検索',
            width=str(u'検索'),
            padding=(10, 5),
            command=self.search
        )
        button.grid(row=1, column=0)
        button2 = ttk.Button(
            search_win,
            text=u'昇順検索',
            width=str(u'昇順検索'),
            padding=(10, 5),
            command=self.search_forward
        )
        button2.grid(row=1, column=1)
        # 最前面に表示し続ける
        search_win.attributes("-topmost", True)
        search_win.title(u'検索')
        self.text_var.focus()

    def replacement_dialog(self, event=None):
        """置換ダイアログを作成

        ・置換ダイアログを作成する。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        self.replacement_win = tk.Toplevel(self.APP)
        self.text_var = ttk.Entry(self.replacement_win, width=40)
        self.text_var.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=5,
            pady=5,
            sticky=tk.W+tk.E,
            ipady=3
        )
        self.replacement_var = ttk.Entry(self.replacement_win, width=40)
        self.replacement_var.grid(
            row=1,
            column=0,
            columnspan=2,
            padx=5,
            pady=5,
            sticky=tk.W+tk.E,
            ipady=3
        )
        button = ttk.Button(
            self.replacement_win,
            text=u'検索',
            width=str(u'検索'),
            padding=(10, 5),
            command=self.search
        )
        button.grid(row=2, column=0)
        button2 = ttk.Button(
            self.replacement_win,
            text=u'置換',
            width=str(u'置換'),
            padding=(10, 5),
            command=self.replacement
        )
        button2.grid(row=2, column=1)
        # 最前面に表示し続ける
        self.replacement_win.attributes("-topmost", True)
        self.replacement_win.title(u'置換')
        self.text_var.focus()
        # ウインドウが閉じられたときの処理
        self.replacement_win.protocol(
            "WM_DELETE_WINDOW",
            self.replacement_dialog_on_closing
            )

    def replacement_dialog_on_closing(self):
        """検索ウインドウが閉じられたときの処理

        ・検索ダイアログが閉じられたことがわかるようにする。

        """
        self.replacement_check = 0
        self.replacement_win.destroy()

    def search(self, event=None):
        """検索処理

        ・検索処理をする。空欄なら処理しない、違うなら最初から、
        同じなら次のを検索する。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        # 現在選択中の部分を解除
        self.APP.text.tag_remove('sel', '1.0', 'end')

        # 現在検索ボックスに入力されてる文字
        now_text = self.text_var.get()
        if not now_text:
            # 空欄だったら処理しない
            pass
        elif now_text != self.find_text:
            # 前回の入力と違う文字なら、検索を最初から行う
            index = '0.0'
            self.search_next(now_text, index, 0)
        else:
            # 前回の入力と同じなら、検索の続きを行う
            self.search_next(now_text, self.next_pos, 1)

        # 今回の入力を、「前回入力文字」にする
        self.find_text = now_text

    def replacement(self, event=None):
        """置換処理

        ・置換処理をする。空欄なら処理しない、違うなら初めから、
        同じなら次を検索する。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        # 現在選択中の部分を解除
        self.APP.text.tag_remove('sel', '1.0', 'end')

        # 現在検索ボックスに入力されてる文字
        now_text = self.text_var.get()
        replacement_text = self.replacement_var.get()
        if not now_text or not replacement_text:
            # 空欄だったら処理しない
            pass
        elif now_text != self.find_text:
            # 前回の入力と違う文字なら、検索を最初から行う
            self.replacement_check = 1
            index = '0.0'
            self.search_next(now_text, index, 0)
        else:
            # 前回の入力と同じなら、検索の続きを行う
            self.replacement_check = 1
            # 検索文字の置換を行なう
            start = self.next_pos
            end = '{0} + {1}c'.format(self.next_pos, len(now_text))
            self.APP.text.delete(start, end)
            self.APP.text.insert(start, replacement_text)
            self.search_next(now_text, self.next_pos, 1)

        # 今回の入力を、「前回入力文字」にする
        self.find_text = now_text

    def search_forward(self, event=None):
        """昇順検索処理

        ・昇順検索をする。空欄なら処理しない、違うなら初めから、
        同じなら次を検索する。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        # 現在選択中の部分を解除
        self.APP.text.tag_remove('sel', '1.0', 'end')

        # 現在検索ボックスに入力されてる文字
        now_text = self.text_var.get()
        if not now_text:
            # 空欄だったら処理しない
            pass
        elif now_text != self.find_text:
            # 前回の入力と違う文字なら、検索を最初から行う
            index = 'end'
            self.search_next(now_text, index, 2)
        else:
            # 前回の入力と同じなら、検索の続きを行う
            self.search_next(now_text, self.next_pos, 2)

        # 今回の入力を、「前回入力文字」にする
        self.find_text = now_text

    def search_next(self, search, index, case):
        """検索のメイン処理

        ・検索できれば選択をする。できなければ、ダイアログを出して終了。

        Args:
            search (str): 検索文字列
            index (str): 検索位置 ex. (1.0)
            case (int): 0.初めから検索 1.次に検索 2.昇順検索

        """
        if case == 2:
            backwards = True
            stopindex = '0.0'
            index = '{0}'.format(index)
        elif case == 0:
            backwards = False
            stopindex = 'end'
            index = '{0}'.format(index)
        else:
            backwards = False
            stopindex = 'end'
            index = '{0} + 1c'.format(index)

        pos = self.APP.text.search(
            search, index,
            stopindex=stopindex,
            backwards=backwards
        )
        if not pos:
            if case == 2:
                index = "end"
            else:
                index = "0.0"

            pos = self.APP.text.search(
                search, index,
                stopindex=stopindex,
                backwards=backwards
            )
            if not pos:
                messagebox.showinfo(
                    "検索",
                    "最後まで検索しましたが検索文字はありませんでした。"
                )
                self.replacement_check = 0
                return

        self.next_pos = pos
        start = pos
        end = '{0} + {1}c'.format(pos, len(search))
        self.APP.text.tag_add('sel', start, end)
        self.APP.text.mark_set('insert', start)
        self.APP.text.see('insert')
        self.APP.text.focus()
