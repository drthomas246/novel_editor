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
        TREE_FOLDER (list): ツリーフォルダの配列
    """
    now_path = ""
    """今の処理ししているファイルのパス."""
    file_path = ""
    """現在開いているファイル."""

    def __init__(self, app, master, TREE_FOLDER):
        self.app = app
        self.master = master
        self.TREE_FOLDER = TREE_FOLDER

    def new_open(self, event=None):
        """新規作成.

        ・変更があれば、ファイル保存するか尋ねて、新規作成する。

        Args:
            event (instance): tkinter.Event のインスタンス
        """
        if not self.app.text.get(
                    '1.0',
                    'end - 1c'
                ) == lm.ListMenuClass.text_text:
            if messagebox.askokcancel(
                self.app.dic.get_dict("Novel Editor"),
                self.app.dic.get_dict("Do you want to overwrite?")
            ):
                self.overwrite_save_file()
                self.new_file()

            elif messagebox.askokcancel(
                    self.app.dic.get_dict("Novel Editor"),
                    self.app.dic.get_dict(
                        "Do you want to discard the current edit"
                        " and create a new one?"
                    )
            ):
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
        fTyp = [(self.app.dic.get_dict("Novel Editor"), '*.ned')]
        iDir = os.path.abspath(os.path.dirname(__file__))
        filepath = filedialog.askopenfilename(
            filetypes=fTyp,
            initialdir=iDir
        )
        # ファイル名があるとき
        if not filepath == "":
            # 初期化する
            self.app.initialize()
            # ファイルを開いてdataフォルダに入れる
            with zipfile.ZipFile(filepath) as existing_zip:
                existing_zip.extractall('./data')
            # ツリービューを削除する
            for val in self.TREE_FOLDER:
                self.app.tree.delete(val[0])

            # ツリービューを表示する
            self.tree_get_loop()
            # ファイルパスを拡張子抜きで表示する
            filepath, ___ = os.path.splitext(filepath)
            self.file_path_input(filepath)
            self.now_path_input("")
            # テキストビューを新にする
            self.app.cwc.frame()

    def overwrite_save_file(self, event=None):
        """上書き保存処理.

        ・上書き保存するための処理。ファイルがあれば保存して、
        なければ保存ダイアログを出す。

        Args:
            event (instance): tkinter.Event のインスタンス
        """
        # ファイルパスが存在するとき
        if not self.file_path == "":
            # 編集中のファイルを保存する
            self.open_file_save(self.now_path)
            # zipファイルにまとめる
            shutil.make_archive(self.file_path, "zip", "./data")
            # 拡張子の変更を行う
            shutil.move(
                "{0}.zip".format(self.file_path),
                "{0}.ned".format(self.file_path)
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
        fTyp = [(self.app.dic.get_dict("Novel Editor"), ".ned")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        filepath = filedialog.asksaveasfilename(
            filetypes=fTyp,
            initialdir=iDir
        )
        # ファイルパスが決まったとき
        if not filepath == "":
            # 拡張子を除いて保存する
            file_path, ___ = os.path.splitext(filepath)
            self.file_path_input(filepath)
            # 上書き保存処理
            self.overwrite_save_file()

    def on_closing(self):
        """終了時の処理.

        ・ソフトを閉じるか確認してから閉じる。
        """
        if messagebox.askokcancel(
                self.app.dic.get_dict("Novel Editor"),
                self.app.dic.get_dict("Can I quit?")
        ):
            shutil.rmtree("./data")
            if os.path.isfile("./userdic.csv"):
                os.remove("./userdic.csv")

            self.master.destroy()

    def new_file(self):
        """新規作成をするための準備.

        ・ファイルの新規作成をするための準備処理をおこなう。
        """
        self.app.initialize()
        for val in self.TREE_FOLDER:
            self.app.tree.delete(val[0])

        # ツリービューを表示する
        self.tree_get_loop()
        self.app.cwc.frame()
        self.app.winfo_toplevel().title(
            self.app.dic.get_dict("Novel Editor")
        )
        # テキストを読み取り専用にする
        self.app.text.configure(state='disabled')
        # テキストにフォーカスを当てる
        self.app.text.focus()

    def open_file_save(self, path):
        """開いてるファイルを保存.

        ・開いてるファイルをそれぞれの保存形式で保存する。

        Args:
            path (str): 保存ファイルのパス
        """
        # 編集ファイルを保存する
        if not path == "":
            with open(path, mode='w', encoding='utf-8') as f:
                if not path.find(self.TREE_FOLDER[0][0]) == -1:
                    f.write(
                        self.save_charactor_file(self.app.txt_yobi_name.get())
                    )
                    self.charactor_file = ""
                elif not path.find(self.TREE_FOLDER[4][0]) == -1:
                    f.write(str(self.app.spc.zoom))
                else:
                    f.write(self.app.text.get("1.0", tk.END+'-1c'))

            self.now_path_input(path)

    def save_charactor_file(self, name):
        """キャラクターファイルの保存準備.

        ・それぞれの項目をxml形式で保存する。

        Args:
            name (str): 名前
        Return:
            str: セーブメタデータ
        """
        return '<?xml version="1.0"?>\n<data>\n\t<call>{0}</call>\
        \n\t<name>{1}</name>\n\t<sex>{2}</sex>\n\t<birthday>{3}</birthday>\
        \n\t<body>{4}</body>\n</data>'.format(
            name,
            self.app.txt_name.get(),
            self.app.var.get(),
            self.app.txt_birthday.get(),
            self.app.text_body.get(
                '1.0',
                'end -1c'
            )
        )

    def tree_get_loop(self):
        """ツリービューに挿入.

        ・保存データからファイルを取得してツリービューに挿入する。
        """
        for val in self.TREE_FOLDER:
            self.app.tree.insert('', 'end', val[0], text=val[1])
            # フォルダのファイルを取得
            path = "./{0}".format(val[0])
            files = os.listdir(path)
            for filename in files:
                if os.path.splitext(filename)[1] == ".txt":
                    self.app.tree.insert(
                        val[0],
                        'end',
                        text=os.path.splitext(filename)[0]
                    )

    @classmethod
    def now_path_input(cls, now_path):
        """今の処理ししているファイルのパスを入力.

        ・今の処理ししているファイルのパスをクラス変数に入力する。

        Args:
            now_path (str): 今の処理ししているファイルのパス
        """
        cls.now_path = now_path

    @classmethod
    def file_path_input(cls, file_path):
        """現在開いているファイルを入力.

        ・現在開いているファイルをクラス変数に入力する。

        Args:
            file_path (str): 今の処理ししているファイルのパス
        """
        cls.file_path = file_path
