#!/usr/bin/env python3
import os
import shutil
import tkinter as tk
import tkinter.filedialog as filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pycirclize import Circos
import pandas as pd

from PIL import Image, ImageTk

from . import FileMenu
from . import ListMenuClass
from . import Definition


class SubfunctionProcessingClass(Definition.DefinitionClass):
    """補助機能のクラス.

    ・補助機能があるプログラム群

    Args:
        app (instance): MainProcessingClass のインスタンス
        locale_var (str): ロケーション
        master (instance): toplevel のインスタンス
    """

    def __init__(self, app, locale_var, master=None):
        super().__init__(locale_var, master)
        self.zoom = 0
        self.app = app

    def mouse_y_scroll(self, event=None):
        """マウスホイール移動の設定.

        ・イメージキャンバスでマウスホイールを回したときにイメージキャンバス
        をスクロールする。

        Args:
            event (instance): tkinter.Event のインスタンス
        """
        if event.delta > 0:
            self.app.CanvasImage.yview_scroll(-1, "units")
        elif event.delta < 0:
            self.app.CanvasImage.yview_scroll(1, "units")

    def mouse_image_scroll(self, event=None):
        """Ctrl+マウスホイールの拡大縮小設定.

        ・イメージキャンバスでCtrl+マウスホイールを回したときに画像を
        拡大縮小する。

        Args:
            event (instance): tkinter.Event のインスタンス
        """
        title = "./data/image/{0}.txt".format(
            ListMenuClass.ListMenuClass.select_list_item
        )
        with open(title, encoding="utf-8") as f:
            zoom = f.read()

        self.zoom = int(zoom)
        f.close()
        if event.delta > 0:
            self.zoom -= 5
            if self.zoom < 10:
                self.zoom = 10
        elif event.delta < 0:
            self.zoom += 5

        with open(title, mode="w", encoding="utf-8") as f:
            f.write(str(self.zoom))

        self.app.lmc.path_read_image(
            "data/image", ListMenuClass.ListMenuClass.select_list_item, self.zoom
        )

    def btn_click(self, event=None):
        """似顔絵ボタンを押したとき.

        ・似顔絵ボタンを押したときに画像イメージを似顔絵フレームに
        貼り付ける。

        Args:
            event (instance): tkinter.Event のインスタンス
        """
        fTyp = [(self.app.dic.get_dict("gif image"), ".gif")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        self.app.filepath = filedialog.askopenfilename(filetypes=fTyp, initialdir=iDir)
        if not self.app.filepath == "":
            path, ___ = os.path.splitext(
                os.path.basename(FileMenu.FileMenuClass.now_path)
            )
            ____, ext = os.path.splitext(os.path.basename(self.app.filepath))
            title = shutil.copyfile(
                self.app.filepath, "./data/character/{0}{1}".format(path, ext)
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
            ListMenuClass.ListMenuClass.select_list_item
        )
        if os.path.isfile(files):
            os.remove(files)
            self.app.CanvasPortrait.delete("all")

    @staticmethod
    def resize_gif(im):
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
            self.app.CanvasPortrait.photo = ImageTk.PhotoImage(self.resize_gif(giffile))
            giffile.close()
            self.app.CanvasPortrait.itemconfig(
                self.app.ImageOnPortrait, image=self.app.CanvasPortrait.photo
            )

    def change_setting(self, event=None):
        """テキストの変更時.

        ・テキストを変更したときに行番号とハイライトを変更する。

        Args:
            event (instance): tkinter.Event のインスタンス
        """
        self.update_line_numbers()
        # その行のハイライトを行う
        self.app.hpc.line_highlight()

    def update_line_numbers(self, event=None):
        """行番号の描画.

        ・行番号をつけて表示する。

        Args:
            event (instance): tkinter.Event のインスタンス
        """
        # 現在の行番号を全て消す
        self.app.CanvasLineNumbers.delete(tk.ALL)

        # Textの0, 0座標、つまり一番左上が何行目にあたるかを取得
        i = self.app.NovelEditor.index("@0,0")
        while True:
            # dlineinfoは、その行がどの位置にあり、どんなサイズか、を返す
            # (3, 705, 197, 13, 18) のように帰る(x,y,width,height,baseline)
            dline = self.app.NovelEditor.dlineinfo(i)
            # dlineinfoに、存在しない行や、スクロールしないと見えない行を渡すとNoneが帰る
            if dline is None:
                break
            else:
                y = dline[1]  # y座標を取得

            # (x座標, y座標, 方向, 表示テキスト)を渡して行番号のテキストを作成
            linenum = str(i).split(".")[0]
            self.app.CanvasLineNumbers.create_text(
                3, y, anchor=tk.NW, text=linenum, font=("", 12)
            )
            i = self.app.NovelEditor.index("%s+1line" % i)

    def update_character_chart(self, event=None):
        """キャラクター画面のレーダーチャートを再描画.

        ・スライダーバーから値をとって再描画する。

        Args:
            event (instance): tkinter.Event のインスタンス
        """
        # print(self.app.SliderExtraversion.get())
        df = pd.DataFrame(
            data=[
                [
                    self.app.SliderExtraversion.get(),
                    self.app.SliderAgreeableness.get(),
                    self.app.SliderConscientiousness.get(),
                    self.app.SliderNeuroticism.get(),
                    self.app.SliderOpenness.get(),
                ]
            ],
            index=["Hero"],
            columns=[
                self.app.dic.get_dict("Extraversion"),
                self.app.dic.get_dict("Agreeableness"),
                self.app.dic.get_dict("Conscientiousness"),
                self.app.dic.get_dict("Neuroticism"),
                self.app.dic.get_dict("Openness"),
            ],
        )
        circos = Circos.radar_chart(
            df,
            vmax=6,
            grid_interval_ratio=0.166666666666666,
            grid_label_kws=dict(size=20),
            label_kws_handler=lambda v: dict(size=20),
        )
        fig = circos.plotfig(dpi=50)
        plt.close()
        self.app.canvasCharacterChart.get_tk_widget().pack_forget()
        self.app.canvasCharacterChart = FigureCanvasTkAgg(
            fig, master=self.app.FrameCharacterChartMap
        )
        self.app.canvasCharacterChart.draw()
        self.app.canvasCharacterChart.get_tk_widget().pack()
