#!/usr/bin/env python3
import os
import shutil
import platform
import tkinter as tk
import tkinter.ttk as ttk

from . import pm
from . import fm
from . import fp
from . import lm


class MainProcessingClass(ttk.Frame):
    """メインフレーム処理のクラス.

    ・初期設定をするプログラム群

    Args:
        TREE_FOLDER (list): ツリーフォルダの配列
        tokenizer (instance): Tokenizer のインスタンス
        wiki_wiki (instance): wikipediaapi.Wikipedia のインスタンス
        TITLE_BINARY (str): タイトルイメージファイルバイナリ
        class_instance (dict): 自作クラスのインスタント群
        VERSION (str): バージョン情報
        locale (str): ロケーション
        master (instance): toplevel のインスタンス
    """

    def __init__(
        self,
        TREE_FOLDER,
        tokenizer,
        WIKI_WIKI,
        TITLE_BINARY,
        BLANK_IMAGE,
        class_instance,
        VERSION,
        dic,
        master=None
    ):
        super().__init__(master)
        self.TREE_FOLDER = TREE_FOLDER
        self.dic = dic
        # 自作クラスの読み込み
        self.cwc = class_instance['cw'].CreateWindowClass(self, BLANK_IMAGE)
        self.epc = class_instance['ep'].EventProcessingClass(self)
        self.spc = class_instance['sp'].SubfunctionProcessingClass(
            self
        )
        self.hpc = class_instance['hp'].HighlightProcessingClass(
            self,
            tokenizer
        )
        self.fpc = class_instance['fp'].FindProcessingClass(self)
        self.cpc = class_instance['cp'].ComplementProcessingClass(
            self,
            tokenizer
        )
        self.fmc = class_instance['fm'].FileMenuClass(
            self,
            master,
            self.TREE_FOLDER
        )
        self.emc = class_instance['em'].EditMenuClass(self)
        self.pmc = class_instance['pm'].ProcessingMenuClass(
            self,
            WIKI_WIKI,
            tokenizer
        )
        self.lmc = class_instance['lm'].ListMenuClass(
            self,
            master,
            self.TREE_FOLDER
        )
        self.hmc = class_instance['hm'].HelpMenuClass(
            self,
            TITLE_BINARY,
            VERSION
        )
        # メニューバーの作成
        self.menu_bar = tk.Menu(self.master)
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
        self.pmc.yahoo_appid = ""
        if os.path.isfile("./appid.txt"):
            with open("./appid.txt", encoding='utf-8') as f:
                self.pmc.yahoo_appid = f.read()

        if u"ここを消して、" in self.pmc.yahoo_appid:
            self.pmc.yahoo_appid = ""
        # フォントをOSごとに変える
        pf = platform.system()
        if pf == 'Windows':
            self.font = "メイリオ"
        elif pf == 'Darwin':  # MacOS
            self.font = "Osaka-等幅"
        elif pf == 'Linux':
            self.font = "IPAゴシック"
        else:
            self.font = ""

        # dataフォルダがあるときは、削除する
        if os.path.isdir('./data'):
            shutil.rmtree('./data')
        # 新しくdataフォルダを作成する
        for val in self.TREE_FOLDER:
            os.makedirs('./{0}'.format(val[0]))
