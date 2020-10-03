import os
import shutil
import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import xml.etree.ElementTree as ET

from PIL import Image, ImageTk

import MD


class ListMenuClass():
    """リストメニューバーのクラス

    ・リストメニューバーにあるプログラム群

    Args:
        app (instance): MainProcessingClassインスタンス
        master (instance): toplevelインスタンス
        tree_folder (str): ツリーフォルダの配列

    Attributes:
        text_text (str): 現在入力中の初期テキスト
        self.select_list_item (str): 選択中のリストボックスアイテム名

    """
    def __init__(self, app, master, tree_folder):
        self.text_text = ""
        self.select_list_item = ""
        self.APP = app
        self.MASTER = master
        self.tree_folder = tree_folder

    def message_window(self, event=None):
        """ツリービューを右クリックしたときの処理

        ・子アイテムならば削除ダイアログを表示する。
        親アイテムならば追加を行う。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        curItem = self.APP.tree.focus()              # 選択アイテムの認識番号取得
        parentItem = self.APP.tree.parent(curItem)   # 親アイテムの認識番号取得
        # 親アイテムをクリックしたとき
        if self.APP.tree.item(curItem)["text"] == self.tree_folder[4][1]:
            # imageタグを選択したとき
            fTyp = [(u'小説エディタ', '*.gif')]
            iDir = os.path.abspath(os.path.dirname(__file__))
            filepath = filedialog.askopenfilename(
                filetypes=fTyp,
                initialdir=iDir
            )
            # ファイル名があるとき
            if not filepath == "":
                file_name = os.path.splitext(os.path.basename(filepath))[0]
                path = "./{0}/{1}.gif".format(
                    self.tree_folder[4][0],
                    file_name
                )
                shutil.copy2(filepath, path)
                self.APP.cwc.frame_image()
                path = "./{0}/{1}.txt".format(
                    self.tree_folder[4][0],
                    file_name
                )
                tree = self.APP.tree.insert(
                    self.tree_folder[4][0],
                    'end',
                    text=file_name
                )
                self.APP.tree.see(tree)
                self.APP.tree.selection_set(tree)
                self.APP.tree.focus(tree)
                self.select_list_item = file_name
                self.APP.fmc.now_path = path
                f = open(path, 'w', encoding='utf-8')
                self.APP.sfc.zoom = 100
                f.write(str(self.APP.sfc.zoom))
                f.close()
                self.APP.cwc.frame_image()
                self.path_read_image(
                    self.tree_folder[4][0],
                    file_name,
                    0
                )

        else:
            if str(
                self.APP.tree.item(curItem)["text"]
            ) and (not str(
                    self.APP.tree.item(parentItem)["text"]
                )
            ):
                # サブダイヤログを表示する
                title = u'{0}に挿入'.format(self.APP.tree.item(curItem)["text"])
                dialog = MD.MyDialogClass(self.APP, "挿入", True, title, False)
                self.MASTER.wait_window(dialog.sub_name_win)
                file_name = dialog.txt
                del dialog
                if not file_name == "":
                    self.APP.fmc.open_file_save(self.APP.fmc.now_path)
                    curItem = self.APP.tree.focus()
                    text = self.APP.tree.item(curItem)["text"]
                    path = ""
                    tree = ""
                    # 選択されているフォルダを見つける
                    for val in self.tree_folder:
                        if text == val[1]:
                            if val[0] == self.tree_folder[0][0]:
                                self.APP.cwc.frame_character()
                                self.APP.txt_yobi_name.insert(
                                    tk.END,
                                    file_name
                                )
                            else:
                                self.APP.cwc.frame()

                            path = "./{0}/{1}.txt".format(val[0], file_name)
                            tree = self.APP.tree.insert(
                                val[0],
                                'end',
                                text=file_name
                            )
                            self.APP.fmc.now_path = path
                            break

                    # パスが存在すれば新規作成する
                    if not path == "":
                        f = open(path, 'w', encoding='utf-8')
                        f.write("")
                        f.close()
                        # ツリービューを選択状態にする
                        self.APP.tree.see(tree)
                        self.APP.tree.selection_set(tree)
                        self.APP.tree.focus(tree)
                        self.select_list_item = file_name
                        self.APP.winfo_toplevel().title(
                            u"小説エディタ\\{0}\\{1}"
                            .format(text, file_name)
                        )
                        self.APP.text.focus()
                        # テキストを読み取り専用を解除する
                        self.APP.text.configure(state='normal')
                        self.APP.hpc.create_tags()
            # 子アイテムを右クリックしたとき
            else:
                if str(self.APP.tree.item(curItem)["text"]):
                    # 項目を削除する
                    file_name = self.APP.tree.item(curItem)["text"]
                    text = self.APP.tree.item(parentItem)["text"]
                    # ＯＫ、キャンセルダイアログを表示し、ＯＫを押したとき
                    if messagebox.askokcancel(
                        u"項目削除",
                        "{0}を削除しますか？".format(file_name)
                    ):
                        image_path = ""
                        path = ""
                        # パスを取得する
                        for val in self.tree_folder:
                            if text == val[1]:
                                path = "./{0}/{1}.txt".format(
                                    val[0],
                                    file_name
                                )
                                image_path = "./{0}/{1}.gif".format(
                                    val[0],
                                    file_name
                                )
                                self.APP.tree.delete(curItem)
                                self.APP.fmc.now_path = ""
                                break
                        # imageパスが存在したとき
                        if os.path.isfile(image_path):
                            os.remove(image_path)

                        # パスが存在したとき
                        if not path == "":
                            os.remove(path)
                            self.APP.cwc.frame()
                            self.APP.text.focus()

    def on_name_click(self, event=None):
        """名前の変更

        ・リストボックスの名前を変更する。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        curItem = self.APP.tree.focus()              # 選択アイテムの認識番号取得
        parentItem = self.APP.tree.parent(curItem)   # 親アイテムの認識番号取得
        text = self.APP.tree.item(parentItem)["text"]
        if not text == "":
            sub_text = self.APP.tree.item(curItem)["text"]
            title = u'{0}の名前を変更'.format(sub_text)
            dialog2 = MD.MyDialogClass(self.APP, u"変更", True, title, sub_text)
            self.MASTER.wait_window(dialog2.sub_name_win)
            # テキストを読み取り専用を解除する
            self.APP.text.configure(state='normal')
            co_text = dialog2.txt
            del dialog2
            for val in self.tree_folder:
                if text == val[1]:
                    path1 = "./{0}/{1}.txt".format(val[0], sub_text)
                    path2 = "./{0}/{1}.txt".format(val[0], co_text)
                    self.APP.fmc.now_path = path2
                    # テキストの名前を変更する
                    os.rename(path1, path2)
                    self.APP.tree.delete(curItem)
                    Item = self.APP.tree.insert(
                        parentItem,
                        'end',
                        text=co_text
                    )
                    self.APP.tree.selection_set(Item)
                    self.path_read_text(val[0], co_text)
                    return

    def path_read_image(self, image_path, image_name, scale):
        """イメージを読み込んで表示

        ・パスが存在すればイメージファイルを読み込んで表示する。

        Args:
            image_path (str): イメージファイルの相対パス
            image_name (str): イメージファイルの名前
            scale (int): 拡大率(%)

        """
        if not self.APP.fmc.now_path == "":
            title = "{0}/{1}.gif".format(
                image_path,
                image_name
            )
            giffile = Image.open(title)
            if scale > 0:
                giffile = giffile.resize(
                    (
                        int(giffile.width / 100*scale),
                        int(giffile.height / 100*scale)
                    ),
                    resample=Image.LANCZOS
                )

            self.APP.image_space.photo = ImageTk.PhotoImage(giffile)
            self.APP.image_space.itemconfig(
                self.APP.image_on_space,
                image=self.APP.image_space.photo
            )
            # イメージサイズにキャンバスサイズを合わす
            self.APP.image_space.config(
                scrollregion=(
                    0,
                    0,
                    giffile.size[0],
                    giffile.size[1]
                )
            )
            giffile.close()

        self.APP.winfo_toplevel().title(
                u"小説エディタ\\{0}\\{1}".format(self.tree_folder[4][1], image_name)
            )

    def path_read_text(self, text_path, text_name):
        """テキストを読み込んで表示

        ・パスが存在すればテキストを読み込んで表示する。

        Args:
            text_path (str): テキストファイルの相対パス
            text_name (str): テキストファイルの名前

        """
        if not self.APP.fmc.now_path == "":
            if not self.APP.fmc.now_path.find(self.tree_folder[0][0]) == -1:
                self.APP.txt_yobi_name.delete('0', tk.END)
                self.APP.txt_name.delete('0', tk.END)
                self.APP.txt_birthday.delete('0', tk.END)
                self.APP.text_body.delete('1.0', tk.END)
                tree = ET.parse(self.APP.fmc.now_path)
                elem = tree.getroot()
                self.APP.txt_yobi_name.insert(tk.END, elem.findtext("call"))
                self.APP.txt_name.insert(tk.END, elem.findtext("name"))
                self.APP.var.set(elem.findtext("sex"))
                self.APP.txt_birthday.insert(tk.END, elem.findtext("birthday"))
                self.APP.text_body.insert(tk.END, elem.findtext("body"))
                title = "{0}/{1}.gif".format(
                    self.tree_folder[0][0],
                    elem.findtext("call")
                )
                if os.path.isfile(title):
                    self.APP.sfc.print_gif(title)
            else:
                self.APP.text.delete('1.0', tk.END)
                f = open(self.APP.fmc.now_path, 'r', encoding='utf-8')
                self.text_text = f.read()
                self.APP.text.insert(tk.END, self.text_text)
                f.close()

            self.APP.winfo_toplevel().title(
                u"小説エディタ\\{0}\\{1}".format(text_path, text_name)
            )
            # シンタックスハイライトをする
            self.APP.hpc.all_highlight()

    def on_double_click(self, event=None):
        """ツリービューをダブルクリック

        ・ファイルを保存して閉じて、選択されたアイテムを表示する。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        curItem = self.APP.tree.focus()              # 選択アイテムの認識番号取得
        parentItem = self.APP.tree.parent(curItem)   # 親アイテムの認識番号取得
        text = self.APP.tree.item(parentItem)["text"]
        # 開いているファイルを保存
        self.APP.fmc.open_file_save(self.APP.fmc.now_path)
        # テキストを読み取り専用を解除する
        self.APP.cwc.frame()
        self.APP.text.configure(state='disabled')
        # 条件によって分離
        self.select_list_item = self.APP.tree.item(curItem)["text"]
        path = ""
        for val in self.tree_folder:
            if text == val[1]:
                if val[0] == self.tree_folder[4][0]:
                    path = "./{0}/{1}.txt".format(
                        val[0],
                        self.select_list_item
                    )
                    f = open(path, 'r', encoding='utf-8')
                    zoom = f.read()
                    self.APP.sfc.zoom = int(zoom)
                    self.APP.fmc.now_path = path
                    self.APP.cwc.frame_image()
                    self.path_read_image(
                        self.tree_folder[4][0],
                        self.select_list_item,
                        self.APP.sfc.zoom
                    )
                else:
                    path = "./{0}/{1}.txt".format(
                        val[0],
                        self.select_list_item
                    )
                    self.APP.fmc.now_path = path
                    if val[0] == self.tree_folder[0][0]:
                        self.APP.cwc.frame_character()
                    else:
                        # テキストを読み取り専用を解除する
                        self.APP.text.configure(state='normal')
                        self.APP.text.focus()

                    self.path_read_text(text, self.select_list_item)

                return

        self.APP.fmc.now_path = ""
        self.APP.winfo_toplevel().title(u"小説エディタ")
