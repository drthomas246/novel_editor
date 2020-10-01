import os
import shutil
import tkinter.filedialog as filedialog

from PIL import Image, ImageTk


class SubFunctionClass():
    def __init__(self, app):
        """
        Args:
            app (instance): lineframeインスタンス

        """
        self.APP = app

    def mouse_y_scroll(self, event=None):
        """マウスホイール移動の設定

        ・イメージキャンバスでマウスホイールを回したときにイメージキャンバス
        をスクロールする。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        if event.delta > 0:
            self.APP.image_space.yview_scroll(-1, 'units')
        elif event.delta < 0:
            self.APP.image_space.yview_scroll(1, 'units')

    def btn_click(self, event=None):
        """似顔絵ボタンを押したとき

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
            path, ___ = os.path.splitext(os.path.basename(self.APP.now_path))
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
        """消去ボタンをクリックしたとき

        ・消去ボタンをクリックしたときに画像イメージから画像を
        削除する。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        files = "./data/character/{0}.gif".format(
            self.APP.select_list_item
        )
        if os.path.isfile(files):
            os.remove(files)
            self.APP.cv.delete("all")

    def resize_gif(self, im):
        """画像をリサイズする

        ・イメージファイルを縦が長いときは縦を、横が長いときは横を、
        同じときは両方を150pxに設定する。

        Args:
            im (instance): イメージインスタンス

        Returns:
            instance: イメージインスタンス

        """
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
        """gifを表示する

        ・似顔絵キャンバスに画像を張り付ける。

        Args:
            title (str): タイトル

        """

        if not title == "":
            giffile = Image.open(title)
            self.APP.cv.photo = ImageTk.PhotoImage(self.resize_gif(giffile))
            print(self.APP.cv.photo)
            giffile.close()
            self.APP.cv.itemconfig(
                self.APP.image_on_canvas,
                image=self.APP.cv.photo
            )
