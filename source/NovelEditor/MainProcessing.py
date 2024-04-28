#!/usr/bin/env python3
import os
import shutil
import tkinter as tk

from . import CreateWindow
from . import EventProcessing
from . import SubfunctionProcessing
from . import HighlightProcessing
from . import FindProcessing
from . import ComplementProcessing
from . import FileMenu
from . import EditMenu
from . import HelpMenu
from . import ProcessingMenu
from . import ListMenuClass
from . import Definition


class MainProcessingClass(Definition.DefinitionClass):
    """メインフレーム処理のクラス.

    ・初期設定をするプログラム群

    Args:
        tokenizer (instance): Tokenizer のインスタンス
        wiki_wiki (instance): wikipediaapi.Wikipedia のインスタンス
        locale_var (str): ロケーション
        master (instance): toplevel のインスタンス
    """

    def __init__(self, tokenizer, wiki_wiki, locale_var, master=None):
        super().__init__(locale_var, master)
        # 自作クラスの読み込み
        self.cwc = CreateWindow.CreateWindowClass(self, locale_var, master)
        self.epc = EventProcessing.EventProcessingClass(self, locale_var, master)
        self.spc = SubfunctionProcessing.SubfunctionProcessingClass(
            self, locale_var, master
        )
        self.hpc = HighlightProcessing.HighlightProcessingClass(
            self, tokenizer, locale_var, master
        )
        self.fpc = FindProcessing.FindProcessingClass(self, locale_var, master)
        self.cpc = ComplementProcessing.ComplementProcessingClass(
            self, tokenizer, locale_var, master
        )
        self.fmc = FileMenu.FileMenuClass(self, locale_var, master)
        self.emc = EditMenu.EditMenuClass(self, locale_var, master)
        self.pmc = ProcessingMenu.ProcessingMenuClass(
            self, tokenizer, wiki_wiki, locale_var, master
        )
        self.lmc = ListMenuClass.ListMenuClass(self, locale_var, master)
        self.hmc = HelpMenu.HelpMenuClass(self, locale_var, master)
        # メニューバーの作成
        self.menu_bar = tk.Menu(master)
        self.master.config(menu=self.menu_bar)
        # 初期化処理
        self.initialize()
        self.cwc.create_widgets()
        self.epc.create_event()

    def initialize(self):
        """初期化処理.

        ・変数の初期化及び起動準備をする。
        """
        # 今の処理ししているファイルのパス
        FileMenu.FileMenuClass.now_path = ""
        # 現在開いているファイル
        FileMenu.FileMenuClass.file_path = ""
        # 検索文字列
        FindProcessing.FindProcessingClass.find_text = ""
        # 現在入力中の初期テキスト
        ListMenuClass.ListMenuClass.text_text = ""
        ListMenuClass.ListMenuClass.select_list_item = ""
        # 文字の大きさ
        ProcessingMenu.ProcessingMenuClass.font_size = 16
        ProcessingMenu.ProcessingMenuClass.yahoo_appid = ""
        if os.path.isfile("./appid.txt"):
            with open("./appid.txt", encoding="utf-8") as f:
                ProcessingMenu.ProcessingMenuClass.yahoo_appid = f.read()

        if "ここを消して、" in ProcessingMenu.ProcessingMenuClass.yahoo_appid:
            ProcessingMenu.ProcessingMenuClass.yahoo_appid = ""

        # dataフォルダがあるときは、削除する
        if os.path.isdir("./data"):
            shutil.rmtree("./data")
        # 新しくdataフォルダを作成する
        for val in self.TREE_FOLDER:
            os.makedirs("./{0}".format(val[0]))
