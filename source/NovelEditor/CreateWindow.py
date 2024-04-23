#!/usr/bin/env python3
import tkinter as tk
import tkinter.ttk as ttk
import customtkinter

from . import ProcessingMenu
from . import Definition


class CreateWindowClass(Definition.DefinitionClass):
    """画面の描画のクラス.

    ・画面描画にあるプログラム群

    Args:
        app (instance): MainProcessingClass のインスタンス
        locale_var (str): ロケーション
        master (instance): toplevel のインスタンス
    """
    def __init__(self, app, locale_var, master=None):
        super().__init__(locale_var, master)
        self.app = app

    def create_widgets(self):
        """画面の描画.

        ・メインウインドウにウェジットを配置する。
        """
        # メニューの配置
        File_menu = tk.Menu(self.app.menu_bar, tearoff=0)
        Edit_menu = tk.Menu(self.app.menu_bar, tearoff=0)
        List_menu = tk.Menu(self.app.menu_bar, tearoff=0)
        Processing_menu = tk.Menu(self.app.menu_bar, tearoff=0)
        Help_menu = tk.Menu(self.app.menu_bar, tearoff=0)
        # ファイルメニュー
        File_menu.add_command(
            label=self.app.dic.get_dict("Newfile"),
            under=5,
            accelerator='Ctrl+N',
            command=self.app.fmc.new_open
        )
        File_menu.add_command(
            label=self.app.dic.get_dict("Open"),
            under=3,
            accelerator='Ctrl+E',
            command=self.app.fmc.open_file
        )
        File_menu.add_separator()
        File_menu.add_command(
            label=self.app.dic.get_dict("Save"),
            under=3,
            accelerator='Ctrl+S',
            command=self.app.fmc.overwrite_save_file
        )
        File_menu.add_command(
            label=self.app.dic.get_dict("Save as"),
            under=9,
            accelerator='Ctrl+W',
            command=self.app.fmc.save_file
        )
        File_menu.add_separator()
        File_menu.add_command(
            label=self.app.dic.get_dict("Close"),
            under=4,
            accelerator='Ctrl+C',
            command=self.app.fmc.on_closing
        )
        self.app.menu_bar.add_cascade(
            label=self.app.dic.get_dict("File"),
            under=5,
            menu=File_menu
        )
        # 編集メニュー
        Edit_menu.add_command(
            label=self.app.dic.get_dict("Redo"),
            under=5,
            accelerator='Ctrl+Shift+Z',
            command=self.app.emc.redo
        )
        Edit_menu.add_command(
            label=self.app.dic.get_dict("Undo"),
            under=3,
            accelerator='Ctrl+Z',
            command=self.app.emc.undo
        )
        Edit_menu.add_separator()
        Edit_menu.add_command(
            label=self.app.dic.get_dict("Cut"),
            under=5,
            accelerator='Ctrl+X',
            command=self.app.emc.cut
        )
        Edit_menu.add_command(
            label=self.app.dic.get_dict("Copy"),
            under=4,
            accelerator='Ctrl+C',
            command=self.app.emc.copy
        )
        Edit_menu.add_command(
            label=self.app.dic.get_dict("Paste"),
            under=5,
            accelerator='Ctrl+V',
            command=self.app.emc.paste
        )
        Edit_menu.add_separator()
        Edit_menu.add_command(
            label=self.app.dic.get_dict("Find"),
            under=3,
            accelerator='Ctrl+F',
            command=self.app.fpc.find_dialog
        )
        Edit_menu.add_command(
            label=self.app.dic.get_dict("Replacement"),
            under=3,
            accelerator='Ctrl+L',
            command=self.app.fpc.replacement_dialog
        )
        self.app.menu_bar.add_cascade(
            label=self.app.dic.get_dict("Edit"),
            under=3,
            menu=Edit_menu
        )
        # 処理メニュー
        Processing_menu.add_command(
            label=self.app.dic.get_dict("Ruby"),
            under=6,
            accelerator='Ctrl+R',
            command=self.app.pmc.ruby_huri
        )
        Processing_menu.add_command(
            label=self.app.dic.get_dict("Count charactors"),
            under=9,
            accelerator='Ctrl+Shift+C',
            command=self.app.pmc.count_moji
        )
        Processing_menu.add_command(
            label=self.app.dic.get_dict("Meaning of selected characters"),
            under=8,
            accelerator='Ctrl+Shift+F',
            command=self.app.pmc.find_wikipedia
        )
        Processing_menu.add_command(
            label=self.app.dic.get_dict("Read aloud"),
            under=8,
            accelerator='Ctrl+Shift+R',
            command=self.app.pmc.read_text
        )
        Processing_menu.add_command(
            label=self.app.dic.get_dict("Sentence structure"),
            under=5,
            accelerator='Ctrl+Y',
            command=self.app.pmc.yahoo
        )
        Processing_menu.add_separator()
        Processing_menu.add_command(
            label=self.app.dic.get_dict("Font size"),
            under=11,
            accelerator='Ctrl+Shift+F',
            command=self.app.pmc.font_dialog
        )
        Processing_menu.add_separator()
        Processing_menu.add_command(
            label=self.app.dic.get_dict("Open [Become a Novelist]"),
            under=17,
            accelerator='Ctrl+U',
            command=self.app.pmc.open_becoming_novelist_page
        )
        self.app.menu_bar.add_cascade(
            label=self.app.dic.get_dict("Processing"),
            under=3,
            menu=Processing_menu
        )
        # リストメニュー
        List_menu.add_command(
            label=self.app.dic.get_dict("Increase item"),
            under=7,
            accelerator=self.app.dic.get_dict("Select and right click"),
            command=self.app.lmc.message_window
        )
        List_menu.add_command(
            label=self.app.dic.get_dict("Delete item"),
            under=6,
            accelerator=self.app.dic.get_dict("Select and right click"),
            command=self.app.lmc.message_window
        )
        List_menu.add_command(
            label=self.app.dic.get_dict("Rename item"),
            under=9,
            accelerator='Ctrl+G',
            command=self.app.lmc.on_name_click
        )
        self.app.menu_bar.add_cascade(
            label=self.app.dic.get_dict("Item"),
            under=4,
            menu=List_menu
        )
        # ヘルプメニュー
        Help_menu.add_command(
            label=self.app.dic.get_dict("Help"),
            under=4,
            accelerator='Ctrl+H',
            command=self.app.hmc.help
        )
        Help_menu.add_command(
            label=self.app.dic.get_dict("Version"),
            under=8,
            accelerator='Ctrl+Shift+V',
            command=self.app.hmc.version
        )
        self.app.menu_bar.add_cascade(
            label=self.app.dic.get_dict("Help"),
            under=4,
            menu=Help_menu
        )
        # ツリーコントロール、入力欄、行番号欄、スクロール部分を作成
        self.app.tree = ttk.Treeview(self.app, show="tree")
        self.app.tree.grid(row=0, column=0, sticky=(tk.N, tk.S))
        self.frame()
        self.app.fmc.tree_get_loop()

    def frame(self):
        """フレーム内にテキストボックスを表示.

        ・メインウインドウの右側に行番号、テキストボックス、スクロールバー
        を表示する。
        """
        # FrameNovelフレームにテキストエディタを表示
        self.app.FrameNovel = customtkinter.CTkFrame(self.app)
        self.app.NovelEditor = CustomText(
            self.app.FrameNovel,
            font=(self.app.font, self.app.pmc.font_size),
            undo=True
        )
        self.app.CanvasLineNumbers = tk.Canvas(self.app.FrameNovel, width=30)
        self.app.ScrollbarVerticalForNovelEditor = customtkinter.CTkScrollbar(
            self.app.FrameNovel,
            orientation="vertical",
            command=self.app.NovelEditor.yview
        )
        # 入力欄にスクロールを紐付け
        self.app.NovelEditor.configure(yscrollcommand=self.app.ScrollbarVerticalForNovelEditor.set)
        # 左から行番号、入力欄、スクロールウィジェット
        self.app.CanvasLineNumbers.grid(row=0, column=0, sticky=(tk.N + tk.S))
        self.app.NovelEditor.grid(row=0, column=1, sticky=(tk.NSEW))
        self.app.ScrollbarVerticalForNovelEditor.grid(row=0, column=2, sticky=(tk.N + tk.S))
        self.app.FrameNovel.columnconfigure(1, weight=1)
        self.app.FrameNovel.rowconfigure(0, weight=1)
        self.app.FrameNovel.grid(row=0, column=1, sticky=(tk.NSEW))
        # テキスト入力欄のみ拡大されるように
        self.app.columnconfigure(1, weight=1)
        self.app.rowconfigure(0, weight=1)
        # テキストを読み取り専用にする
        self.app.NovelEditor.configure(state='disabled')
        # テキストにフォーカスを当てる
        self.app.NovelEditor.focus()
        self.app.epc.create_event_text()

    def frame_image(self):
        """フレーム内にイメージフレーム表示.

        ・メインウインドウの右側にイメージキャンバス、スクロールバーを表示する。
        """
        self.app.FrameImage = customtkinter.CTkFrame(self.app)
        self.app.CanvasImage = tk.Canvas(self.app.FrameImage, bg="black", width=30)
        self.app.ScrollbarVerticalForCanvasImage = customtkinter.CTkScrollbar(
            self.app.FrameImage,
            orientation="vertical",
            command=self.app.CanvasImage.yview
        )
        self.app.ScrollbarHorizontalForCanvasImage = customtkinter.CTkScrollbar(
            self.app.FrameImage,
            orientation="horizontal",
            command=self.app.CanvasImage.xview
        )
        self.app.CanvasImage.configure(xscrollcommand=self.app.ScrollbarHorizontalForCanvasImage.set)
        self.app.CanvasImage.configure(yscrollcommand=self.app.ScrollbarVerticalForCanvasImage.set)
        self.app.CanvasImage.grid(
            row=0,
            column=1,
            sticky=(tk.NSEW)
        )
        self.app.ScrollbarVerticalForCanvasImage.grid(row=0, column=2, sticky=(tk.N + tk.S))
        self.app.ScrollbarHorizontalForCanvasImage.grid(row=1, column=1, sticky=(tk.W + tk.E))
        self.app.FrameImage.grid(row=0, column=1, sticky=(tk.NSEW))
        self.app.FrameImage.columnconfigure(1, weight=1)
        self.app.FrameImage.rowconfigure(0, weight=1)
        self.app.FrameImage.grid(row=0, column=1, sticky=(tk.NSEW))
        # デフォルトの画像を設定する
        self.app.CanvasImage.photo = tk.PhotoImage(data=self.BLANK_IMAGE)
        self.app.ImageOnImage = self.app.CanvasImage.create_image(
            0,
            0,
            anchor='nw',
            image=self.app.CanvasImage.photo
        )
        self.app.epc.create_event_image()

    def frame_character(self):
        """フレーム内にイメージフレーム表示.

        ・メインウインドウの右側に呼び名、似顔絵、名前、誕生日、略歴を表示する。
        """
        # チェック有無変数
        self.app.var = tk.IntVar()
        # value=0のラジオボタンにチェックを入れる
        self.app.var.set(0)
        self.app.FrameCharacter = customtkinter.CTkFrame(self.app)
        self.app.FrameCallName = customtkinter.CTkFrame(
            self.app.FrameCharacter
        )
        self.app.LabelCallName = customtkinter.CTkLabel(
            self.app.FrameCallName,
            text=self.app.dic.get_dict("Call name")
        )
        self.app.EntryCallName = customtkinter.CTkEntry(
            self.app.FrameCallName, width=400,
            font=(self.app.font, ProcessingMenu.ProcessingMenuClass.font_size)
        )
        self.app.LabelCallName.grid(row=0, column=0)
        self.app.EntryCallName.grid(row=1, column=0)
        self.app.FrameName = customtkinter.CTkFrame(
            self.app.FrameCharacter
        )
        self.app.LabelName = customtkinter.CTkLabel(
            self.app.FrameName,
            text=self.app.dic.get_dict("Name")
        )
        self.app.EntryName = customtkinter.CTkEntry(
            self.app.FrameName, width=400,
            font=(self.app.font, ProcessingMenu.ProcessingMenuClass.font_size)
        )
        self.app.LabelName.grid(row=0, column=0)
        self.app.EntryName.grid(row=1, column=0)
        self.app.FrameSex = customtkinter.CTkFrame(
            self.app.FrameCharacter
        )
        self.app.LabelSex = customtkinter.CTkLabel(
            self.app.FrameSex,
            text=self.app.dic.get_dict("Sex")
        )
        self.app.RadioButtonMan = customtkinter.CTkRadioButton(
            self.app.FrameSex, value=0,
            variable=self.app.var,
            text=self.app.dic.get_dict("Man")
        )
        self.app.RadioButtonWoman = customtkinter.CTkRadioButton(
            self.app.FrameSex, value=1,
            variable=self.app.var,
            text=self.app.dic.get_dict("Woman")
        )
        self.app.RadioButtonOther = customtkinter.CTkRadioButton(
            self.app.FrameSex, value=2,
            variable=self.app.var,
            text=self.app.dic.get_dict("Other")
        )
        self.app.LabelSex.grid(row=0, column=1)
        self.app.RadioButtonMan.grid(row=1, column=1)
        self.app.RadioButtonWoman.grid(row=2, column=1)
        self.app.RadioButtonOther.grid(row=3, column=1)
        self.app.FramePortrait = customtkinter.CTkFrame(
            self.app.FrameCharacter
        )
        self.app.LabelPortrait = customtkinter.CTkLabel(
            self.app.FramePortrait,
            text=self.app.dic.get_dict("Portrait")
        )
        self.app.CanvasPortrait = tk.Canvas(
            self.app.FramePortrait,
            bg="black",
            width=149,
            height=199
        )
        self.app.FramePortraitButtons = customtkinter.CTkFrame(self.app.FramePortrait)
        self.app.ButtonPortraitInsert = customtkinter.CTkButton(
            self.app.FramePortraitButtons,
            text=self.app.dic.get_dict("Insert"),
            width=len(self.app.dic.get_dict("Insert"))*12,
            command=self.app.spc.btn_click
        )
        self.app.ButtonPortraitDelete = customtkinter.CTkButton(
            self.app.FramePortraitButtons,
            width=len(self.app.dic.get_dict("Delete"))*12,
            text=self.app.dic.get_dict("Delete"),
            command=self.app.spc.clear_btn_click
        )
        self.app.ButtonPortraitInsert.grid(row=0, column=1)
        self.app.ButtonPortraitDelete.grid(row=1, column=1)

        self.app.LabelPortrait.grid(row=0, column=0, columnspan=2)
        self.app.FramePortraitButtons.grid(row=1,column=0, sticky=(tk.S))
        self.app.CanvasPortrait.grid(row=1, column=1)
        self.app.FrameBirthday = customtkinter.CTkFrame(
            self.app.FrameCharacter
        )
        self.app.LabelBirthday = customtkinter.CTkLabel(
            self.app.FrameBirthday,
            text=self.app.dic.get_dict("Birthday")
        )
        self.app.EntryBirthday = customtkinter.CTkEntry(
            self.app.FrameBirthday, width=400,
            font=(self.app.font, ProcessingMenu.ProcessingMenuClass.font_size)
        )
        self.app.LabelBirthday.grid(row=0, column=1)
        self.app.EntryBirthday.grid(row=1, column=1)
        self.app.LabelBiography = customtkinter.CTkLabel(
            self.app.FrameCharacter,
            text=self.app.dic.get_dict("Biography")
        )
        self.app.TextboxBiography = customtkinter.CTkTextbox(
            self.app.FrameCharacter,
            width=800,
            font=(self.app.font, ProcessingMenu.ProcessingMenuClass.font_size)
        )
        self.app.FrameCallName.grid(row=0, column=1, columnspa=2)
        self.app.FrameSex.grid(row=2, column=1, rowspan=2)
        self.app.FramePortrait.grid(row=0, column=3, rowspan=4)
        self.app.FrameName.grid(row=0, column=4)
        self.app.FrameBirthday.grid(row=2, column=4)
        self.app.LabelBiography.grid(row=4, column=1, columnspa=4)
        self.app.TextboxBiography.grid(
            row=5,
            column=1,
            columnspa=4,
            sticky=(tk.NSEW)
        )
        self.app.FrameCharacter.columnconfigure(1, weight=1)
        self.app.FrameCharacter.columnconfigure(4, weight=1)
        self.app.FrameCharacter.rowconfigure(5, weight=1)

        self.app.FrameCharacter.grid(row=0, column=1, sticky=(tk.NSEW))
        self.app.columnconfigure(1, weight=1)
        self.app.rowconfigure(0, weight=1)
        # デフォルトの画像を設定する
        self.app.CanvasPortrait.photo = tk.PhotoImage(data=self.BLANK_IMAGE)
        self.app.ImageOnPortrait = self.app.CanvasPortrait.create_image(
            0,
            0,
            anchor='nw',
            image=self.app.CanvasPortrait.photo
        )

        # キャラクターイベントを追加
        self.app.epc.create_event_character()


class CustomText(tk.Text):
    """Textのイベントを拡張したウィジェット.

    ・TCl/TKを使って、textに<<Scroll>>イベントと、<<Change>>イベントを追加する。

    Args:
        master (instance): toplevel のインスタンス
    """
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.tk.eval('''
            proc widget_proxy {widget widget_command args} {
                # 引数を使用してtkウィジェットコマンドを呼び出す
                set result [uplevel [linsert $args 0 $widget_command]]
                # ビューが移動した場合、バインドできるイベントを生成する
                if {([lrange $args 0 1] == {xview moveto}) ||
                    ([lrange $args 0 1] == {xview scroll}) ||
                    ([lrange $args 0 1] == {yview moveto}) ||
                    ([lrange $args 0 1] == {yview scroll})} {
                    event generate  $widget <<Scroll>> -when tail
                }
                # 内容が変更された場合、バインドできるイベントを生成する
                if {([lindex $args 0] in {insert replace delete})} {
                    event generate  $widget <<Change>> -when tail
                }
                # ウィジェットコマンドから結果を返す
                return $result
            }
            ''')
        self.tk.eval('''
            # コマンドをリネームする
            rename {widget} _{widget}
            # コマンドを置き換える
            interp alias {{}} ::{widget} {{}} widget_proxy {widget} _{widget}
        '''.format(widget=str(self)))
