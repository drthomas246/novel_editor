#!/usr/bin/env python3
# -*- coding: utf8 -*-
import os
import re
import sys
import zipfile
import shutil
import webbrowser
import platform
import textwrap
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog
import xml.etree.ElementTree as ET

import jaconv
import pyttsx3
import wikipediaapi
import requests
from PIL import Image, ImageTk
from janome.tokenizer import Tokenizer


class CustomText(tk.Text):
    """Textのイベントを拡張したウィジェット

    ・textに<<Scroll>>イベントと、<<Change>>イベントを追加する。

    """

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.tk.eval('''
            proc widget_proxy {widget widget_command args} {
                set result [uplevel [linsert $args 0 $widget_command]]
                if {([lrange $args 0 1] == {xview moveto}) ||
                    ([lrange $args 0 1] == {xview scroll}) ||
                    ([lrange $args 0 1] == {yview moveto}) ||
                    ([lrange $args 0 1] == {yview scroll})} {
                    event generate  $widget <<Scroll>> -when tail
                }
                if {([lindex $args 0] in {insert replace delete})} {
                    event generate  $widget <<Change>> -when tail
                }
                # return the result from the real widget command
                return $result
            }
            ''')
        self.tk.eval('''
            rename {widget} _{widget}
            interp alias {{}} ::{widget} {{}} widget_proxy {widget} _{widget}
        '''.format(widget=str(self)))


class Mydialog():
    """ダイアログ作成クラス

    ・自作ダイアログを呼び出し表示する。

    Attributes:
        self.txt (str): インプットボックスの値
        self.sub_name_win (instance): ダイアログウインドウインスタンス
        self.txt_name (instance): インプットボックスインスタンス

    """

    def __init__(self, message, button1, button2, title, text):
        """
        Args:
            message (instance): 親ウインドウインスタンス
            button1 (str): ボタンのメッセージ
            button2 (bool): キャンセルボタンを表示する(True)
            title (str): タイトル
            text (bool): 選択状態にする(True)

        """
        self.txt = ""
        self.sub_name_win = tk.Toplevel(message)
        self.txt_name = ttk.Entry(self.sub_name_win, width=40)
        self.txt_name.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=5,
            pady=5,
            sticky=tk.W+tk.E,
            ipady=3
        )
        button = ttk.Button(
            self.sub_name_win,
            text=button1,
            width=str(button1),
            padding=(10, 5),
            command=self.sub_name_ok
        )
        button.grid(row=1, column=0)
        if button2:
            button = ttk.Button(
                self.sub_name_win,
                text=u'キャンセル',
                width=str(u'キャンセル'),
                padding=(10, 5),
                command=self.sub_name_win.destroy
            )

            button.grid(row=1, column=1)
            self.txt_name.focus()
            if text is not False:
                self.txt_name.insert(tk.END, text)
                self.txt_name.select_range(0, 'end')

        self.sub_name_win.title(title)
        self.txt_name.focus()

    def sub_name_ok(self, event=None):
        """ダイアログボタンクリック時の処理

        ・自作ダイアログのボタンをクリックしたときにインプットボックスに
        入力されている値を取得する。

        Args:
            event (instance): tkinter.Event のインスタンス

        Returns:
            str: インプットボックスの値

        """
        self.txt = self.txt_name.get()
        self.sub_name_win.destroy()
        return self.txt


class LineFrame(ttk.Frame):
    """メインフレーム処理

    ・メインに表示される画面の処理をする。

    """

    def __init__(self, master=None, **kwargs):
        """初期設定

        ・初期化、メニューバーの作成、画面の描画、イベントの追加をする。

        """
        super().__init__(master, **kwargs)
        self.initialize()

        self.menu_bar = tk.Menu(self.master)
        self.master.config(menu=self.menu_bar)

        self.create_widgets()
        self.create_event()

    def initialize(self):
        """初期化処理

        ・変数の初期化及び起動準備をする。

        """
        # 今の処理ししているファイルのパス
        self.now_path = ""
        # 現在開いているファイル
        self.file_path = ""
        # 検索文字列
        self.last_text = ""
        # 現在入力中の初期テキスト
        self.text_text = ""
        # 文字の大きさ
        self.int_var = 16
        # yahooの校正支援
        self.KOUSEI = "{urn:yahoo:jp:jlp:KouseiService}"
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
        for val in tree_folder:
            os.makedirs('./{0}'.format(val[0]))

    def create_widgets(self):
        """画面の描画

        ・メインウインドウにウェジットを配置する。

        """
        # メニューの配置
        File_menu = tk.Menu(self.menu_bar, tearoff=0)
        Edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        List_menu = tk.Menu(self.menu_bar, tearoff=0)
        Processing_menu = tk.Menu(self.menu_bar, tearoff=0)
        Help_menu = tk.Menu(self.menu_bar, tearoff=0)
        # ファイルメニュー
        File_menu.add_command(
            label=u'新規作成(N)',
            under=5,
            accelerator='Ctrl+N',
            command=self.new_open
        )
        File_menu.add_command(
            label=u'開く(O)',
            under=3,
            accelerator='Ctrl+E',
            command=self.open_file
        )
        File_menu.add_separator()
        File_menu.add_command(
            label=u'保存(S)',
            under=3,
            accelerator='Ctrl+S',
            command=self.overwrite_save_file
        )
        File_menu.add_command(
            label=u'名前を付けて保存(W)',
            under=9,
            accelerator='Ctrl+W',
            command=self.save_file
        )
        File_menu.add_separator()
        File_menu.add_command(
            label=u'閉じる(C)',
            under=4,
            accelerator='Ctrl+C',
            command=on_closing
        )
        self.menu_bar.add_cascade(
            label=u'ファイル(F)',
            under=5,
            menu=File_menu
        )
        # 編集メニュー
        Edit_menu.add_command(
            label=u'やり直し(R)',
            under=5,
            accelerator='Ctrl+Z',
            command=self.redo
        )
        Edit_menu.add_command(
            label=u'戻る(U)',
            under=3,
            accelerator='Ctrl+Shift+Z',
            command=self.undo
        )
        Edit_menu.add_separator()
        Edit_menu.add_command(
            label=u'切り取り(X)',
            under=5,
            accelerator='Ctrl+X',
            command=self.cut
        )
        Edit_menu.add_command(
            label=u'コピー(C)',
            under=4,
            accelerator='Ctrl+C',
            command=self.copy
        )
        Edit_menu.add_command(
            label=u'貼り付け(V)',
            under=5,
            accelerator='Ctrl+V',
            command=self.paste
        )
        Edit_menu.add_separator()
        Edit_menu.add_command(
            label=u'検索(F)',
            under=3,
            accelerator='Ctrl+F',
            command=self.find_dialog
        )
        Edit_menu.add_command(
            label=u'置換(L)',
            under=3,
            accelerator='Ctrl+L',
            command=self.replacement_dialog
        )
        self.menu_bar.add_cascade(
            label=u'編集(E)',
            under=3,
            menu=Edit_menu
        )
        # 処理メニュー
        Processing_menu.add_command(
            label=u'ルビをふる(R)',
            under=6,
            accelerator='Ctrl+R',
            command=self.ruby
        )
        Processing_menu.add_command(
            label=u'文字数のカウント(C)',
            under=9,
            accelerator='Ctrl+Shift+C',
            command=self.moji_count
        )
        Processing_menu.add_command(
            label=u'選択文字の意味(M)',
            under=8,
            accelerator='Ctrl+Shift+F',
            command=self.find_dictionaly
        )
        Processing_menu.add_command(
            label=u'文章の読み上げ(B)',
            under=8,
            accelerator='Ctrl+Shift+R',
            command=self.read_text
        )
        Processing_menu.add_command(
            label=u'文章校正(Y)',
            under=5,
            accelerator='Ctrl+Y',
            command=self.yahoo
        )
        Processing_menu.add_separator()
        Processing_menu.add_command(
            label=u'フォントサイズの変更(F)',
            under=11,
            accelerator='Ctrl+Shift+F',
            command=self.font_dialog
        )
        Processing_menu.add_separator()
        Processing_menu.add_command(
            label=u'「小説家になろう」のページを開く(U)',
            under=17,
            accelerator='Ctrl+U',
            command=self.open_url
        )
        self.menu_bar.add_cascade(
            label=u'処理(P)',
            under=3,
            menu=Processing_menu
        )
        # リストメニュー
        List_menu.add_command(
            label=u'項目を増やす(U)',
            under=7,
            accelerator='選択右クリック',
            command=self.message_window
        )
        List_menu.add_command(
            label=u'項目を削除(D)',
            under=6,
            accelerator='選択右クリック',
            command=self.message_window
        )
        List_menu.add_command(
            label=u'項目の名前を変更(C)',
            under=9,
            accelerator='Ctrl+G',
            command=self.on_name_click
        )
        self.menu_bar.add_cascade(
            label=u'リスト(L)',
            under=4,
            menu=List_menu
        )
        # ヘルプメニュー
        Help_menu.add_command(
            label=u'ヘルプ(H)',
            under=4,
            accelerator='Ctrl+H',
            command=self.open_help
        )
        Help_menu.add_command(
            label=u'バージョン情報(V)',
            under=8,
            accelerator='Ctrl+Shift+V',
            command=self.open_version
        )
        self.menu_bar.add_cascade(
            label=u'ヘルプ(H)',
            under=4,
            menu=Help_menu
        )
        # ツリーコントロール、入力欄、行番号欄、スクロール部分を作成
        self.tree = ttk.Treeview(self, show="tree")
        self.tree.grid(row=0, column=0, sticky=(tk.N, tk.S))
        self.frame()
        self.tree_get_loop()

    def frame(self):
        """フレーム内にテキストボックスを表示

        ・メインウインドウの右側に行番号、テキストボックス、スクロールバー
        を表示する。

        """
        # f1フレームにテキストエディタを表示
        self.f1 = tk.Frame(self, relief=tk.RIDGE, bd=2)
        self.text = CustomText(
            self.f1,
            font=(self.font, self.int_var),
            undo=True
        )
        self.line_numbers = tk.Canvas(self.f1, width=30)
        self.ysb = ttk.Scrollbar(
            self.f1,
            orient=tk.VERTICAL,
            command=self.text.yview
        )
        # 入力欄にスクロールを紐付け
        self.text.configure(yscrollcommand=self.ysb.set)
        # 左から行番号、入力欄、スクロールウィジェット
        self.line_numbers.grid(row=0, column=0, sticky=(tk.N, tk.S))
        self.text.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.ysb.grid(row=0, column=2, sticky=(tk.N, tk.S))
        self.f1.columnconfigure(1, weight=1)
        self.f1.rowconfigure(0, weight=1)
        self.f1.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.W, tk.E))
        # テキスト入力欄のみ拡大されるように
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        # テキストを読み取り専用にする
        self.text.configure(state='disabled')
        # テキストにフォーカスを当てる
        self.text.focus()
        self.create_event_text()

    def frame_image(self):
        """フレーム内にイメージフレーム表示

        ・メインウインドウの右側にイメージキャンバス、スクロールバーを表示する。

        """
        self.f1 = tk.Frame(self, relief=tk.RIDGE, bd=2)
        self.image_space = tk.Canvas(self.f1, bg="black", width=30)
        self.image_ysb = ttk.Scrollbar(
            self.f1,
            orient=tk.VERTICAL,
            command=self.image_space.yview
        )
        self.image_xsb = ttk.Scrollbar(
            self.f1,
            orient=tk.HORIZONTAL,
            command=self.image_space.xview
        )
        self.image_space.configure(xscrollcommand=self.image_xsb.set)
        self.image_space.configure(yscrollcommand=self.image_ysb.set)
        self.image_space.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.image_ysb.grid(row=0, column=2, sticky=(tk.N, tk.S))
        self.image_xsb.grid(row=1, column=1, sticky=(tk.W, tk.E))
        self.f1.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.f1.columnconfigure(1, weight=1)
        self.f1.rowconfigure(0, weight=1)
        self.f1.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.W, tk.E))
        # デフォルトの画像を設定する
        self.image_space.photo = tk.PhotoImage(data=original_image)
        self.image_on_space = self.image_space.create_image(
            0,
            0,
            anchor='nw',
            image=self.image_space.photo
        )
        self.create_event_image()

    def frame_character(self):
        """フレーム内にイメージフレーム表示

        ・メインウインドウの右側に呼び名、似顔絵、名前、誕生日、略歴を表示する。

        """
        # チェック有無変数
        self.var = tk.IntVar()
        # value=0のラジオボタンにチェックを入れる
        self.var.set(0)
        self.f1 = tk.Frame(self, relief=tk.RIDGE, bd=2)
        self.label1 = tk.Label(self.f1, text=u"呼び名")
        self.txt_yobi_name = ttk.Entry(
            self.f1, width=30,
            font=(self.font, self.int_var)
        )
        self.label2 = tk.Label(self.f1, text=u"名前")
        self.txt_name = ttk.Entry(
            self.f1, width=40,
            font=(self.font, self.int_var)
        )
        self.f2 = tk.LabelFrame(self.f1, relief=tk.RIDGE, bd=2, text=u"性別")
        self.rdo1 = tk.Radiobutton(
            self.f2, value=0,
            variable=self.var,
            text=u'男'
        )
        self.rdo2 = tk.Radiobutton(
            self.f2, value=1,
            variable=self.var,
            text=u'女'
        )
        self.rdo3 = tk.Radiobutton(
            self.f2, value=2,
            variable=self.var,
            text=u'その他'
        )
        self.rdo1.grid(row=0, column=1)
        self.rdo2.grid(row=1, column=1)
        self.rdo3.grid(row=2, column=1)
        self.f3 = tk.LabelFrame(self.f1, relief=tk.RIDGE, bd=2, text=u"似顔絵")
        self.cv = self.foto_canvas = tk.Canvas(
            self.f3,
            bg="black",
            width=149,
            height=199
        )
        self.foto_canvas.grid(row=0, column=0)
        self.label3 = tk.Label(self.f1, text=u"誕生日")
        self.txt_birthday = ttk.Entry(
            self.f1, width=40,
            font=(self.font, self.int_var)
        )
        self.f4 = tk.Frame(self.f1)
        self.foto_button = ttk.Button(
            self.f4,
            width=5,
            text=u'挿入',
            command=self.btn_click
        )
        self.foto_button_calcel = ttk.Button(
            self.f4,
            width=5,
            text=u'消去',
            command=self.clear_btn_click
        )
        self.foto_button.grid(row=0, column=1)
        self.foto_button_calcel.grid(row=1, column=1)
        self.label4 = tk.Label(self.f1, text=u"略歴")
        self.text_body = tk.Text(
            self.f1,
            width=80,
            font=(self.font, self.int_var)
        )
        self.label1.grid(row=0, column=1, columnspa=2)
        self.txt_yobi_name.grid(row=1, column=1, columnspa=2)
        self.f2.grid(row=2, column=1, rowspan=2)
        self.f4.grid(row=3, column=2)
        self.f3.grid(row=0, column=3, rowspan=4)
        self.label2.grid(row=0, column=4, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.txt_name.grid(row=1, column=4)
        self.label3.grid(row=2, column=4)
        self.txt_birthday.grid(row=3, column=4)
        self.label4.grid(row=4, column=1, columnspa=4)
        self.text_body.grid(
            row=5,
            column=1,
            columnspa=4,
            sticky=(tk.N, tk.S, tk.W, tk.E)
        )
        self.f1.columnconfigure(1, weight=1)
        self.f1.columnconfigure(4, weight=1)
        self.f1.rowconfigure(5, weight=1)

        self.f1.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        # デフォルトの画像を設定する
        self.cv.photo = tk.PhotoImage(data=original_image)
        self.image_on_canvas = self.cv.create_image(
            0,
            0,
            anchor='nw',
            image=self.cv.photo
        )

        # キャラクターイベントを追加
        self.create_event_character()

    def create_event_text(self):
        """テキストイベントの設定

        ・テキストボックスにイベントを追加する。

        """
        # テキスト内でのスクロール時
        self.text.bind('<<Scroll>>', self.update_line_numbers)
        self.text.bind('<Up>', self.update_line_numbers)
        self.text.bind('<Down>', self.update_line_numbers)
        self.text.bind('<Left>', self.update_line_numbers)
        self.text.bind('<Right>', self.update_line_numbers)
        # テキストの変更時
        self.text.bind('<<Change>>', self.change_setting)
        # キー場押されたときの処理
        self.text.bind("<Any-KeyPress>", self.push_keys)
        # ウィジェットのサイズが変わった際。行番号の描画を行う
        self.text.bind('<Configure>', self.update_line_numbers)
        # Tab押下時(インデント、又はコード補完)
        self.text.bind('<Tab>', self.tab)
        # ルビを振る
        self.text.bind('<Control-Key-r>', self.ruby)
        # 開くダイアロクを表示する
        self.text.bind('<Control-Key-e>', self.open_file)
        # 保存ダイアロクを表示する
        self.text.bind('<Control-Key-w>', self.save_file)
        # 小説家になろうを開く
        self.text.bind('<Control-Key-u>', self.open_url)
        # 検索ダイアログを開く
        self.text.bind('<Control-Key-f>', self.find_dialog)
        # 置換ダイアログを開く
        self.text.bind('<Control-Key-l>', self.replacement_dialog)
        # 上書き保存する
        self.text.bind('<Control-Key-s>', self.overwrite_save_file)
        # 新規作成する
        self.text.bind('<Control-Key-n>', self.new_open)
        # helpページを開く
        self.text.bind('<Control-Key-h>', self.open_help)  # helpページを開く
        # Versionページを開く
        self.text.bind('<Control-Shift-Key-V>', self.open_version)
        # 文字数と行数をカウントすShift-る
        self.text.bind('<Control-Shift-Key-C>', self.moji_count)
        # redo処理
        self.text.bind('<Control-Shift-Key-Z>', self.redo)
        # フォントサイズの変更
        self.text.bind('<Control-Shift-Key-F>', self.font_dialog)
        # 意味を検索
        self.text.bind('<Control-Shift-Key-D>', self.find_dictionaly)
        # 文章を読み上げ
        self.text.bind('<Control-Shift-Key-R>', self.read_text)
        # yahoo文字列解析
        self.text.bind('<Control-Key-y>', self.yahoo)

    def create_event_image(self):
        """イメージイベントの設定

        ・イメージキャンバスにイベントを追加する。

        """
        self.image_space.bind('<MouseWheel>', self.mouse_y_scroll)
        self.image_space.bind('<Control-MouseWheel>', self.mouse_image_scroll)

    def create_event_character(self):
        """キャラクター欄のイベント設定

        ・キャラクター関係のボックスにイベントを追加する。

        """
        # 開くダイアロクを表示する
        self.txt_yobi_name.bind('<Control-Key-e>', self.open_file)
        self.txt_name.bind('<Control-Key-e>', self.open_file)
        self.txt_birthday.bind('<Control-Key-e>', self.open_file)
        self.text_body.bind('<Control-Key-e>', self.open_file)
        # 保存ダイアロクを表示する
        self.txt_yobi_name.bind('<Control-Key-w>', self.save_file)
        self.txt_name.bind('<Control-Key-w>', self.save_file)
        self.txt_birthday.bind('<Control-Key-w>', self.save_file)
        self.text_body.bind('<Control-Key-w>', self.save_file)
        # 小説家になろうを開く
        self.txt_yobi_name.bind('<Control-Key-u>', self.open_url)
        self.txt_name.bind('<Control-Key-u>', self.open_url)
        self.txt_birthday.bind('<Control-Key-u>', self.open_url)
        self.text_body.bind('<Control-Key-u>', self.open_url)
        # 検索ダイアログを開く
        self.txt_yobi_name.bind('<Control-Key-f>', self.find_dialog)
        self.txt_name.bind('<Control-Key-f>', self.find_dialog)
        self.txt_yobi_name.bind('<Control-Key-f>', self.find_dialog)
        self.text_body.bind('<Control-Key-f>', self.find_dialog)
        # 上書き保存する
        self.txt_yobi_name.bind('<Control-Key-s>', self.overwrite_save_file)
        self.txt_name.bind('<Control-Key-s>', self.overwrite_save_file)
        self.txt_birthday.bind('<Control-Key-s>', self.overwrite_save_file)
        self.text_body.bind('<Control-Key-s>', self.overwrite_save_file)
        # 新規作成する
        self.txt_yobi_name.bind('<Control-Key-n>', self.new_open)
        self.txt_name.bind('<Control-Key-n>', self.new_open)
        self.txt_yobi_name.bind('<Control-Key-n>', self.new_open)
        self.text_body.bind('<Control-Key-n>', self.new_open)
        # helpページを開く
        self.txt_yobi_name.bind('<Control-Key-h>', self.open_help)
        self.txt_name.bind('<Control-Key-h>', self.open_help)
        self.txt_birthday.bind('<Control-Key-h>', self.open_help)
        self.text_body.bind('<Control-Key-h>', self.open_help)
        # Versionページを開く
        self.txt_yobi_name.bind('<Control-Shift-Key-V>', self.open_version)
        self.txt_name.bind('<Control-Shift-Key-V>', self.open_version)
        self.txt_birthday.bind('<Control-Shift-Key-V>', self.open_version)
        self.txt_yobi_name.bind('<Control-Shift-Key-V>', self.open_version)
        # redo処理
        self.txt_yobi_name.bind('<Control-Shift-Key-Z>', self.redo)
        self.txt_name.bind('<Control-Shift-Key-Z>', self.redo)
        self.txt_birthday.bind('<Control-Shift-Key-Z>', self.redo)
        self.text_body.bind('<Control-Shift-Key-Z>', self.redo)
        # フォントサイズの変更
        self.txt_yobi_name.bind('<Control-Shift-Key-F>', self.font_dialog)
        self.txt_name.bind('<Control-Shift-Key-F>', self.font_dialog)
        self.txt_birthday.bind('<Control-Shift-Key-F>', self.font_dialog)
        self.text_body.bind('<Control-Shift-Key-F>', self.font_dialog)

    def create_event(self):
        """ツリービューイベントの設定

        ・ツリービューにイベントを追加する。

        """
        # ツリービューをダブルクリックしたときにその項目を表示する
        self.tree.bind("<Double-1>", self.on_double_click)
        # ツリービューの名前を変更する
        self.tree.bind("<Control-Key-g>", self.on_name_click)
        # ツリービューで右クリックしたときにダイアログを表示する
        self.tree.bind("<Button-3>", self.message_window)

    def push_keys(self, event=None):
        """キーが押されたときの処理

        ・何かキーが押されたときに検索処理を中断する。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        # 検索処理を中断する
        self.replacement_dialog = 0

    def mouse_y_scroll(self, event=None):
        """マウスホイール移動の設定

        ・イメージキャンバスでマウスホイールを回したときにイメージキャンバス
        をスクロールする。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        if event.delta > 0:
            self.image_space.yview_scroll(-1, 'units')
        elif event.delta < 0:
            self.image_space.yview_scroll(1, 'units')

    def mouse_image_scroll(self, event=None):
        """Ctrl+マウスホイールの拡大縮小設定

        ・イメージキャンバスでCtrl+マウスホイールを回したときに画像を
        拡大縮小する。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        curItem = self.tree.focus()
        self.select_list_item = self.tree.item(curItem)["text"]
        title = "./{0}/{1}.txt".format(
            tree_folder[4][0],
            self.select_list_item
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
        self.path_read_image(
                    tree_folder[4][0],
                    self.select_list_item,
                    self.zoom
                )

    def btn_click(self, event=None):
        """似顔絵ボタンを押したとき

        ・似顔絵ボタンを押したときに画像イメージを似顔絵フレームに
        貼り付ける。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        fTyp = [(u"gif画像", ".gif")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        self.filepath = filedialog.askopenfilename(
            filetypes=fTyp,
            initialdir=iDir
        )
        if not self.filepath == "":
            path, ___ = os.path.splitext(os.path.basename(self.now_path))
            ____, ext = os.path.splitext(os.path.basename(self.filepath))
            title = shutil.copyfile(
                self.filepath,
                "./{0}/{1}{2}".format(
                    tree_folder[0][0],
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
        files = "./{0}/{1}.gif".format(
            tree_folder[0][0],
            self.select_list_item
        )
        if os.path.isfile(files):
            os.remove(files)
            self.cv.delete("all")

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
            self.cv.photo = ImageTk.PhotoImage(self.resize_gif(giffile))
            giffile.close()
            self.cv.itemconfig(self.image_on_canvas, image=self.cv.photo)

    def create_tags(self):
        """タグの作成

        ・キャラクターの名前をJanomeの形態素解析にかかるようにする。
        キャラクターの名前を色付きにする。

        """
        i = 0
        system_dic = u"喜寛,固有名詞,ヨシヒロ"
        # キャラクターから一覧を作る。
        children = self.tree.get_children('data/character')
        for child in children:
            # ユーザー定義辞書の設定
            reading = ""
            childname = self.tree.item(child, "text")
            for token in tokenizer.tokenize(childname):
                reading += token.phonetic
            system_dic += u"\n{0},固有名詞,{1}".format(childname, reading)
            # タグの作成
            self.text.tag_configure(
                childname,
                foreground=color[i % len(color)],
                font=(self.font, self.int_var, "bold")
            )
            i += 1
        f = open("./userdic.csv", 'w', encoding='utf-8')
        f.write(system_dic)
        f.close()
        # Janomeを使って日本語の形態素解析
        self.t = Tokenizer(
            "./userdic.csv",
            udic_type="simpledic",
            udic_enc="utf8"
        )

    def all_highlight(self, event=None):
        """全てハイライト

        ・開く処理等の時にすべての行をハイライトする。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        # 全てのテキストを取得
        src = self.text.get('1.0', 'end - 1c')
        # 全てのハイライトを一度解除する
        for tag in self.text.tag_names():
            self.text.tag_remove(tag, '1.0', 'end')

        # ハイライトする
        self._highlight('1.0', src, 'end')

    def line_highlight(self, event=None):
        """現在行だけハイライト

        ・入力等の変更時に現在の行のみをハイライトする。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        start = 'insert linestart'
        end = 'insert lineend'
        # 現在行のテキストを取得
        src = self.text.get(start, end)
        # その行のハイライトを一度解除する
        for tag in self.text.tag_names():
            self.text.tag_remove(tag, start, end)

        # ハイライトする
        self._highlight(start, src, end)
        # 置換処理時に選択する
        if self.replacement_dialog == 1:
            start = self.next_pos
            end = '{0} + {1}c'.format(self.next_pos, len(self.last_text))
            self.text.tag_add('sel', start, end)

    def _highlight(self, start, src, end):
        """ハイライトの共通処理

        ・ハイライトする文字が見つかったらハイライト処理をする。
        先頭の文字が全角スペースならば、一文字ずらしてハイライトする。

        """
        self.create_tags()
        self.text.mark_set('range_start', start)
        space_count = re.match(r"\u3000*", self.text.get(start, end)).end()
        # 形態素解析を行う
        for token in self.t.tokenize(src):
            content = token.surface
            self.text.mark_set(
                'range_end', 'range_start+{0}c'
                .format(len(content))
            )
            # 全角スペースの時はずらす
            if space_count > 0:
                self.text.tag_add(
                    content,
                    'range_start+{0}c'.format(space_count),
                    'range_end+{0}c'.format(space_count)
                )
            else:
                self.text.tag_add(content, 'range_start', 'range_end')
            self.text.mark_set('range_start', 'range_end')

    def font_dialog(self, event=None):
        """フォントサイズダイアログを作成

        ・フォントサイズダイアログを作成し表示する。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        self.sub_wins = tk.Toplevel(self)
        self.intSpin = ttk.Spinbox(self.sub_wins, from_=12, to=72)
        self.intSpin.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=5,
            pady=5,
            sticky=tk.W+tk.E,
            ipady=3
        )
        button = ttk.Button(
            self.sub_wins,
            text=u'サイズ変更',
            width=str(u'サイズ変更'),
            padding=(10, 5),
            command=self.font_size_Change
        )
        button.grid(row=1, column=1)
        self.intSpin.set(self.int_var)
        self.sub_wins.title(u'フォントサイズの変更')

    def font_size_Change(self):
        """フォントのサイズを変える

        ・サイズ変更を押されたときにサイズを変更する。
        上は72ptまで下は12ptまでにする。

        """
        # 比較のため数値列に変更
        self.int_var = int(self.intSpin.get())
        if self.int_var < 12:  # 12より下の値を入力した時、12にする
            self.int_var = 12
        elif 72 < self.int_var:  # 72より上の値を入力した時、72にする
            self.int_var = 72
        # 文字列にもどす
        self.int_var = str(self.int_var)
        self.sub_wins.destroy()
        # フォントサイズの変更
        self.text.configure(font=(self.font, self.int_var))
        # ハイライトのやり直し
        self.all_highlight()

    def open_url(self, event=None):
        """小説家になろうのユーザーページを開く

        ・インターネットブラウザで小説家になろうのユーザーページを開く。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        webbrowser.open("https://syosetu.com/user/top/")

    def find_dictionaly(self, event=None):
        """意味を検索

        ・Wikipedia-APIライブラリを使ってWikipediaから選択文字の意味を
        検索する。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        # wikipediaから
        select_text = self.text.selection_get()
        page_py = wiki_wiki.page(select_text)
        # ページがあるかどうか判断
        if page_py.exists():
            messagebox.showinfo(
                "「{0}」の意味".format(select_text),
                page_py.summary
            )
        else:
            messagebox.showwarning(
                "「{0}」の意味".format(select_text),
                u"見つけられませんでした。"
            )

    def open_help(self, event=None):
        """helpページを開く

        ・ウエブブラウザを使ってREADME.htmlを表示する。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        webbrowser.open(
            'file://' + os.path.dirname(
                os.path.abspath(os.path.dirname(__file__))
            )
            + "/README.html"
        )

    def open_version(self, event=None):
        """バージョン情報を表示

        ・バージョン情報表示ダイアログを表示する。
        ×を押すまで消えないようにする。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        img2 = tk.PhotoImage(data=datas)
        window = tk.Toplevel(root)
        self.pack()
        self.canvas = tk.Canvas(window, width=600, height=300)
        self.canvas.create_image(0, 0, anchor='nw', image=img2)
        self.canvas.create_text(
            550,
            290,
            anchor='se',
            text='Copyright (C) 2019-2020 Yamahara Yoshihiro',
            font=('', 12)
        )
        self.canvas.create_text(
            420,
            120,
            anchor='nw',
            text='Ver 0.6.0 Beta',
            font=('', 12)
        )
        self.canvas.pack()
        window.resizable(width=0, height=0)
        window.mainloop()

    def read_text(self, event=None):
        """テキストを読み上げる

        ・pyttsx3ライブラリを使ってテキストボックスに書かれているものを読み上げる。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        self.text.focus()
        self.read_texts = True
        self.engine = pyttsx3.init()
        self.engine.connect('started-word', self.pyttsx3_onword)
        self.engine.connect('finished-utterance', self.pyttsx3_onend)
        self.engine.setProperty('rate', 150)
        self.engine.say(self.text.get('1.0', 'end - 1c'))
        self.i = 0
        self.textlen = 0
        self.engine.startLoop(False)
        self.externalLoop()

    def externalLoop(self):
        """文章読み上げ繰り返し処理

        ・文章読み上げを繰り返し続ける。

        """
        self.engine.iterate()

    def pyttsx3_onword(self, name, location, length):
        """文章を読み上げ中の処理

        ・文章読み始めるときに止めるダイアログを出してから読み上げる。
        読み上げている最中は読み上げている行を選択状態にする。

        Args:
            name (str): 読み上げに関連付けられた名前
            location (int): 現在の場所
            length (int): 不明

        """
        # 今読んでいる場所と選択位置を比較する
        if location > self.textlen:
            # すべての選択一度解除する
            self.text.tag_remove('sel', '1.0', 'end')
            # 現在読んでいる場所を選択する
            self.text.tag_add(
                'sel',
                "{0}.0".format(self.i),
                "{0}.0".format(self.i+1)
            )
            # 次の行の長さをtextlenに入力する
            self.textlen += len(
                self.text.get(
                    '{0}.0'.format(self.i),
                    '{0}.0'.format(self.i+1)
                )
            )
            # カーソルを文章の一番後ろに持ってくる
            self.text.mark_set('insert', '{0}.0'.format(self.i+1))
            self.text.see('insert')
            self.text.focus()
            # 行を１行増やす
            self.i += 1
        # 読み初めての処理
        if self.read_texts:
            # 読むのを中止するウインドウを作成する
            self.sub_read_win = tk.Toplevel(self)
            button = ttk.Button(
                self.sub_read_win,
                text=u'中止する',
                width=str(u'中止する'),
                padding=(100, 5),
                command=self.pyttsx3_onreadend
            )
            button.grid(row=1, column=1)
            # 最前面に表示し続ける
            self.sub_read_win.attributes("-topmost", True)
            # サイズ変更禁止
            self.sub_read_win.resizable(width=0, height=0)
            self.sub_read_win.title(u'読み上げ')
            self.read_texts = False

    def pyttsx3_onreadend(self):
        """中止するボタンを押したときの処理

        ・中止ボタンを押したときに読み上げをやめ、中止ウインドウ
        を削除する。

        """
        self.engine.stop()
        self.engine.endLoop()
        self.sub_read_win.destroy()
        self.text.tag_remove('sel', '1.0', 'end')

    def pyttsx3_onend(self, name, completed):
        """文章を読み終えた時の処理

        ・文章を読み終えたら中止ウインドウを削除する。

        Args:
            name (str): 読み上げに関連付けられた名前
            completed (bool): 文章が読み上げ終わった(True)

        """
        self.engine.stop()
        self.engine.endLoop()
        self.sub_read_win.destroy()
        self.text.tag_remove('sel', '1.0', 'end')

    def is_hiragana(self, char):
        """文字がひらがなか判断

        ・与えられた文字がひらがなかどうか判断する。

        Args:
            char (str): 判断する文字

        Returns:
            bool: ひらがなならTrue、違うならFalse

        """
        return (0x3040 < ord(char) < 0x3097)

    def ruby(self, event=None):
        """ルビをふる

        ・選択文字列に小説家になろうのルビを振る。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        hon = ""
        # 選択文字列を切り取る
        set_ruby = self.text.get('sel.first', 'sel.last')
        # 選択文字列を削除する
        self.text.delete('sel.first', 'sel.last')
        # 形態素解析を行う
        for token in tokenizer.tokenize(set_ruby):
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
        self.text.insert('insert', hon)

    def redo(self, event=None):
        """Redo

        ・Redo処理を行う。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        self.text.edit_redo()

    def undo(self, event=None):
        """Undo

        ・Uedo処理を行う。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        self.text.edit_undo()

    def copy(self, event=None):
        """Copy

        ・Copy処理を行う。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        self.clipboard_clear()
        self.clipboard_append(self.text.selection_get())

    def cut(self, event=None):
        """Cut

        ・Cut処理を行う。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        self.copy()
        self.text.delete("sel.first", "sel.last")

    def paste(self, event=None):
        """Paste

        ・Paste処理を行う。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        self.text.insert('insert', self.clipboard_get())

    def moji_count(self, event=None):
        """文字数と行数を表示する

        ・文字数と行数をカウントして表示する。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        # 行数の取得
        new_line = int(self.text.index('end-1c').split('.')[0])
        # 文字列の取得
        moji = self.text.get('1.0', 'end')
        # ２０文字で区切ったときの行数を数える
        gen_mai = 0
        for val in moji.splitlines():
            gen_mai += len(textwrap.wrap(val, 20))
        # メッセージボックスの表示
        messagebox.showinfo(
            u"文字数と行数、原稿用紙枚数", "文字数 :{0}文字　行数 : {1}行"
            u"\n 原稿用紙 : {2}枚".format(
                len(moji)-new_line,
                new_line,
                -(-gen_mai//20)))

    def new_file(self):
        """新規作成をするための準備

        ・ファイルの新規作成をするための準備処理をおこなう。

        """
        self.initialize()
        for val in tree_folder:
            self.tree.delete(val[0])

        # ツリービューを表示する
        self.tree_get_loop()
        self.frame()
        self.winfo_toplevel().title(u"小説エディタ")
        # テキストを読み取り専用にする
        self.text.configure(state='disabled')
        # テキストにフォーカスを当てる
        self.text.focus()

    def new_open(self, event=None):
        """新規作成

        ・変更があれば、ファイル保存するか尋ねて、新規作成する。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        if not self.text.get('1.0', 'end - 1c') == self.text_text:
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

    def overwrite_save_file(self, event=None):
        """上書き保存処理

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
        """ファイルを保存処理

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
            self.file_path, ___ = os.path.splitext(filepath)
            # 上書き保存処理
            self.overwrite_save_file()

    def open_file(self, event=None):
        """ファイルを開く処理

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
            self.initialize()
            # ファイルを開いてdataフォルダに入れる
            with zipfile.ZipFile(filepath) as existing_zip:
                existing_zip.extractall('./data')
            # ツリービューを削除する
            for val in tree_folder:
                self.tree.delete(val[0])

            # ツリービューを表示する
            self.tree_get_loop()
            # ファイルパスを拡張子抜きで表示する
            filepath, ___ = os.path.splitext(filepath)
            self.file_path = filepath
            self.now_path = ""
            # テキストビューを新にする
            self.frame()

    def tree_get_loop(self):
        """ツリービューに挿入

        ・保存データからファイルを取得してツリービューに挿入する。

        """
        for val in tree_folder:
            self.tree.insert('', 'end', val[0], text=val[1])
            # フォルダのファイルを取得
            path = "./{0}".format(val[0])
            files = os.listdir(path)
            for filename in files:
                if os.path.splitext(filename)[1] == ".txt":
                    self.tree.insert(
                        val[0],
                        'end',
                        text=os.path.splitext(filename)[0]
                    )

    def find_dialog(self, event=None):
        """検索ダイアログを作成

        ・検索ダイアログを作成する。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        search_win = tk.Toplevel(self)
        self.text_var = ttk.Entry(search_win, width=40)
        self.text_var.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=5,
            pady=5,
            sticky=tk.W+tk.E,
            ipady=3
        )
        button = ttk.Button(
            search_win,
            text=u'検索',
            width=str(u'検索'),
            padding=(10, 5),
            command=self.search
        )
        button.grid(row=1, column=0)
        button2 = ttk.Button(
            search_win,
            text=u'昇順検索',
            width=str(u'昇順検索'),
            padding=(10, 5),
            command=self.search_forward
        )
        button2.grid(row=1, column=1)
        # 最前面に表示し続ける
        search_win.attributes("-topmost", True)
        search_win.title(u'検索')
        self.text_var.focus()

    def replacement_dialog(self, event=None):
        """置換ダイアログを作成

        ・置換ダイアログを作成する。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        self.replacement_win = tk.Toplevel(self)
        self.text_var = ttk.Entry(self.replacement_win, width=40)
        self.text_var.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=5,
            pady=5,
            sticky=tk.W+tk.E,
            ipady=3
        )
        self.replacement_var = ttk.Entry(self.replacement_win, width=40)
        self.replacement_var.grid(
            row=1,
            column=0,
            columnspan=2,
            padx=5,
            pady=5,
            sticky=tk.W+tk.E,
            ipady=3
        )
        button = ttk.Button(
            self.replacement_win,
            text=u'検索',
            width=str(u'検索'),
            padding=(10, 5),
            command=self.search
        )
        button.grid(row=2, column=0)
        button2 = ttk.Button(
            self.replacement_win,
            text=u'置換',
            width=str(u'置換'),
            padding=(10, 5),
            command=self.replacement
        )
        button2.grid(row=2, column=1)
        # 最前面に表示し続ける
        self.replacement_win.attributes("-topmost", True)
        self.replacement_win.title(u'置換')
        self.text_var.focus()
        # ウインドウが閉じられたときの処理
        self.replacement_win.protocol(
            "WM_DELETE_WINDOW",
            self.replacement_dialog_on_closing
            )

    def replacement_dialog_on_closing(self):
        """検索ウインドウが閉じられたときの処理

        ・検索ダイアログが閉じられたことがわかるようにする。

        """
        self.replacement_dialog = 0
        self.replacement_win.destroy()

    def search(self, event=None):
        """検索処理

        ・検索処理をする。空欄なら処理しない、違うなら最初から、
        同じなら次のを検索する。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        # 現在選択中の部分を解除
        self.text.tag_remove('sel', '1.0', 'end')

        # 現在検索ボックスに入力されてる文字
        now_text = self.text_var.get()
        if not now_text:
            # 空欄だったら処理しない
            pass
        elif now_text != self.last_text:
            # 前回の入力と違う文字なら、検索を最初から行う
            index = '0.0'
            self.search_next(now_text, index, 0)
        else:
            # 前回の入力と同じなら、検索の続きを行う
            self.search_next(now_text, self.next_pos, 1)

        # 今回の入力を、「前回入力文字」にする
        self.last_text = now_text

    def replacement(self, event=None):
        """置換処理

        ・置換処理をする。空欄なら処理しない、違うなら初めから、
        同じなら次を検索する。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        # 現在選択中の部分を解除
        self.text.tag_remove('sel', '1.0', 'end')

        # 現在検索ボックスに入力されてる文字
        now_text = self.text_var.get()
        replacement_text = self.replacement_var.get()
        if not now_text or not replacement_text:
            # 空欄だったら処理しない
            pass
        elif now_text != self.last_text:
            # 前回の入力と違う文字なら、検索を最初から行う
            self.replacement_dialog = 1
            index = '0.0'
            self.search_next(now_text, index, 0)
        else:
            # 前回の入力と同じなら、検索の続きを行う
            self.replacement_dialog = 1
            # 検索文字の置換を行なう
            start = self.next_pos
            end = '{0} + {1}c'.format(self.next_pos, len(now_text))
            self.text.delete(start, end)
            self.text.insert(start, replacement_text)
            self.search_next(now_text, self.next_pos, 1)

        # 今回の入力を、「前回入力文字」にする
        self.last_text = now_text

    def search_forward(self, event=None):
        """昇順検索処理

        ・昇順検索をする。空欄なら処理しない、違うなら初めから、
        同じなら次を検索する。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        # 現在選択中の部分を解除
        self.text.tag_remove('sel', '1.0', 'end')

        # 現在検索ボックスに入力されてる文字
        now_text = self.text_var.get()
        if not now_text:
            # 空欄だったら処理しない
            pass
        elif now_text != self.last_text:
            # 前回の入力と違う文字なら、検索を最初から行う
            index = 'end'
            self.search_next(now_text, index, 2)
        else:
            # 前回の入力と同じなら、検索の続きを行う
            self.search_next(now_text, self.next_pos, 2)

        # 今回の入力を、「前回入力文字」にする
        self.last_text = now_text

    def search_next(self, search, index, case):
        """検索のメイン処理

        ・検索できれば選択をする。できなければ、ダイアログを出して終了。

        Args:
            search (str): 検索文字列
            index (str): 検索位置 ex. (1.0)
            case (int): 0.初めから検索 1.次に検索 2.昇順検索

        """
        if case == 2:
            backwards = True
            stopindex = '0.0'
            index = '{0}'.format(index)
        elif case == 0:
            backwards = False
            stopindex = 'end'
            index = '{0}'.format(index)
        else:
            backwards = False
            stopindex = 'end'
            index = '{0} + 1c'.format(index)

        pos = self.text.search(
            search, index,
            stopindex=stopindex,
            backwards=backwards
        )
        if not pos:
            if case == 2:
                index = "end"
            else:
                index = "0.0"

            pos = self.text.search(
                search, index,
                stopindex=stopindex,
                backwards=backwards
            )
            if not pos:
                messagebox.showinfo(
                    "検索",
                    "最後まで検索しましたが検索文字はありませんでした。"
                )
                self.replacement_dialog = 0
                return

        self.next_pos = pos
        start = pos
        end = '{0} + {1}c'.format(pos, len(search))
        self.text.tag_add('sel', start, end)
        self.text.mark_set('insert', start)
        self.text.see('insert')
        self.text.focus()

    def message_window(self, event=None):
        """ツリービューを右クリックしたときの処理

        ・子アイテムならば削除ダイアログを表示する。
        親アイテムならば追加を行う。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        curItem = self.tree.focus()              # 選択アイテムの認識番号取得
        parentItem = self.tree.parent(curItem)   # 親アイテムの認識番号取得
        # 親アイテムをクリックしたとき
        if self.tree.item(curItem)["text"] == tree_folder[4][1]:
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
                path = "./{0}/{1}.gif".format(tree_folder[4][0], file_name)
                shutil.copy2(filepath, path)
                self.frame_image()
                path = "./{0}/{1}.txt".format(tree_folder[4][0], file_name)
                tree = self.tree.insert(
                    tree_folder[4][0],
                    'end',
                    text=file_name
                )
                self.tree.see(tree)
                self.tree.selection_set(tree)
                self.tree.focus(tree)
                self.select_list_item = file_name
                self.now_path = path
                f = open(path, 'w', encoding='utf-8')
                self.zoom = 100
                f.write(str(self.zoom))
                f.close()
                self.frame_image()
                self.path_read_image(
                    tree_folder[4][0],
                    file_name,
                    0
                )

        else:
            if str(
                self.tree.item(curItem)["text"]
            ) and (not str(
                    self.tree.item(parentItem)["text"]
                )
            ):
                # サブダイヤログを表示する
                title = u'{0}に挿入'.format(self.tree.item(curItem)["text"])
                dialog = Mydialog(self, "挿入", True, title, False)
                root.wait_window(dialog.sub_name_win)
                file_name = dialog.txt
                del dialog
                if not file_name == "":
                    self.open_file_save(self.now_path)
                    curItem = self.tree.focus()              # 選択アイテムの認識番号取得
                    text = self.tree.item(curItem)["text"]
                    path = ""
                    # 選択されているフォルダを見つける
                    for val in tree_folder:
                        if text == val[1]:
                            if val[0] == tree_folder[0][0]:
                                self.frame_character()
                                self.txt_yobi_name.insert(tk.END, file_name)
                            else:
                                self.frame()

                            path = "./{0}/{1}.txt".format(val[0], file_name)
                            tree = self.tree.insert(
                                val[0],
                                'end',
                                text=file_name
                            )
                            self.now_path = path
                            break

                    # パスが存在すれば新規作成する
                    if not path == "":
                        f = open(path, 'w', encoding='utf-8')
                        f.write("")
                        f.close()
                        # ツリービューを選択状態にする
                        self.tree.see(tree)
                        self.tree.selection_set(tree)
                        self.tree.focus(tree)
                        self.select_list_item = file_name
                        self.winfo_toplevel().title(
                            u"小説エディタ\\{0}\\{1}"
                            .format(text, file_name)
                        )
                        self.text.focus()
                        # テキストを読み取り専用を解除する
                        self.text.configure(state='normal')
                        self.create_tags()
            # 子アイテムを右クリックしたとき
            else:
                if str(self.tree.item(curItem)["text"]):
                    # 項目を削除する
                    file_name = self.tree.item(curItem)["text"]
                    text = self.tree.item(parentItem)["text"]
                    # ＯＫ、キャンセルダイアログを表示し、ＯＫを押したとき
                    if messagebox.askokcancel(
                        u"項目削除",
                        "{0}を削除しますか？".format(file_name)
                    ):
                        # パスを取得する
                        for val in tree_folder:
                            if text == val[1]:
                                path = "./{0}/{1}.txt".format(
                                    val[0],
                                    file_name
                                )
                                image_path = "./{0}/{1}.gif".format(
                                    val[0],
                                    file_name
                                )
                                self.tree.delete(curItem)
                                self.now_path = ""
                                break
                        # imageパスが存在したとき
                        if os.path.isfile(image_path):
                            os.remove(image_path)

                        # パスが存在したとき
                        if not path == "":
                            os.remove(path)
                            self.frame()
                            self.text.focus()

    def save_charactor_file(self):
        """キャラクターファイルの保存準備

        ・それぞれの項目をxml形式で保存する。

        """
        return '<?xml version="1.0"?>\n<data>\n\t<call>{0}</call>\
        \n\t<name>{1}</name>\n\t<sex>{2}</sex>\n\t<birthday>{3}</birthday>\
        \n\t<body>{4}</body>\n</data>'.format(
            self.txt_yobi_name.get(),
            self.txt_name.get(),
            self.var.get(),
            self.txt_birthday.get(),
            self.text_body.get(
                '1.0',
                'end -1c'
            )
        )

    def open_file_save(self, path):
        """開いてるファイルを保存する

        ・開いてるファイルをそれぞれの保存形式で保存する。

        Args:
            path (str): 保存ファイルのパス

        """
        # 編集ファイルを保存する
        if not path == "":
            f = open(path, 'w', encoding='utf-8')
            if not path.find(tree_folder[0][0]) == -1:
                f.write(self.save_charactor_file())
                self.charactor_file = ""
            elif not path.find(tree_folder[4][0]) == -1:
                f.write(str(self.zoom))
            else:
                f.write(self.text.get("1.0", tk.END+'-1c'))

            f.close()
            self.now_path = path

    def on_double_click(self, event=None):
        """ツリービューをダブルクリック

        ・ファイルを保存して閉じて、選択されたアイテムを表示する。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        curItem = self.tree.focus()              # 選択アイテムの認識番号取得
        parentItem = self.tree.parent(curItem)   # 親アイテムの認識番号取得
        text = self.tree.item(parentItem)["text"]
        # 開いているファイルを保存
        self.open_file_save(self.now_path)
        # テキストを読み取り専用を解除する
        self.frame()
        self.text.configure(state='disabled')
        # 条件によって分離
        self.select_list_item = self.tree.item(curItem)["text"]
        path = ""
        for val in tree_folder:
            if text == val[1]:
                if val[0] == tree_folder[4][0]:
                    path = "./{0}/{1}.txt".format(
                        val[0],
                        self.select_list_item
                    )
                    f = open(path, 'r', encoding='utf-8')
                    zoom = f.read()
                    self.zoom = int(zoom)
                    self.now_path = path
                    self.frame_image()
                    self.path_read_image(
                        tree_folder[4][0],
                        self.select_list_item,
                        self.zoom
                    )
                else:
                    path = "./{0}/{1}.txt".format(
                        val[0],
                        self.select_list_item
                    )
                    self.now_path = path
                    if val[0] == tree_folder[0][0]:
                        self.frame_character()
                    else:
                        # テキストを読み取り専用を解除する
                        self.text.configure(state='normal')
                        self.text.focus()

                    self.path_read_text(text, self.select_list_item)

                return

        self.now_path = ""
        self.winfo_toplevel().title(u"小説エディタ")

    def path_read_image(self, image_path, image_name, scale):
        """イメージを読み込んで表示

        ・パスが存在すればイメージファイルを読み込んで表示する。

        Args:
            image_path (str): イメージファイルの相対パス
            image_name (str): イメージファイルの名前
            scale (int): 拡大率(%)

        """
        if not self.now_path == "":
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

            self.image_space.photo = ImageTk.PhotoImage(giffile)
            self.image_space.itemconfig(
                self.image_on_space,
                image=self.image_space.photo
            )
            # イメージサイズにキャンバスサイズを合わす
            self.image_space.config(
                scrollregion=(
                    0,
                    0,
                    giffile.size[0],
                    giffile.size[1]
                )
            )
            giffile.close()

        self.winfo_toplevel().title(
                u"小説エディタ\\{0}\\{1}".format(tree_folder[4][1], image_name)
            )

    def path_read_text(self, text_path, text_name):
        """テキストを読み込んで表示

        ・パスが存在すればテキストを読み込んで表示する。

        Args:
            text_path (str): テキストファイルの相対パス
            text_name (str): テキストファイルの名前

        """
        if not self.now_path == "":
            if not self.now_path.find(tree_folder[0][0]) == -1:
                self.txt_yobi_name.delete('0', tk.END)
                self.txt_name.delete('0', tk.END)
                self.txt_birthday.delete('0', tk.END)
                self.text_body.delete('1.0', tk.END)
                tree = ET.parse(self.now_path)
                elem = tree.getroot()
                self.txt_yobi_name.insert(tk.END, elem.findtext("call"))
                self.txt_name.insert(tk.END, elem.findtext("name"))
                self.var.set(elem.findtext("sex"))
                self.txt_birthday.insert(tk.END, elem.findtext("birthday"))
                self.text_body.insert(tk.END, elem.findtext("body"))
                title = "{0}/{1}.gif".format(
                    tree_folder[0][0],
                    elem.findtext("call")
                )
                if os.path.isfile(title):
                    self.print_gif(title)
            else:
                self.text.delete('1.0', tk.END)
                f = open(self.now_path, 'r', encoding='utf-8')
                self.text_text = f.read()
                self.text.insert(tk.END, self.text_text)
                f.close()

            self.winfo_toplevel().title(
                u"小説エディタ\\{0}\\{1}".format(text_path, text_name)
            )
            # シンタックスハイライトをする
            self.all_highlight()

    def on_name_click(self, event=None):
        """名前の変更

        ・リストボックスの名前を変更する。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        curItem = self.tree.focus()              # 選択アイテムの認識番号取得
        parentItem = self.tree.parent(curItem)   # 親アイテムの認識番号取得
        text = self.tree.item(parentItem)["text"]
        if not text == "":
            sub_text = self.tree.item(curItem)["text"]
            title = u'{0}の名前を変更'.format(sub_text)
            dialog2 = Mydialog(self, u"変更", True, title, sub_text)
            root.wait_window(dialog2.sub_name_win)
            # テキストを読み取り専用を解除する
            self.text.configure(state='normal')
            co_text = dialog2.txt
            del dialog2
            for val in tree_folder:
                if text == val[1]:
                    path1 = "./{0}/{1}.txt".format(val[0], sub_text)
                    path2 = "./{0}/{1}.txt".format(val[0], co_text)
                    self.now_path = path2
                    # テキストの名前を変更する
                    os.rename(path1, path2)
                    self.tree.delete(curItem)
                    Item = self.tree.insert(parentItem, 'end', text=co_text)
                    self.tree.selection_set(Item)
                    self.path_read_text(val[0], co_text)
                    return

    def update_line_numbers(self, event=None):
        """行番号の描画

        ・行番号をつけて表示する。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        # 現在の行番号を全て消す
        self.line_numbers.delete(tk.ALL)

        # Textの0, 0座標、つまり一番左上が何行目にあたるかを取得
        i = self.text.index("@0,0")
        while True:
            # dlineinfoは、その行がどの位置にあり、どんなサイズか、を返す
            # (3, 705, 197, 13, 18) のように帰る(x,y,width,height,baseline)
            dline = self.text.dlineinfo(i)
            # dlineinfoに、存在しない行や、スクロールしないと見えない行を渡すとNoneが帰る
            if dline is None:
                break
            else:
                y = dline[1]  # y座標を取得

            # (x座標, y座標, 方向, 表示テキスト)を渡して行番号のテキストを作成
            linenum = str(i).split(".")[0]
            self.line_numbers.create_text(
                3,
                y,
                anchor=tk.NW,
                text=linenum,
                font=("", 12)
            )
            i = self.text.index("%s+1line" % i)

    def change_setting(self, event=None):
        """テキストの変更時

        ・テキストを変更したときに行番号とハイライトを変更する。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        self.update_line_numbers()
        # その行のハイライトを行う
        self.line_highlight()

    def tab(self, event=None):
        """タブ押下時の処理

        ・タブキーを押したときに補完リストを出す。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        # 文字を選択していないとき
        sel_range = self.text.tag_ranges('sel')
        if not sel_range:
            return self.auto_complete()
        else:
            return

    def auto_complete(self):
        """補完リストの設定

        ・補完リストの設定をする。

        """
        auto_complete_list = tk.Listbox(self.text)
        # エンターでそのキーワードを選択
        auto_complete_list.bind('<Return>', self.selection)
        auto_complete_list.bind('<Double-1>', self.selection)
        # エスケープ、タブ、他の場所をクリックで補完リスト削除
        auto_complete_list.bind('<Escape>', self.remove_list)
        auto_complete_list.bind('<Tab>', self.remove_list)
        auto_complete_list.bind('<FocusOut>', self.remove_list)
        # (x,y,width,height,baseline)
        x, y, width, height, _ = self.text.dlineinfo(
            'insert'
        )
        # 現在のカーソル位置のすぐ下に補完リストを貼る
        auto_complete_list.place(x=x+width, y=y+height)
        # 補完リストの候補を作成
        for word in self.get_keywords():
            auto_complete_list.insert(tk.END, word)

        # 補完リストをフォーカスし、0番目を選択している状態に
        auto_complete_list.focus_set()
        auto_complete_list.selection_set(0)
        self.auto_complete_list = auto_complete_list  # self.でアクセスできるように
        return 'break'

    def get_keywords(self):
        """補完リストの候補キーワードを作成

        ・補完リストに表示するキーワードを得る。

        """
        text = ''
        text, _, _ = self.get_current_insert_word()
        my_func_and_class = set()
        # コード補完リストをTreeviewにある'名前'から得る
        children = self.tree.get_children('data/character')
        for child in children:
            childname = self.tree.item(child, "text")
            # 前列の文字列と同じものを選び出す
            if childname.startswith(text) or childname.startswith(
                text.title()
            ):
                my_func_and_class.add(childname)

        result = list(my_func_and_class)
        return result

    def remove_list(self, event=None):
        """補完リストの削除処理

        ・補完リストを削除し、テキストボックスにフォーカスを戻す。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        self.auto_complete_list.destroy()
        self.text.focus()  # テキストウィジェットにフォーカスを戻す

    def selection(self, event=None):
        """補完リストでの選択後の処理

        ・補完リストを選択したときにその文字を入力する。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        # リストの選択位置を取得
        select_index = self.auto_complete_list.curselection()
        if select_index:
            # リストの表示名を取得
            value = self.auto_complete_list.get(select_index)

            # 現在入力中の単語位置の取得
            _, start, end = self.get_current_insert_word()
            self.text.delete(start, end)
            self.text.insert('insert', value)
            self.remove_list()

    def get_current_insert_word(self):
        """現在入力中の単語と位置を取得

        ・現在入力している単語とその位置を取得する。

        """
        text = ''
        start_i = 1
        end_i = 0
        while True:
            start = 'insert-{0}c'.format(start_i)
            end = 'insert-{0}c'.format(end_i)
            text = self.text.get(start, end)
            # 1文字ずつ見て、スペース、改行、タブ、空文字、句読点にぶつかったら終わり
            if text in (' ', '　', '\t', '\n', '', '、', '。'):
                text = self.text.get(end, 'insert')

                # 最終単語を取得する
                pri = [token.surface for token in tokenizer.tokenize(text)]
                hin = [
                    token.part_of_speech.split(',')[0] for token
                    in tokenizer.tokenize(text)
                ]
                if len(pri) > 0:
                    if hin[len(pri)-1] == u'名詞':
                        text = pri[len(pri)-1]
                    else:
                        text = ""
                else:
                    text = ""

                end = 'insert-{0}c'.format(len(text))
                return text, end, 'insert'

            start_i += 1
            end_i += 1

    def yahoocall(self, appid="", sentence=""):
        """yahooの校正支援を呼び出す

        ・Yahoo! 校正支援をClient IDを使って呼び出す。

        Args:
            appid (str): Yahoo! Client ID
            sentence (str): 校正をしたい文字列

        Returns:
            str: 校正結果

        """
        if appid == "":
            messagebox.showerror(
                "Yahoo! Client ID",
                u"Yahoo! Client IDが見つかりません。\n"
                "Readme.pdfを読んで、設定し直してください。"
            )
            return
        url = "https://jlp.yahooapis.jp/KouseiService/V1/kousei"
        data = {
            "appid": appid.rstrip('\n'),
            "sentence": sentence,
        }
        html = requests.post(url, data)
        return html.text

    def yahooresult(self, html):
        """校正支援を表示する画面を制作

        ・校正結果を表示するダイアログを作成する。

        Args:
            html (str): 校正結果

        """
        xml = ET.fromstring(html)
        # サブウインドウの表示
        sub_win = tk.Toplevel(self)
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
        self.yahoo_tree.heading(1, text="先頭からの文字数")
        self.yahoo_tree.heading(2, text="対象文字数")
        self.yahoo_tree.heading(3, text="対象表記")
        self.yahoo_tree.heading(4, text="言い換え候補文字列")
        self.yahoo_tree.heading(5, text="指摘の詳細情報")
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
        sub_win.title(u'文章校正')

    def yahoo(self, event=None):
        """Yahoo! 校正支援

        ・Yahoo! 校正支援を呼び出し表示する。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        html = self.yahoocall(
            self.APPID,
            self.text.get('1.0', 'end -1c')
        )
        if not self.APPID == "":
            self.yahooresult(html)
            self.yahoo_tree.bind("<Double-1>", self.on_double_click_yahoo)

    def on_double_click_yahoo(self, event=None):
        """Yahoo! 校正支援リストをダブルクリック

        ・Yahoo! 校正支援ダイアログのリストをダブルクリックすると
        その該当箇所を選択する。

        Args:
            event (instance): tkinter.Event のインスタンス

        """
        curItem = self.yahoo_tree.focus()
        value = self.yahoo_tree.item(curItem)
        i = 0
        textlen = 0
        textforlen = 0
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
                    self.text.get(
                        '{0}.0'.format(i),
                        '{0}.0'.format(i+1)
                    )
                )
            else:
                break
        if i == 0:
            i = 1
        # 選択状態を一旦削除
        self.text.tag_remove('sel', '1.0', 'end')
        # 選択状態にする
        self.text.tag_add(
            'sel',
            "{0}.{1}".format(i, val-textforlen),
            "{0}.{1}".format(i, val-textforlen+lenge)
        )
        # カーソルの移動
        self.text.mark_set('insert', '{0}.{1}'.format(i, val-textforlen))
        self.text.see('insert')
        # フォーカスを合わせる
        self.text.focus()
        return


def on_closing():
    """終了時の処理

    ・ソフトを閉じるか確認してから閉じる。

    """
    if messagebox.askokcancel(u"小説エディタ", u"終了してもいいですか？"):
        shutil.rmtree("./data")
        if os.path.isfile("./userdic.csv"):
            os.remove("./userdic.csv")

        root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    if os.path.isdir("./data"):
        messagebox.showerror(u"小説エディタ", u"二重起動はできません")
        sys.exit()

    # タイトル横の画像ファイルのbase 64データ
    data = '''R0lGODlhgACAAPcAAAAAAAQEBAcHBwkJCQoKCg8PDxAQEBERERMTExUVFRgYGBkZ
        GRoaGhwcHB0dHR4eHh8fHyAgICEhISIiIiMjIyQkJCUlJSYmJicnJygoKCkpKSoq
        KisrKywsLC0tLS4uLi8vLzAwMDExMTIyMjMzMzQ0NDU1NTc3Nzg4ODo6Ojs7Ozw8
        PD4+Pj8/P0BAQEFBQUJCQkNDQ0REREVFRUZGRkdHR0hISElJSUpKSktLS0xMTE1N
        TU5OTk9PT1BQUFJSUlNTU1RUVFVVVVZWVldXV1lZWVpaWltbW1xcXF1dXV5eXl9f
        X2BgYGFhYWJiYmNjY2RkZGVlZWZmZmdnZ2hoaGlpaWpqamtra21tbW5ubm9vb3Bw
        cHFxcXJycnNzc3R0dHV1dXZ2dnd3d3h4eHl5eXp6ent7e3x8fH19fX5+fn9/f4CA
        gIGBgYKCgoODg4SEhIWFhYaGhoeHh4iIiImJiYqKiouLi4yMjI2NjY6Ojo+Pj5CQ
        kJGRkZKSkpOTk5SUlJWVlZaWlpeXl5iYmJmZmZqampubm5ycnJ2dnZ6enp+fn6Cg
        oKGhoaKioqOjo6SkpKWlpaampqenp6ioqKmpqaqqqqurq6ysrK2tra6urq+vr7Cw
        sLGxsbKysrOzs7S0tLW1tba2tre3t7i4uLm5ubq6uru7u7y8vL29vb6+vr+/v8DA
        wMHBwcLCwsPDw8TExMXFxcbGxsfHx8jIyMnJycrKysvLy8zMzM3Nzc7Ozs/Pz9DQ
        0NHR0dLS0tPT09TU1NXV1dbW1tfX19jY2NnZ2dra2tvb29zc3N3d3d7e3t/f3+Dg
        4OHh4eLi4uPj4+Tk5OXl5ebm5ufn5+jo6Onp6erq6uvr6+zs7O3t7e7u7u/v7/Dw
        8PHx8fLy8vPz8/T09PX19fb29vf39/j4+Pn5+fr6+vv7+/z8/P39/f7+/v///wAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAACH/C05FVFNDQVBFMi4wAwEAAAAh+QQJAAAAACwAAAAAgACA
        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
        8AzX8A3n8A738A8H8RDP8IAAADs=
        '''
    # アイコンを設定
    root.geometry('600x300')
    root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(data=data))
    root.title(u"小説エディタ")
    # タイトルの画像ファイルのbase 64データ
    datas = '''R0lGODlhWAIsAfcAAAAAAQ0AAwAABQAAC0oXCzQMEC0VFBAAFQAAGFIfHQ0KHhIT
        IAAAISQBJgBuJwBuKSUkKgAAKzEbK3hBLTwYLh0bMWAyMYZZMRcAMwEMMw0SM2s/
        M1c5NEooNZdlNYNJNyESODQyOHlIOhcYOxwoO5FTOzw7PTovQQAGQh4NQkwvQqt4
        QwAQRCEgRKJnRC0oSUk/SQAYTHNRTD9DTQcbTj88TpJuUV1KUiIzU1FQU0ZGVDY1
        Vqp6V1dXWahzWVpaWgAcW7eIW3lfXsOXZRElZ2hoaCs2ajVBaxkubD1LbAAibWFg
        bcuccXZzckNSc86hdhlAd6OEeAsze3l6e1BffNWpgX9+gyNFhR5JhjFPhtuwhiBM
        iq6Si+O6jI6Ojl6/j1/AjypUkXFwkZOTk+7Bk5aWljVfl8CSmW97m4aFnNq5nZyb
        n3+/n4DAoDxqoaGhocSpo+XEoy5opKWlpXzTp6ioqHvSqDxsrDBxrICRra6urrW1
        tVl6tse1tsG2t7e3t//ht42Rubm5uUp8u7u7u/XQu/fYu0J4vcu+vlyNv7+/v/rf
        wk6HxMTExMbGxm+bycnJyYChymKWy8zMzKezzeHNzc7Ozs/Pz2eZ0NDQ0P/m0NHR
        0aCu0tTU1P/u1NbW1uPW1oOv2NjY2G6j2nqs2tra2tzc3L+/3d3d3f/13b3/3t/f
        3/Di4Yi44r7H4uPj4+Xl5cX/5f//5ufn58j/53u16Ojo6P/w6erq6v//6uvr6+zs
        7O3t7ZrG7vXr7u7u7v/z7v//7pHD7+/v78XX8PDw8PHx8fLy8v//8rTS8+Do8/Pz
        887c9PT09PX19f/59f/79f//9fb29rng9/f39///9/j4+Pn5+f//+YW++vr6+ubt
        +/v7+///+/z8/P39/f///f7+/v///p7N/6vZ/6Lb/7nh/8Dn/8rp/77v/+fz/9H2
        /9v3//H6//v6/+v8///+/9P//9z//+X//+v//+7///D///P///T///n///r///z/
        //3///7//////wAAACH/C05FVFNDQVBFMi4wAwEAAAAh+QQAAAAAACwAAAAAWAIs
        AQAI/gBVCRxIsKDBgwZj2XkAhhbChxAjSpxIsaLFixgzatzIsaPHjyBDihxJsqRJ
        jrTAPLAT66RLVQoZOnxJs6bNmzhz6tzJs6fPlylXtvypMWZDokiTKl3KtKnTp02D
        soQa0ehMqlizat3KtatXkVKHfrX6tazZs2jTqr0Z1izZtXDjyp1L12zbsm/r6t3L
        t6/fknfHLjz6t7Dhw4gLB/aaN7Hjx5AjY13ctbHky5gzaz5JmavlzaBDix59sPPW
        z6RTq16d2LRW1Kxjy5691nVW2LRz69791DZW3LyDCx/OVuVUvIOvEl/OvPlI31SB
        O59OvbpB6FClW9/OnTj2p9q7/osfL/u70/Dk06sHbb4p+vXw4ztuz/S9/Pv499Jf
        aj+///9p7adUfwAWaKBWAiZF4IEMNqhUgkgt6OCEFOYEIVESVqjhhoAZJxZjyXEo
        4og6XfhThiSmqKJEJvqE4oowxihQiz29KOONJNLIk4049qihjjvx6OOQDQKpk5BE
        JgmgkQfF4uSTUEYp5ZRS0kKHTFRmqeWWXHbp5ZdghinmmGSWaeaZaKap5ppstunm
        m3CaGRQdtMQZCx145qnnnnz22ecXD3zh56CEFmrooYgmquiijDbq6KOQRirppJRW
        aumlmGaqqaSACrrplQ+EKuqopJZq6qkPOKDqqqy26uqr/rDGKuustNZq66245qrr
        rrz26uuvwAYr7LDEFmvsscSiquyyp37h7LPQRivttNKCAagTbbCh7bbcduvtt+CG
        K+645JZr7rnopqvuuuy26+678MYr77z01mvvvfK24USg1lLr77/S0iLwwAQXbPDB
        B9PhQBv+NOzwwxBHLPHEFFds8cUYZ6zxxhx37PHHIIcs8sgkl2zyySinrPLJbThA
        J8Iwx3ywSwotvPLNOOes88489+zzz0AHLXTKLR8nmM1DJ6300kw37fTTUEfNsgNG
        g4i01FhnrfXWXHftddRFf1iZHVd/bfbZaKet9tpbh+0W2QyzLffcdNdt990Xu41c
        /tl49+3334AHHrTeR8ct+OGIJ6744hQTbrXhjEcu+eSUo+342HxXrvnmnHfe8+We
        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
        '''
    img = tk.PhotoImage(data=datas)
    label = tk.Label(image=img)
    # タイトルを表示する
    label.pack()
    # センターに表示する
    root.update_idletasks()
    ww = root.winfo_screenwidth()
    lw = root.winfo_width()
    wh = root.winfo_screenheight()
    lh = root.winfo_height()
    root.geometry(
        "{0}x{1}+{2}+{3}".format(
            str(lw),
            str(lh),
            str(int(ww/2-lw/2)),
            str(int(wh/2-lh/2))
        )
    )
    root.deiconify()

    # windowsのみタイトルバーを削除
    # OS別判断
    if os.name == 'nt':
        root.overrideredirect(True)
    elif os.name == 'posix':
        root.wm_attributes('-type', 'splash')
    # 描画するが処理は止めない
    root.update()
    # Janomeを使って日本語の形態素解析を起動
    tokenizer = Tokenizer()
    wiki_wiki = wikipediaapi.Wikipedia('ja')
    # メイン画面を削除
    root.destroy()
    # 初期処理
    original_image = '''R0lGODlhHgAeAPcAAAAAAAAAMwAAZgAAmQAAzAAA/wAzAAAzMwAzZgAzmQAzzAAz
        /wBmAABmMwBmZgBmmQBmzABm/wCZAACZMwCZZgCZmQCZzACZ/wDMAADMMwDMZgDM
        mQDMzADM/wD/AAD/MwD/ZgD/mQD/zAD//zMAADMAMzMAZjMAmTMAzDMA/zMzADMz
        MzMzZjMzmTMzzDMz/zNmADNmMzNmZjNmmTNmzDNm/zOZADOZMzOZZjOZmTOZzDOZ
        /zPMADPMMzPMZjPMmTPMzDPM/zP/ADP/MzP/ZjP/mTP/zDP//2YAAGYAM2YAZmYA
        mWYAzGYA/2YzAGYzM2YzZmYzmWYzzGYz/2ZmAGZmM2ZmZmZmmWZmzGZm/2aZAGaZ
        M2aZZmaZmWaZzGaZ/2bMAGbMM2bMZmbMmWbMzGbM/2b/AGb/M2b/Zmb/mWb/zGb/
        /5kAAJkAM5kAZpkAmZkAzJkA/5kzAJkzM5kzZpkzmZkzzJkz/5lmAJlmM5lmZplm
        mZlmzJlm/5mZAJmZM5mZZpmZmZmZzJmZ/5nMAJnMM5nMZpnMmZnMzJnM/5n/AJn/
        M5n/Zpn/mZn/zJn//8wAAMwAM8wAZswAmcwAzMwA/8wzAMwzM8wzZswzmcwzzMwz
        /8xmAMxmM8xmZsxmmcxmzMxm/8yZAMyZM8yZZsyZmcyZzMyZ/8zMAMzMM8zMZszM
        mczMzMzM/8z/AMz/M8z/Zsz/mcz/zMz///8AAP8AM/8AZv8Amf8AzP8A//8zAP8z
        M/8zZv8zmf8zzP8z//9mAP9mM/9mZv9mmf9mzP9m//+ZAP+ZM/+ZZv+Zmf+ZzP+Z
        ///MAP/MM//MZv/Mmf/MzP/M////AP//M///Zv//mf//zP///8DAwICAgIAAAACA
        AAAAgICAAIAAgACAgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
        AAAAAAAAAAAAAAAAACwAAAAAHgAeAAAIMgABCBxIsKDBgwgTKlzIsKHDhxAjSpxI
        saLFixgzatzIsaPHjyBDihxJsqTJkyhTngwIADs=
        '''
    tree_folder = [
        ['data/character', u'キャラクター'],
        ['data/occupation', u'職種'],
        ['data/space', u'場所'],
        ['data/event', u'イベント'],
        ['data/image', u'イメージ'],
        ['data/nobel', u'小説']
    ]
    color = [
        'sky blue',
        'yellow green',
        'gold',
        'salmon',
        'orange',
        'red',
        'hot pink',
        'dark orchid',
        'purple',
        'midnight blue',
        'light slate blue',
        'dodger blue',
        'dark turquoise',
        'cadet blue',
        'maroon',
        'tan1',
        'rosy brown',
        'indian red',
        'orange red',
        'violet red'
    ]
    # 再度メイン画面を作成
    root = tk.Tk()
    # アイコンを設定
    root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(data=data))
    # タイトルの表示
    root.title(u"小説エディタ")
    # フレームを表示する
    app = LineFrame(root)
    app.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))
    # 終了時にon_closingを行う
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    pf = platform.system()
    if pf == 'Windows':
        root.state('zoomed')
    else:
        root.attributes("-zoomed", "1")

# テスト環境ではループを抜ける
    value = sys.argv
    if len(value) > 1:
        for arg in value:
            if arg == "test":
                root.update_idletasks()

    else:
        root.mainloop()
