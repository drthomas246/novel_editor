#!/usr/bin/env python3
import os
import shutil
import platform
import tkinter as tk
import tkinter.ttk as ttk

import CW
import EP
import SP
import HP
import FP
import CP
import FM
import EM
import HM
import PM
import LM


class MainProcessingClass(ttk.Frame):
    """メインフレーム処理のクラス.

    ・初期設定をするプログラム群

    Args:
        tree_folder (str): ツリーフォルダの配列
        tokenizer (instance): Tokenizerインスタンス
        wiki_wiki (instance): wikipediaapi.Wikipediaインスタンス
        title_binary (str): タイトルイメージファイルバイナリ
        master (instance): toplevelインスタンス

    """

    def __init__(
        self,
        tree_folder,
        tokenizer,
        wiki_wiki,
        title_binary,
        master=None
    ):
        super().__init__(master)
        self.TREE_FOLDER = tree_folder
        # 自作クラスの読み込み
        self.cwc = CW.CreateWindowClass(self)
        self.epc = EP.EventProcessingClass(self)
        self.sfc = SP.SubfunctionProcessingClass(self, self.TREE_FOLDER)
        self.hpc = HP.HighlightProcessingClass(self, tokenizer)
        self.fpc = FP.FindProcessingClass(self)
        self.cpc = CP.ComplementProcessingClass(self, tokenizer)
        self.fmc = FM.FileMenuClass(self, master, self.TREE_FOLDER)
        self.emc = EM.EditMenuClass(self)
        self.pmc = PM.ProcessingMenuClass(self, wiki_wiki, tokenizer)
        self.lmc = LM.ListMenuClass(self, master, self.TREE_FOLDER)
        self.hmc = HM.HelpMenuClass(self, title_binary)
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
        self.fmc.now_path = ""
        # 現在開いているファイル
        self.fmc.file_path = ""
        # 検索文字列
        self.fpc.find_text = ""
        # 現在入力中の初期テキスト
        self.lmc.text_text = ""
        self.lmc.select_list_item = ""
        # 文字の大きさ
        self.pmc.font_size = 16
        self.APPID = ""
        if os.path.isfile("./appid.txt"):
            f = open("./appid.txt", "r", encoding="utf-8")
            self.APPID = f.read()
            f.close()
        if u"ここを消して、" in self.APPID:
            self.APPID = ""
        # フォントをOSごとに変える
        pf = platform.system()
        if pf == 'Windows':
            self.font = "メイリオ"
        elif pf == 'Darwin':  # MacOS
            self.font = "Osaka-等幅"
        elif pf == 'Linux':
            self.font = "IPAゴシック"
        # dataフォルダがあるときは、削除する
        if os.path.isdir('./data'):
            shutil.rmtree('./data')
        # 新しくdataフォルダを作成する
        for val in self.TREE_FOLDER:
            os.makedirs('./{0}'.format(val[0]))
