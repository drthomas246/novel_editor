#!/usr/bin/env python3
import os
import sys
import platform
import tkinter as tk
import tkinter.messagebox as messagebox

import wikipediaapi
from janome.tokenizer import Tokenizer

from . import mp as MainProcessing
from . import data
import i18n


def main_window_create(locale_var):
    """タイトルウインドウの作成.

    ・タイトルウインドウを作成する。

    Args:
        locale_var (str): ロケーション
    """
    dic = i18n.initialize(locale_var)
    root = tk.Tk()
    root.withdraw()
    if os.path.isdir("./data"):
        messagebox.showerror(
            dic.get_dict("Novel Editor"),
            dic.get_dict("This program cannot be started more than once.")
        )
        sys.exit()

    root.geometry('600x300')
    root.title(dic.get_dict("Novel Editor"))
    img = tk.PhotoImage(data=data.TITLE_BINARY)
    label = tk.Label(image=img)
    # タイトルを表示する
    label.pack()
    # センターに表示する
    root.update_idletasks()
    ww = root.winfo_screenwidth()
    lw = root.winfo_width()
    wh = root.winfo_screenheight()
    lh = root.winfo_height()
    root.geometry(
        "{0}x{1}+{2}+{3}".format(
            str(lw),
            str(lh),
            str(int(ww/2-lw/2)),
            str(int(wh/2-lh/2))
        )
    )
    root.deiconify()

    # windowsのみタイトルバーを削除
    # OS別判断
    if os.name == 'nt':
        root.overrideredirect(True)
    elif os.name == 'posix':
        root.wm_attributes('-type', 'splash')
    # 描画するが処理は止めない
    root.update()
    # Janomeを使って日本語の形態素解析を起動
    tokenizer = Tokenizer()
    # wikipediaapiを起動
    wiki_wiki = wikipediaapi.Wikipedia('Novel Editor(yoshihiro@yamahara.email)','ja')
    # メイン画面を削除
    root.destroy()
    # 再度メイン画面を作成
    root = tk.Tk()
    # アイコンを設定
    root.tk.call(
        'wm',
        'iconphoto',
        root._w,
        tk.PhotoImage(data=data.ICO_BINARY)
    )
    # タイトルの表示
    root.title(dic.get_dict("Novel Editor"))
    # フレームを表示する
    app = MainProcessing.MainProcessingClass(
        tokenizer,
        wiki_wiki,
        locale_var,
        root
    )
    app.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
    # 終了時にon_closingを行う
    root.protocol("WM_DELETE_WINDOW", app.fmc.on_closing)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    pf = platform.system()
    if pf == 'Windows':
        root.state('zoomed')
    else:
        root.attributes("-zoomed", "1")

    return root
