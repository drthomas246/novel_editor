#!/usr/bin/env python3
import textwrap
import webbrowser
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
import xml.etree.ElementTree as ET

import jaconv
import pyttsx3
import requests


class ProcessingMenuClass():
    """処理メニューバーのクラス.

    ・処理メニューバーにあるプログラム群

    Args:
        app (instance): MainProcessingClass のインスタンス
        wiki_wiki (instance): wikipediaapi.Wikipedia のインスタンス
        tokenizer (instance): Tokenizer のインスタンス
    """
    font_size = 0
    """フォントのサイズ."""

    def __init__(self, app, wiki_wiki, tokenizer):
        # yahooの校正支援
        self.KOUSEI = "{urn:yahoo:jp:jlp:KouseiService}"
        self.app = app
        self.wiki_wiki = wiki_wiki
        self.tokenizer = tokenizer

    def ruby_huri(self):
        """ルビをふり.

        ・選択文字列に小説家になろうのルビを振る。
        """
        hon = ""
        # 選択文字列を切り取る
        set_ruby = self.app.text.get('sel.first', 'sel.last')
        # 選択文字列を削除する
        self.app.text.delete('sel.first', 'sel.last')
        # 形態素解析を行う
        for token in self.tokenizer.tokenize(set_ruby):
            # ルビの取得
            ruby = ""
            ruby = jaconv.kata2hira(token.reading)
            # 解析している文字のひらがなの部分を取得
            hira = ""
            for i in token.surface:
                if self.is_hiragana(i):
                    hira += i
            # ルビがないときと、記号の時の処理
            if ruby.replace(
                hira, ''
            ) == "" or token.part_of_speech.split(
                ","
            )[0] == u"記号":
                hon += token.surface
            else:
                # ルビ振りを行う
                hon += "|{0}≪{1}≫{2}".format(
                    token.surface.replace(hira, ''),
                    ruby.replace(hira, ''),
                    hira
                )

        # テキストを表示する
        self.app.text.insert('insert', hon)

    @staticmethod
    def is_hiragana(char):
        """文字がひらがなか判断.

        ・与えられた文字がひらがなかどうか判断する。

        Args:
            char (str): 判断する文字

        Returns:
            bool: ひらがなならTrue、違うならFalse
        """
        return (0x3040 < ord(char) < 0x3097)

    def count_moji(self):
        """文字数と行数を表示.

        ・文字数と行数をカウントして表示する。
        """
        # 行数の取得
        new_line = int(self.app.text.index('end-1c').split('.')[0])
        # 文字列の取得
        moji = self.app.text.get('1.0', 'end')
        # ２０文字で区切ったときの行数を数える
        gen_mai = 0
        for val in moji.splitlines():
            gen_mai += len(textwrap.wrap(val, 20))
        # メッセージボックスの表示
        messagebox.showinfo(
            self.app.dic.get_dict("Number of characters etc"),
            self.app.dic.get_dict(
                "Characters : {0} Lines : {1}\n Manuscript papers : {2}"
            )
            .format(
                len(moji)-new_line,
                new_line,
                -(-gen_mai//20)))

    def find_wikipedia(self):
        """意味を検索.

        ・Wikipedia-APIライブラリを使ってWikipediaから選択文字の意味を
        検索する。
        """
        # wikipediaから
        select_text = self.app.text.selection_get()
        page_py = self.wiki_wiki.page(select_text)
        # ページがあるかどうか判断
        if page_py.exists():
            messagebox.showinfo(
                self.app.dic.get_dict(
                    "Meaning of [{0}]"
                ).format(select_text),
                page_py.summary
            )
        else:
            messagebox.showwarning(
                self.app.dic.get_dict(
                    "Meaning of [{0}]"
                ).format(select_text),
                self.app.dic.get_dict("Can't find.")
            )

    def open_becoming_novelist_page(self):
        """小説家になろうのユーザーページを開く.

        ・インターネットブラウザで小説家になろうのユーザーページを開く。
        """
        webbrowser.open("https://syosetu.com/user/top/")

    def read_text(self):
        """テキストを読み上げる.

        ・pyttsx3ライブラリを使ってテキストボックスに書かれているものを読み上げる。
        """
        self.gyou_su = 0
        self.text_len = 0
        self.app.text.focus()
        self.read_texts = True
        self.engine = pyttsx3.init()
        self.engine.connect('started-word', self.pyttsx3_onword)
        self.engine.connect('finished-utterance', self.pyttsx3_onend)
        self.engine.setProperty('rate', 150)
        self.engine.say(self.app.text.get('1.0', 'end - 1c'))
        self.engine.startLoop(False)
        self.externalLoop()

    def externalLoop(self):
        """文章読み上げ繰り返し処理.

        ・文章読み上げを繰り返し続ける。
        """
        self.engine.iterate()

    def pyttsx3_onword(self, name, location, length):
        """文章を読み上げ中の処理.

        ・文章読み始めるときに止めるダイアログを出してから読み上げる。
        読み上げている最中は読み上げている行を選択状態にする。

        Args:
            name (str): 読み上げに関連付けられた名前
            location (int): 現在の場所
            length (int): 不明
        """
        # 今読んでいる場所と選択位置を比較する
        if location > self.text_len:
            # すべての選択一度解除する
            self.app.text.tag_remove('sel', '1.0', 'end')
            # 現在読んでいる場所を選択する
            self.app.text.tag_add(
                'sel',
                "{0}.0".format(self.gyou_su),
                "{0}.0".format(self.gyou_su+1)
            )
            # 次の行の長さをtextlenに入力する
            self.text_len += len(
                self.app.text.get(
                    '{0}.0'.format(self.gyou_su),
                    '{0}.0'.format(self.gyou_su+1)
                )
            )
            # カーソルを文章の一番後ろに持ってくる
            self.app.text.mark_set('insert', '{0}.0'.format(self.gyou_su+1))
            self.app.text.see('insert')
            self.app.text.focus()
            # 行を１行増やす
            self.gyou_su += 1
        # 読み初めての処理
        if self.read_texts:
            # 読むのを中止するウインドウを作成する
            self.sub_read_win = tk.Toplevel(self.app)
            button = ttk.Button(
                self.sub_read_win,
                text=self.app.dic.get_dict("Stop"),
                width=str(self.app.dic.get_dict("Stop")),
                padding=(100, 5),
                command=self.pyttsx3_onreadend
            )
            button.grid(row=1, column=1)
            # 最前面に表示し続ける
            self.sub_read_win.attributes("-topmost", True)
            # サイズ変更禁止
            self.sub_read_win.resizable(width=0, height=0)
            self.sub_read_win.title(
                self.app.dic.get_dict("Read aloud")
            )
            self.read_texts = False

    def pyttsx3_onreadend(self):
        """中止するボタンを押したときの処理.

        ・中止ボタンを押したときに読み上げをやめ、中止ウインドウ
        を削除する。
        """
        self.engine.stop()
        self.engine.endLoop()
        self.sub_read_win.destroy()
        self.app.text.tag_remove('sel', '1.0', 'end')

    def pyttsx3_onend(self, name, completed):
        """文章を読み終えた時の処理.

        ・文章を読み終えたら中止ウインドウを削除する。

        Args:
            name (str): 読み上げに関連付けられた名前
            completed (bool): 文章が読み上げ終わった(True)
        """
        self.engine.stop()
        self.engine.endLoop()
        self.sub_read_win.destroy()
        self.app.text.tag_remove('sel', '1.0', 'end')

    def yahoo(self):
        """Yahoo! 校正支援.

        ・Yahoo! 校正支援を呼び出し表示する。

        Args:
            event (instance): tkinter.Event のインスタンス
        """
        html = self.yahoocall(
            self.yahoo_appid,
            self.app.text.get('1.0', 'end -1c')
        )
        if not self.yahoo_appid == "":
            self.yahooresult(html)
            self.yahoo_tree.bind("<Double-1>", self.on_double_click_yahoo)

    def yahoocall(self, yahoo_appid="", sentence=""):
        """yahooの校正支援を呼び出し.

        ・Yahoo! 校正支援をClient IDを使って呼び出す。

        Args:
            yahoo_appid (str): Yahoo! Client ID
            sentence (str): 校正をしたい文字列

        Returns:
            str: 校正結果
        """
        if yahoo_appid == "":
            messagebox.showerror(
                self.app.dic.get_dict("Yahoo! Client ID"),
                self.app.dic.get_dict(
                    "Yahoo! Client ID is not find."
                    "\nRead Readme.pdf and set it again."
                )
            )
            return
        url = "https://jlp.yahooapis.jp/KouseiService/V1/kousei"
        data = {
            "appid": yahoo_appid.rstrip('\n'),
            "sentence": sentence,
        }
        html = requests.post(url, data)
        return html.text

    def yahooresult(self, html):
        """校正支援を表示する画面を制作.

        ・校正結果を表示するダイアログを作成する。

        Args:
            html (str): 校正結果
        """
        xml = ET.fromstring(html)
        # サブウインドウの表示
        sub_win = tk.Toplevel(self.app)
        # ツリービューの表示
        self.yahoo_tree = ttk.Treeview(sub_win)
        self.yahoo_tree["columns"] = (1, 2, 3, 4, 5)
        # 表スタイルの設定(headingsはツリー形式ではない、通常の表形式)
        self.yahoo_tree["show"] = "headings"
        self.yahoo_tree.column(1, width=100)
        self.yahoo_tree.column(2, width=80)
        self.yahoo_tree.column(3, width=75)
        self.yahoo_tree.column(4, width=150)
        self.yahoo_tree.column(5, width=120)
        self.yahoo_tree.heading(
            1,
            text=u"先頭からの文字数"
        )
        self.yahoo_tree.heading(
            2,
            text=u"対象文字数"
        )
        self.yahoo_tree.heading(
            3,
            text=u"対象表記"
        )
        self.yahoo_tree.heading(
            4,
            text=u"言い換え候補文字列"
        )
        self.yahoo_tree.heading(
            5,
            text=u"指摘の詳細情報"
        )
        # 情報を取り出す
        for child in list(xml):
            StartPos = (child.findtext(self.KOUSEI+"StartPos"))
            Length = (child.findtext(self.KOUSEI+"Length"))
            Surface = (child.findtext(self.KOUSEI+"Surface"))
            ShitekiWord = (child.findtext(self.KOUSEI+"ShitekiWord"))
            ShitekiInfo = (child.findtext(self.KOUSEI+"ShitekiInfo"))
            self.yahoo_tree.insert(
                "",
                "end",
                values=(StartPos,
                        Length,
                        Surface,
                        ShitekiWord,
                        ShitekiInfo
                        )
                )

        self.yahoo_tree.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        # スクロールバーを表示する
        SCRLBAR_Y = ttk.Scrollbar(
            sub_win,
            orient=tk.VERTICAL,
            command=self.yahoo_tree.yview
        )
        self.yahoo_tree.configure(yscroll=SCRLBAR_Y.set)
        SCRLBAR_Y.grid(row=0, column=1, sticky=(tk.N, tk.S))
        # 最前面に表示し続ける
        sub_win.attributes("-topmost", True)
        sub_win.title(
            self.app.dic.get_dict("Sentence structure")
        )

    def on_double_click_yahoo(self, event=None):
        """Yahoo! 校正支援リストをダブルクリック.

        ・Yahoo! 校正支援ダイアログのリストをダブルクリックすると
        その該当箇所を選択する。

        Args:
            event (instance): tkinter.Event のインスタンス
        """
        i = 0
        textlen = 0
        textforlen = 0
        curItem = self.yahoo_tree.focus()
        value = self.yahoo_tree.item(curItem)
        # 出てくる場所を取得
        val = int(value.get("values")[0])
        # 出てくる文字数を取得
        lenge = value.get("values")[1]
        # 何行目になるか確認する
        while True:
            if val > textlen:
                i += 1
                textforlen = textlen
                textlen += len(
                    self.app.text.get(
                        '{0}.0'.format(i),
                        '{0}.0'.format(i+1)
                    )
                )
            else:
                break
        if i == 0:
            i = 1
        # 選択状態を一旦削除
        self.app.text.tag_remove('sel', '1.0', 'end')
        # 選択状態にする
        self.app.text.tag_add(
            'sel',
            "{0}.{1}".format(i, val-textforlen),
            "{0}.{1}".format(i, val-textforlen+lenge)
        )
        # カーソルの移動
        self.app.text.mark_set('insert', '{0}.{1}'.format(i, val-textforlen))
        self.app.text.see('insert')
        # フォーカスを合わせる
        self.app.text.focus()
        return

    def font_dialog(self, event=None):
        """フォントサイズダイアログを作成.

        ・フォントサイズダイアログを作成し表示する。

        Args:
            event (instance): tkinter.Event のインスタンス
        """
        self.app.sub_wins = tk.Toplevel(self.app)
        self.app.intSpin = ttk.Spinbox(self.app.sub_wins, from_=12, to=72)
        self.app.intSpin.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=5,
            pady=5,
            sticky=tk.W+tk.E,
            ipady=3
        )
        button = ttk.Button(
            self.app.sub_wins,
            text=self.app.dic.get_dict("Resize"),
            width=str(self.app.dic.get_dict("Resize")),
            padding=(10, 5),
            command=self.font_size_Change
        )
        button.grid(row=1, column=1)
        self.app.intSpin.set(ProcessingMenuClass.font_size)
        self.app.sub_wins.title(
            self.app.dic.get_dict("Font size")
        )

    def font_size_Change(self):
        """フォントのサイズの変更.

        ・サイズ変更を押されたときにサイズを変更する。
        上は72ptまで下は12ptまでにする。
        """
        # 比較のため数値列に変更
        font_size = int(self.app.intSpin.get())
        if font_size < 12:  # 12より下の値を入力した時、12にする
            font_size = 12
        elif 72 < font_size:  # 72より上の値を入力した時、72にする
            font_size = 72
        # 文字列にもどす
        self.font_size_input(str(font_size))
        self.app.sub_wins.destroy()
        # フォントサイズの変更
        self.app.text.configure(font=(self.app.font, self.font_size))
        # ラインナンバーの変更
        self.app.spc.update_line_numbers()
        # ハイライトのやり直し
        self.app.hpc.all_highlight()

    @classmethod
    def font_size_input(cls, font_size):
        """フォントサイズを入力.

        ・フォントサイズをクラス変数に入力する。

        Args:
            font_size (str): フォントサイズ
        """
        cls.font_size = font_size
