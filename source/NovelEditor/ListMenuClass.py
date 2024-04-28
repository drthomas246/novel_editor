#!/usr/bin/env python3
import os
import shutil
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import xml.etree.ElementTree as ET

from PIL import Image, ImageTk

from . import FileMenu
from . import Definition


class ListMenuClass(Definition.DefinitionClass):
    """リストメニューバーのクラス.

    ・リストメニューバーにあるプログラム群

    Args:
        app (instance): MainProcessingClass のインスタンス
        locale_var (str): ロケーション
        master (instance): toplevel のインスタンス
    """

    text_text = ""
    """現在入力中の初期テキスト."""
    select_list_item = ""
    """選択中のリストボックスアイテム名."""

    def __init__(self, app, locale_var, master=None):
        super().__init__(locale_var, master)
        self.app = app
        self.master = master

    def message_window(self, event=None):
        """ツリービューを右クリックしたときの処理.

        ・子アイテムならば削除ダイアログを表示する。
        親アイテムならば追加を行う。

        Args:
            event (instance): tkinter.Event のインスタンス
        """
        # 選択アイテムの認識番号取得
        curItem = self.app.tree.focus()
        # 親アイテムの認識番号取得
        parentItem = self.app.tree.parent(curItem)
        # 親アイテムをクリックしたとき
        if self.app.tree.item(curItem)["text"] == self.TREE_FOLDER[4][1]:
            # イメージアイテムの親アイテムを選択したとき
            self.check_image_true()
        else:
            if (str(self.app.tree.item(curItem)["text"])) and (
                not str(self.app.tree.item(parentItem)["text"])
            ):
                # イメージアイテム以外の親アイテムを選択したとき
                self.check_image_false(curItem)
            else:
                # 子アイテムを右クリックしたとき
                self.click_child_item(curItem, parentItem)

    def on_name_click(self, event=None):
        """名前の変更.

        ・リストボックスの名前を変更する。

        Args:
            event (instance): tkinter.Event のインスタンス
        """
        # 開いているファイルを保存
        self.app.fmc.open_file_save(FileMenu.FileMenuClass.now_path)
        # 選択アイテムの認識番号取得
        curItem = self.app.tree.focus()
        # 親アイテムの認識番号取得
        parentItem = self.app.tree.parent(curItem)
        text = self.app.tree.item(parentItem)["text"]
        if not text == "":
            old_file = self.app.tree.item(curItem)["text"]
            title = self.app.dic.get_dict("Rename {0}").format(old_file)
            dialog2 = MyDialogClass(
                self.app, self.app.dic.get_dict("Change"), True, title, old_file
            )
            self.master.wait_window(dialog2.sub_name_win)
            # テキストを読み取り専用を解除する
            self.app.NovelEditor.configure(state="normal")
            new_file = dialog2.txt
            del dialog2
            for val in self.TREE_FOLDER:
                if text == val[1]:
                    path1 = "./{0}/{1}.txt".format(val[0], old_file)
                    path2 = "./{0}/{1}.txt".format(val[0], new_file)
                    FileMenu.FileMenuClass.now_path = path2
                    # テキストの名前を変更する
                    os.rename(path1, path2)
                    self.app.tree.delete(curItem)
                    Item = self.app.tree.insert(parentItem, "end", text=new_file)
                    if val == self.TREE_FOLDER[0]:
                        self.character_rename(
                            FileMenu.FileMenuClass.now_path, val[0], old_file, new_file
                        )

                    if val == self.TREE_FOLDER[4]:
                        self.rename_gif(val[0], old_file, new_file)

                    self.app.tree.selection_set(Item)
                    self.path_read_text(val[0], new_file)
                    return

    def character_rename(self, now_path, folder, old_file, new_file):
        """キャラクターの名前変更.

        ・キャラクターの名前を変更する。

        Args:
            now_path (str): 今の処理ししているファイルのパス
            folder (str): 今処理しているフォルダ
            old_file (str): 変更前のファイル名
            new_file (str): 変更後のファイル名
        """
        self.rename_gif(folder, old_file, new_file)
        with open(now_path, mode="w", encoding="utf-8") as f:
            f.write(self.app.fmc.save_charactor_file(new_file))

    @staticmethod
    def rename_gif(folder, old_file, new_file):
        """gifの名前変更.

        ・gifの名前を変更する。

        Args:
            folder (str): 今処理しているフォルダ
            old_file (str): 変更前のファイル名
            new_file (str): 変更後のファイル名
        """
        path1 = "./{0}/{1}.gif".format(folder, old_file)
        path2 = "./{0}/{1}.gif".format(folder, new_file)
        if os.path.isfile(path1):
            os.rename(path1, path2)

    def path_read_image(self, image_path, image_name, scale):
        """イメージを読み込んで表示.

        ・パスが存在すればイメージファイルを読み込んで表示する。

        Args:
            image_path (str): イメージファイルの相対パス
            image_name (str): イメージファイルの名前
            scale (int): 拡大率(%)
        """
        if not FileMenu.FileMenuClass.now_path == "":
            title = "{0}/{1}.gif".format(image_path, image_name)
            giffile = Image.open(title)
            if scale > 0:
                giffile = giffile.resize(
                    (
                        int(giffile.width / 100 * scale),
                        int(giffile.height / 100 * scale),
                    ),
                    resample=Image.LANCZOS,
                )

            self.app.CanvasImage.photo = ImageTk.PhotoImage(giffile)
            self.app.CanvasImage.itemconfig(
                self.app.ImageOnImage, image=self.app.CanvasImage.photo
            )
            # イメージサイズにキャンバスサイズを合わす
            self.app.CanvasImage.config(
                scrollregion=(0, 0, giffile.size[0], giffile.size[1])
            )
            giffile.close()

        self.app.winfo_toplevel().title(
            "{0}/{1}/{2}".format(
                self.app.dic.get_dict("Novel Editor"),
                self.TREE_FOLDER[4][1],
                image_name,
            )
        )

    def path_read_text(self, text_path, text_name):
        """テキストを読み込んで表示.

        ・パスが存在すればテキストを読み込んで表示する。

        Args:
            text_path (str): テキストファイルの相対パス
            text_name (str): テキストファイルの名前
        """
        if not FileMenu.FileMenuClass.now_path == "":
            if not FileMenu.FileMenuClass.now_path.find(self.TREE_FOLDER[0][0]) == -1:
                self.app.EntryCallName.configure(state="normal")
                self.app.EntryCallName.delete("0", tk.END)
                self.app.EntryName.delete("0", tk.END)
                self.app.EntryBirthday.delete("0", tk.END)
                self.app.TextboxBiography.delete("1.0", tk.END)
                tree = ET.parse(FileMenu.FileMenuClass.now_path)
                elem = tree.getroot()
                self.app.EntryCallName.insert(tk.END, elem.findtext("call"))
                self.app.EntryCallName.configure(state="readonly")
                self.app.EntryName.insert(tk.END, elem.findtext("name"))
                self.app.var.set(elem.findtext("sex"))
                self.app.EntryBirthday.insert(tk.END, elem.findtext("birthday"))
                self.app.TextboxBiography.insert(tk.END, elem.findtext("body"))
                title = "{0}/{1}.gif".format(
                    self.TREE_FOLDER[0][0], elem.findtext("call")
                )
                if os.path.isfile(title):
                    self.app.spc.print_gif(title)
            else:
                self.app.NovelEditor.delete("1.0", tk.END)
                with open(FileMenu.FileMenuClass.now_path, encoding="utf-8") as f:
                    self.text_text_input(f.read())
                    self.app.NovelEditor.insert(tk.END, self.text_text)

            self.app.winfo_toplevel().title(
                "{0}/{1}/{2}".format(
                    self.app.dic.get_dict("Novel Editor"), text_path, text_name
                )
            )
            # シンタックスハイライトをする
            self.app.hpc.all_highlight()

    def on_double_click(self, event=None):
        """ツリービューをダブルクリック.

        ・ファイルを保存して閉じて、選択されたアイテムを表示する。

        Args:
            event (instance): tkinter.Event のインスタンス
        """
        # 選択アイテムの認識番号取得
        curItem = self.app.tree.focus()
        # 親アイテムの認識番号取得
        parentItem = self.app.tree.parent(curItem)
        text = self.app.tree.item(parentItem)["text"]
        # 開いているファイルを保存
        self.app.fmc.open_file_save(FileMenu.FileMenuClass.now_path)
        # テキストを読み取り専用を解除する
        self.app.cwc.frame()
        self.app.NovelEditor.configure(state="disabled")
        # 条件によって分離
        self.select_list_item_input(self.app.tree.item(curItem)["text"])
        path = ""
        for val in self.TREE_FOLDER:
            if text == val[1]:
                if val[0] == self.TREE_FOLDER[4][0]:
                    path = "./{0}/{1}.txt".format(val[0], self.select_list_item)
                    with open(path, encoding="utf-8") as f:
                        zoom = f.read()

                    self.app.spc.zoom = int(zoom)
                    FileMenu.FileMenuClass.now_path = path
                    self.app.cwc.frame_image()
                    self.path_read_image(
                        self.TREE_FOLDER[4][0], self.select_list_item, self.app.spc.zoom
                    )
                else:
                    path = "./{0}/{1}.txt".format(val[0], self.select_list_item)
                    FileMenu.FileMenuClass.now_path = path
                    if val[0] == self.TREE_FOLDER[0][0]:
                        self.app.cwc.frame_character()
                    else:
                        # テキストを読み取り専用を解除する
                        self.app.NovelEditor.configure(state="normal")
                        self.app.NovelEditor.focus()

                    self.path_read_text(text, self.select_list_item)

                return

        FileMenu.FileMenuClass.now_path = ""
        self.app.winfo_toplevel().title(self.app.dic.get_dict("Novel Editor"))

    def check_image_true(self):
        """イメージアイテムを右クリックしたとき.

        ・イメージアイテムの親アイテムを右クリックしたときの処理。
        """
        # イメージアイテムを選択したとき
        fTyp = [(self.app.dic.get_dict("Novel Editor"), "*.gif")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        filepath = filedialog.askopenfilename(filetypes=fTyp, initialdir=iDir)
        # ファイル名があるとき
        if not filepath == "":
            file_name = os.path.splitext(os.path.basename(filepath))[0]
            path = "./{0}/{1}.gif".format(self.TREE_FOLDER[4][0], file_name)
            shutil.copy2(filepath, path)
            self.app.cwc.frame_image()
            path = "./{0}/{1}.txt".format(self.TREE_FOLDER[4][0], file_name)
            tree = self.app.tree.insert(self.TREE_FOLDER[4][0], "end", text=file_name)
            self.app.tree.see(tree)
            self.app.tree.selection_set(tree)
            self.app.tree.focus(tree)
            self.select_list_item_input(file_name)
            FileMenu.FileMenuClass.now_path = path
            with open(path, mode="w", encoding="utf-8") as f:
                self.app.spc.zoom = 100
                f.write(str(self.app.spc.zoom))

            self.app.cwc.frame_image()
            self.path_read_image(self.TREE_FOLDER[4][0], file_name, 0)

    def check_image_false(self, curItem):
        """イメージアイテム以外を右クリックしたとき.

        ・イメージアイテム以外の親アイテムを右クリックしたときの処理。

        Args:
            curItem (int): 選択アイテムの認識番号
        """
        # サブダイヤログを表示する
        title = self.app.dic.get_dict("Insert in {0}").format(
            self.app.tree.item(curItem)["text"]
        )
        dialog = MyDialogClass(
            self.app, self.app.dic.get_dict("Insert"), True, title, False
        )
        self.master.wait_window(dialog.sub_name_win)
        file_name = dialog.txt
        del dialog
        if not file_name == "":
            self.app.fmc.open_file_save(FileMenu.FileMenuClass.now_path)
            curItem = self.app.tree.focus()
            text = self.app.tree.item(curItem)["text"]
            path = ""
            tree = ""
            # 選択されているフォルダを見つける
            for val in self.TREE_FOLDER:
                if text == val[1]:
                    if val[0] == self.TREE_FOLDER[0][0]:
                        self.app.cwc.frame_character()
                        self.app.EntryCallName.configure(state="normal")
                        self.app.EntryCallName.insert(tk.END, file_name)
                        self.app.EntryCallName.configure(state="readonly")
                    else:
                        self.app.cwc.frame()

                    path = "./{0}/{1}.txt".format(val[0], file_name)
                    tree = self.app.tree.insert(val[0], "end", text=file_name)
                    FileMenu.FileMenuClass.now_path = path
                    break

            # パスが存在すれば新規作成する
            if not path == "":
                with open(path, mode="w", encoding="utf-8") as f:
                    f.write("")

                # ツリービューを選択状態にする
                self.app.tree.see(tree)
                self.app.tree.selection_set(tree)
                self.app.tree.focus(tree)
                self.select_list_item_input(file_name)
                self.app.winfo_toplevel().title(
                    "{0}/{1}/{2}".format(
                        self.app.dic.get_dict("Novel Editor"), text, file_name
                    )
                )
                self.app.NovelEditor.focus()
                # テキストを読み取り専用を解除する
                self.app.NovelEditor.configure(state="normal")
                self.app.hpc.create_tags()

    def click_child_item(self, curItem, parentItem):
        """子アイテムを右クリックしたとき.

        ・子アイテムを右クリックしたときの処理。

        Args:
            curItem (int): 選択アイテムの認識番号
            parentItem (int): 親アイテムの認識番号
        """
        if str(self.app.tree.item(curItem)["text"]):
            # 項目を削除する
            file_name = self.app.tree.item(curItem)["text"]
            text = self.app.tree.item(parentItem)["text"]
            # ＯＫ、キャンセルダイアログを表示し、ＯＫを押したとき
            if messagebox.askokcancel(
                self.app.dic.get_dict("Delete item"),
                self.app.dic.get_dict("Delete {0} item?").format(file_name),
            ):
                image_path = ""
                path = ""
                # パスを取得する
                for val in self.TREE_FOLDER:
                    if text == val[1]:
                        path = "./{0}/{1}.txt".format(val[0], file_name)
                        image_path = "./{0}/{1}.gif".format(val[0], file_name)
                        self.app.tree.delete(curItem)
                        FileMenu.FileMenuClass.now_path = ""
                        break
                # imageパスが存在したとき
                if os.path.isfile(image_path):
                    os.remove(image_path)

                # パスが存在したとき
                if not path == "":
                    os.remove(path)
                    self.app.cwc.frame()
                    self.app.NovelEditor.focus()

    @classmethod
    def text_text_input(cls, text_text):
        """現在入力中の初期テキストを入力.

        ・現在入力中の初期テキストをクラス変数に入力する。

        Args:
            text_text (str): 現在入力中の初期テキスト
        """
        cls.text_text = text_text

    @classmethod
    def select_list_item_input(cls, select_list_item):
        """選択中のリストボックスアイテム名を入力.

        ・選択中のリストボックスアイテム名をクラス変数に入力する。

        Args:
            select_list_item (str): 選択中のリストボックスアイテム名
        """
        cls.select_list_item = select_list_item


class MyDialogClass:
    """ダイアログ作成クラス.

    ・自作ダイアログを呼び出し表示する。

    Args:
        app (instance): 親ウインドウインスタンス
        caption (str): ボタンのメッセージ
        cancel (bool): キャンセルボタンを表示する(True)
        title (str): タイトル
        text (bool): 選択状態にする(True)
    """

    def __init__(self, app, caption, cancel, title, text):
        self.txt = ""
        self.sub_name_win = tk.Toplevel(app)
        self.EntryName = ttk.Entry(self.sub_name_win, width=40)
        self.EntryName.grid(
            row=0, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W + tk.E, ipady=3
        )
        button = ttk.Button(
            self.sub_name_win,
            text=caption,
            width=str(caption),
            padding=(10, 5),
            command=self.sub_name_ok,
        )
        button.grid(row=1, column=0)
        if cancel:
            button2 = ttk.Button(
                self.sub_name_win,
                text=app.dic.get_dict("Cancel"),
                width=str(app.dic.get_dict("Cancel")),
                padding=(10, 5),
                command=self.sub_name_win.destroy,
            )

            button2.grid(row=1, column=1)
            self.EntryName.focus()
            if text is not False:
                self.EntryName.insert(tk.END, text)
                self.EntryName.select_range(0, "end")

        self.sub_name_win.title(title)
        self.sub_name_win.attributes("-topmost", True)
        self.sub_name_win.resizable(False, False)
        self.EntryName.focus()

    def sub_name_ok(self, event=None):
        """ダイアログボタンクリック時の処理.

        ・自作ダイアログのボタンをクリックしたときにインプットボックスに
        入力されている値を取得する。

        Args:
            event (instance): tkinter.Event のインスタンス

        Returns:
            str: インプットボックスの値
        """
        self.txt = self.EntryName.get()
        self.sub_name_win.destroy()
        return self.txt
