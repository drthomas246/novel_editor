#!/usr/bin/env python3
import os
import shutil
import tkinter as tk

from . import cw
from . import ep
from . import sp
from . import hp
from . import fp
from . import cp
from . import fm
from . import em
from . import hm
from . import pm
from . import lm
from . import main


class MainProcessingClass(main.MainClass):
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
        self.cwc = cw.CreateWindowClass(
            self,
            locale_var,
            master
        )
        self.epc = ep.EventProcessingClass(
            self,
            locale_var,
            master
        )
        self.spc = sp.SubfunctionProcessingClass(
            self,
            locale_var,
            master
        )
        self.hpc = hp.HighlightProcessingClass(
            self,
            tokenizer,
            locale_var,
            master
        )
        self.fpc = fp.FindProcessingClass(
            self,
            locale_var,
            master
        )
        self.cpc = cp.ComplementProcessingClass(
            self,
            tokenizer,
            locale_var,
            master
        )
        self.fmc = fm.FileMenuClass(
            self,
            locale_var,
            master
        )
        self.emc = em.EditMenuClass(
            self,
            locale_var,
            master
        )
        self.pmc = pm.ProcessingMenuClass(
            self,
            tokenizer,
            wiki_wiki,
            locale_var,
            master
        )
        self.lmc = lm.ListMenuClass(
            self,
            locale_var,
            master
        )
        self.hmc = hm.HelpMenuClass(
            self,
            locale_var,
            master
        )
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
        fm.FileMenuClass.now_path = ""
        # 現在開いているファイル
        fm.FileMenuClass.file_path = ""
        # 検索文字列
        fp.FindProcessingClass.find_text = ""
        # 現在入力中の初期テキスト
        lm.ListMenuClass.text_text = ""
        lm.ListMenuClass.select_list_item = ""
        # 文字の大きさ
        pm.ProcessingMenuClass.font_size = 16
        pm.ProcessingMenuClass.yahoo_appid = ""
        if os.path.isfile("./appid.txt"):
            with open("./appid.txt", encoding='utf-8') as f:
                pm.ProcessingMenuClass.yahoo_appid = f.read()

        if u"ここを消して、" in pm.ProcessingMenuClass.yahoo_appid:
            pm.ProcessingMenuClass.yahoo_appid = ""

        # dataフォルダがあるときは、削除する
        if os.path.isdir('./data'):
            shutil.rmtree('./data')
        # 新しくdataフォルダを作成する
        for val in self.TREE_FOLDER:
            os.makedirs('./{0}'.format(val[0]))
