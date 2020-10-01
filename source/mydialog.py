import tkinter as tk
import tkinter.ttk as ttk


class Mydialog():
    """ダイアログ作成クラス

    ・自作ダイアログを呼び出し表示する。

    """

    def __init__(self, message, button1, button2, title, text):
        """
        Args:
            message (instance): 親ウインドウインスタンス
            button1 (str): ボタンのメッセージ
            button2 (bool): キャンセルボタンを表示する(True)
            title (str): タイトル
            text (bool): 選択状態にする(True)

        """
        self.txt = ""
        self.sub_name_win = tk.Toplevel(message)
        self.txt_name = ttk.Entry(self.sub_name_win, width=40)
        self.txt_name.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=5,
            pady=5,
            sticky=tk.W+tk.E,
            ipady=3
        )
        button = ttk.Button(
            self.sub_name_win,
            text=button1,
            width=str(button1),
            padding=(10, 5),
            command=self.sub_name_ok
        )
        button.grid(row=1, column=0)
        if button2:
            button = ttk.Button(
                self.sub_name_win,
                text=u'キャンセル',
                width=str(u'キャンセル'),
                padding=(10, 5),
                command=self.sub_name_win.destroy
            )

            button.grid(row=1, column=1)
            self.txt_name.focus()
            if text is not False:
                self.txt_name.insert(tk.END, text)
                self.txt_name.select_range(0, 'end')

        self.sub_name_win.title(title)
        self.txt_name.focus()

    def sub_name_ok(self, event=None):
        """ダイアログボタンクリック時の処理

        ・自作ダイアログのボタンをクリックしたときにインプットボックスに
        入力されている値を取得する。

        Args:
            event (instance): tkinter.Event のインスタンス

        Returns:
            str: インプットボックスの値

        """
        self.txt = self.txt_name.get()
        self.sub_name_win.destroy()
        return self.txt
