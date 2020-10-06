#!/usr/bin/env python3
import os
import zipfile
import shutil
import tkinter as tk
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog

from . import lm


class FileMenuClass():
    """ファイルメニューバーのクラス.

    ・ファイルメニューバーにあるプログラム群

    Args:
        app (instance): MainProcessingClass のインスタンス
        master (instance): toplevel のインスタンス
        tree_folder (list): ツリーフォルダの配列
    """
    now_path = ""
    """今の処理ししているファイルのパス."""
    file_path = ""
    """現在開いているファイル."""

    def __init__(self, app, master, tree_folder):
        self.APP = app
        self.MASTER = master
        self.TREE_FOLDER = tree_folder

    def new_open(self, event=None):
        """新規作成.

        ・変更があれば、ファイル保存するか尋ねて、新規作成する。

        Args:
            event (instance): tkinter.Event のインスタンス
        """
        if not self.APP.text.get('1.0', 'end - 1c') == lm.ListMenuClass.text_text:
            if messagebox.askokcancel(
                u"小説エディタ",
                u"上書き保存しますか？"
            ):
                self.overwrite_save_file()
                self.new_file()

            elif messagebox.askokcancel(u"小説エディタ", u"今の編集を破棄して新規作成しますか？"):
                self.new_file()
        else:
            self.new_file()

    def open_file(self, event=None):
        """ファイルを開く処理.

        ・ファイルを開くダイアログを作成しファイルを開く。

        Args:
            event (instance): tkinter.Event のインスタンス
        """
        # ファイルを開くダイアログを開く
        fTyp = [(u'小説エディタ', '*.ned')]
        iDir = os.path.abspath(os.path.dirname(__file__))
        filepath = filedialog.askopenfilename(
            filetypes=fTyp,
            initialdir=iDir
        )
        # ファイル名があるとき
        if not filepath == "":
            # 初期化する
            self.APP.initialize()
            # ファイルを開いてdataフォルダに入れる
            with zipfile.ZipFile(filepath) as existing_zip:
                existing_zip.extractall('./data')
            # ツリービューを削除する
            for val in self.TREE_FOLDER:
                self.APP.tree.delete(val[0])

            # ツリービューを表示する
            self.tree_get_loop()
            # ファイルパスを拡張子抜きで表示する
            filepath, ___ = os.path.splitext(filepath)
            FileMenuClass.file_path = filepath
            FileMenuClass.now_path = ""
            # テキストビューを新にする
            self.APP.cwc.frame()

    def overwrite_save_file(self, event=None):
        """上書き保存処理.

        ・上書き保存するための処理。ファイルがあれば保存して、
        なければ保存ダイアログを出す。

        Args:
            event (instance): tkinter.Event のインスタンス
        """
        # ファイルパスが存在するとき
        if not FileMenuClass.file_path == "":
            # 編集中のファイルを保存する
            self.open_file_save(FileMenuClass.now_path)
            # zipファイルにまとめる
            shutil.make_archive(FileMenuClass.file_path, "zip", "./data")
            # 拡張子の変更を行う
            shutil.move(
                "{0}.zip".format(FileMenuClass.file_path),
                "{0}.ned".format(FileMenuClass.file_path)
            )
        # ファイルパスが存在しないとき
        else:
            # 保存ダイアログを開く
            self.save_file()

    def save_file(self, event=None):
        """ファイルを保存処理.

        ・ファイルを保存する。ファイル保存ダイアログを作成し保存をおこなう。

        Args:
            event (instance): tkinter.Event のインスタンス
        """
        # ファイル保存ダイアログを表示する
        fTyp = [(u"小説エディタ", ".ned")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        filepath = filedialog.asksaveasfilename(
            filetypes=fTyp,
            initialdir=iDir
        )
        # ファイルパスが決まったとき
        if not filepath == "":
            # 拡張子を除いて保存する
            FileMenuClass.file_path, ___ = os.path.splitext(filepath)
            # 上書き保存処理
            self.overwrite_save_file()

    def on_closing(self):
        """終了時の処理.

        ・ソフトを閉じるか確認してから閉じる。
        """
        if messagebox.askokcancel(u"小説エディタ", u"終了してもいいですか？"):
            shutil.rmtree("./data")
            if os.path.isfile("./userdic.csv"):
                os.remove("./userdic.csv")

            self.MASTER.destroy()

    def new_file(self):
        """新規作成をするための準備.

        ・ファイルの新規作成をするための準備処理をおこなう。
        """
        self.APP.initialize()
        for val in self.TREE_FOLDER:
            self.APP.tree.delete(val[0])

        # ツリービューを表示する
        self.tree_get_loop()
        self.APP.cwc.frame()
        self.APP.winfo_toplevel().title(u"小説エディタ")
        # テキストを読み取り専用にする
        self.APP.text.configure(state='disabled')
        # テキストにフォーカスを当てる
        self.APP.text.focus()

    def open_file_save(self, path):
        """開いてるファイルを保存.

        ・開いてるファイルをそれぞれの保存形式で保存する。

        Args:
            path (str): 保存ファイルのパス
        """
        # 編集ファイルを保存する
        if not path == "":
            f = open(path, 'w', encoding='utf-8')
            if not path.find(self.TREE_FOLDER[0][0]) == -1:
                f.write(self.save_charactor_file())
                self.charactor_file = ""
            elif not path.find(self.TREE_FOLDER[4][0]) == -1:
                f.write(str(self.APP.spc.zoom))
            else:
                f.write(self.APP.text.get("1.0", tk.END+'-1c'))

            f.close()
            FileMenuClass.now_path = path

    def save_charactor_file(self):
        """キャラクターファイルの保存準備.

        ・それぞれの項目をxml形式で保存する。
        """
        return '<?xml version="1.0"?>\n<data>\n\t<call>{0}</call>\
        \n\t<name>{1}</name>\n\t<sex>{2}</sex>\n\t<birthday>{3}</birthday>\
        \n\t<body>{4}</body>\n</data>'.format(
            self.APP.txt_yobi_name.get(),
            self.APP.txt_name.get(),
            self.APP.var.get(),
            self.APP.txt_birthday.get(),
            self.APP.text_body.get(
                '1.0',
                'end -1c'
            )
        )

    def tree_get_loop(self):
        """ツリービューに挿入.

        ・保存データからファイルを取得してツリービューに挿入する。
        """
        for val in self.TREE_FOLDER:
            self.APP.tree.insert('', 'end', val[0], text=val[1])
            # フォルダのファイルを取得
            path = "./{0}".format(val[0])
            files = os.listdir(path)
            for filename in files:
                if os.path.splitext(filename)[1] == ".txt":
                    self.APP.tree.insert(
                        val[0],
                        'end',
                        text=os.path.splitext(filename)[0]
                    )
