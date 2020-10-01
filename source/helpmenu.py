import os
import webbrowser
import tkinter as tk


class HelpMenuClass():
    """ヘルプメニューバーのクラス

    ・ヘルプメニューバーにあるプログラム群

    """
    def __init__(self, app, image_data):
        """
        Args:
            app (instance): lineframeインスタンス
            image_data (str): イメージファイル

        """
        # バージョン情報
        self.VERSION = 'Ver 0.6.0 Beta'
        self.APP = app
        self.IMAGE_DATA = image_data

    def version(self):
        """バージョン情報を表示

        ・バージョン情報表示ダイアログを表示する。
        ×を押すまで消えないようにする。

        """
        img2 = tk.PhotoImage(data=self.IMAGE_DATA)
        window = tk.Toplevel(self.APP)
        canvas = tk.Canvas(window, width=600, height=300)
        canvas.create_image(0, 0, anchor='nw', image=img2)
        canvas.create_text(
            550,
            290,
            anchor='se',
            text='Copyright (C) 2019-2020 Yamahara Yoshihiro',
            font=('', 12)
        )
        canvas.create_text(
            420,
            120,
            anchor='nw',
            text=self.VERSION,
            font=('', 12)
        )
        canvas.pack()
        window.resizable(width=0, height=0)
        window.mainloop()

    def help(self):
        """helpページを開く

        ・ウエブブラウザを使ってREADME.htmlを表示する。

        """
        webbrowser.open(
            'file://' + os.path.dirname(
                os.path.abspath(os.path.dirname(__file__))
            )
            + "/README.html"
        )
