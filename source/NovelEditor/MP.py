#!/usr/bin/env python3
import os
import shutil
import platform
import tkinter as tk
import tkinter.ttk as ttk


class MainProcessingClass(ttk.Frame):
    """メインフレーム処理のクラス.

    ・初期設定をするプログラム群

    Args:
        tree_folder (list): ツリーフォルダの配列
        tokenizer (instance): Tokenizer のインスタンス
        wiki_wiki (instance): wikipediaapi.Wikipedia のインスタンス
        title_binary (str): タイトルイメージファイルバイナリ
        master (instance): toplevel のインスタンス
        class_instance (dict): 自作クラスのインスタント群
        version (str): バージョン情報
    """

    def __init__(
        self,
        tree_folder,
        tokenizer,
        wiki_wiki,
        title_binary,
        class_instance,
        version,
        master=None
    ):
        super().__init__(master)
        self.TREE_FOLDER = tree_folder
        # 自作クラスの読み込み
        self.cwc = class_instance['cw'].CreateWindowClass(self)
        self.epc = class_instance['ep'].EventProcessingClass(self)
        self.sfc = class_instance['sp'].SubfunctionProcessingClass(self, self.TREE_FOLDER)
        self.hpc = class_instance['hp'].HighlightProcessingClass(self, tokenizer)
        self.fpc = class_instance['fp'].FindProcessingClass(self)
        self.cpc = class_instance['cp'].ComplementProcessingClass(self, tokenizer)
        self.fmc = class_instance['fm'].FileMenuClass(self, master, self.TREE_FOLDER)
        self.emc = class_instance['em'].EditMenuClass(self)
        self.pmc = class_instance['pm'].ProcessingMenuClass(self, wiki_wiki, tokenizer)
        self.lmc = class_instance['lm'].ListMenuClass(self, master, self.TREE_FOLDER)
        self.hmc = class_instance['hm'].HelpMenuClass(self, title_binary, version)
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
        self.pmc.APPID = ""
        if os.path.isfile("./appid.txt"):
            f = open("./appid.txt", "r", encoding="utf-8")
            self.pmc.APPID = f.read()
            f.close()
        if u"ここを消して、" in self.pmc.APPID:
            self.pmc.APPID = ""
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
