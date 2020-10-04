#!/usr/bin/env python3
import os
import shutil
import tkinter as tk
import tkinter.filedialog as filedialog

from PIL import Image, ImageTk


class SubfunctionProcessingClass():
    """補助機能のクラス.

    ・補助機能があるプログラム群

    Args:
        app (instance): MainProcessingClassインスタンス
        tree_folder (str): ツリーフォルダの配列

    """
    def __init__(self, app, tree_folder):
        self.zoom = 0
        self.APP = app

    def mouse_y_scroll(self, event=None):
        """マウスホイール移動の設定.

        ・イメージキャンバスでマウスホイールを回したときにイメージキャンバス
        をスクロールする。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        if event.delta > 0:
            self.APP.image_space.yview_scroll(-1, 'units')
        elif event.delta < 0:
            self.APP.image_space.yview_scroll(1, 'units')

    def mouse_image_scroll(self, event=None):
        """Ctrl+マウスホイールの拡大縮小設定.

        ・イメージキャンバスでCtrl+マウスホイールを回したときに画像を
        拡大縮小する。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        curItem = self.APP.tree.focus()
        self.APP.lmc.select_list_item = self.APP.tree.item(curItem)["text"]
        title = "./data/image/{0}.txt".format(
            self.APP.lmc.select_list_item
        )
        f = open(title, 'r', encoding='utf-8')
        zoom = f.read()
        self.zoom = int(zoom)
        f.close()
        if event.delta > 0:
            self.zoom -= 5
            if self.zoom < 10:
                self.zoom = 10
        elif event.delta < 0:
            self.zoom += 5

        f = open(title, 'w', encoding='utf-8')
        f.write(str(self.zoom))
        f.close()
        self.APP.lmc.path_read_image(
                    'data/image',
                    self.APP.lmc.select_list_item,
                    self.zoom
                )

    def btn_click(self, event=None):
        """似顔絵ボタンを押したとき.

        ・似顔絵ボタンを押したときに画像イメージを似顔絵フレームに
        貼り付ける。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        fTyp = [(u"gif画像", ".gif")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        self.APP.filepath = filedialog.askopenfilename(
            filetypes=fTyp,
            initialdir=iDir
        )
        if not self.APP.filepath == "":
            path, ___ = os.path.splitext(
                os.path.basename(self.APP.fmc.now_path)
            )
            ____, ext = os.path.splitext(os.path.basename(self.APP.filepath))
            title = shutil.copyfile(
                self.APP.filepath,
                "./data/character/{0}{1}".format(
                    path,
                    ext
                )
            )
            self.print_gif(title)

    def clear_btn_click(self, event=None):
        """消去ボタンをクリックしたとき.

        ・消去ボタンをクリックしたときに画像イメージから画像を
        削除する。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        files = "./data/character/{0}.gif".format(
            self.APP.lmc.select_list_item
        )
        if os.path.isfile(files):
            os.remove(files)
            self.APP.cv.delete("all")

    def resize_gif(self, im):
        """画像をリサイズ.

        ・イメージファイルを縦が長いときは縦を、横が長いときは横を、
        同じときは両方を150pxに設定する。

        Args:
            im (instance): イメージインスタンス

        Returns:
            instance: イメージインスタンス

        """
        resized_image = ""
        if im.size[0] == im.size[1]:
            resized_image = im.resize((150, 150))
        elif im.size[0] > im.size[1]:
            zoom = int(im.size[1] * 150 / im.size[0])
            resized_image = im.resize((150, zoom))
        elif im.size[0] < im.size[1]:
            zoom = int(im.size[0] * 200 / im.size[1])
            resized_image = im.resize((zoom, 200))
        return resized_image

    def print_gif(self, title):
        """gifを表示.

        ・似顔絵キャンバスに画像を張り付ける。

        Args:
            title (str): タイトル

        """

        if not title == "":
            giffile = Image.open(title)
            self.APP.cv.photo = ImageTk.PhotoImage(self.resize_gif(giffile))
            giffile.close()
            self.APP.cv.itemconfig(
                self.APP.image_on_canvas,
                image=self.APP.cv.photo
            )

    def change_setting(self, event=None):
        """テキストの変更時.

        ・テキストを変更したときに行番号とハイライトを変更する。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        self.update_line_numbers()
        # その行のハイライトを行う
        self.APP.hpc.line_highlight(
            self.APP.fpc.replacement_check,
            self.APP.fpc.find_text,
            self.APP.fpc.next_pos
        )

    def update_line_numbers(self, event=None):
        """行番号の描画.

        ・行番号をつけて表示する。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        # 現在の行番号を全て消す
        self.APP.line_numbers.delete(tk.ALL)

        # Textの0, 0座標、つまり一番左上が何行目にあたるかを取得
        i = self.APP.text.index("@0,0")
        while True:
            # dlineinfoは、その行がどの位置にあり、どんなサイズか、を返す
            # (3, 705, 197, 13, 18) のように帰る(x,y,width,height,baseline)
            dline = self.APP.text.dlineinfo(i)
            # dlineinfoに、存在しない行や、スクロールしないと見えない行を渡すとNoneが帰る
            if dline is None:
                break
            else:
                y = dline[1]  # y座標を取得

            # (x座標, y座標, 方向, 表示テキスト)を渡して行番号のテキストを作成
            linenum = str(i).split(".")[0]
            self.APP.line_numbers.create_text(
                3,
                y,
                anchor=tk.NW,
                text=linenum,
                font=("", 12)
            )
            i = self.APP.text.index("%s+1line" % i)
