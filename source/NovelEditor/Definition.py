import platform
import tkinter as tk
import tkinter.ttk as ttk

import i18n
from . import data


class DefinitionClass(ttk.Frame):
    """ディフィニションクラス.

    定数を定義しておくプログラム群

    Args:
        locale_var (str): ロケーション
        master (instance): toplevel のインスタンス
    """

    def __init__(self, locale_var, master=None):
        super().__init__(master)
        self.dic = i18n.initialize(locale_var)
        self.TREE_FOLDER = [
            ["data/character", self.dic.get_dict("Character")],
            ["data/occupation", self.dic.get_dict("Occupation")],
            ["data/space", self.dic.get_dict("Space")],
            ["data/event", self.dic.get_dict("Event")],
            ["data/image", self.dic.get_dict("Image")],
            ["data/nobel", self.dic.get_dict("Novel")],
        ]
        self.TITLE_BINARY = data.TITLE_BINARY
        self.BLANK_IMAGE = data.BLANK_IMAGE
        self.VERSION = data.__version__
        # メニューバーの作成
        self.menu_bar = tk.Menu(master)
        self.master.config(menu=self.menu_bar)
        # フォントをOSごとに変える
        pf = platform.system()
        if pf == "Windows":
            self.font = "メイリオ"
        elif pf == "Darwin":  # MacOS
            self.font = "Osaka-等幅"
        elif pf == "Linux":
            self.font = "IPAゴシック"
        else:
            self.font = ""
