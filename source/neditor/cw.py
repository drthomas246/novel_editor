#!/usr/bin/env python3
import tkinter as tk
import tkinter.ttk as ttk

from . import pm


class CreateWindowClass():
    """画面の描画のクラス.

    ・画面描画にあるプログラム群

    Args:
        app (instance): MainProcessingClass のインスタンス
        BLANK_IMAGE (str): 空白のbase 64データ
    """
    def __init__(self, app, BLANK_IMAGE):
        self.app = app
        self.BLANK_IMAGE = BLANK_IMAGE

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
            label=self.app.dic.get_dict("Meaning of letters"),
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
        # f1フレームにテキストエディタを表示
        self.app.f1 = tk.Frame(self.app, relief=tk.RIDGE, bd=2)
        self.app.text = CustomText(
            self.app.f1,
            font=(self.app.font, self.app.pmc.font_size),
            undo=True
        )
        self.app.line_numbers = tk.Canvas(self.app.f1, width=30)
        self.app.ysb = ttk.Scrollbar(
            self.app.f1,
            orient=tk.VERTICAL,
            command=self.app.text.yview
        )
        # 入力欄にスクロールを紐付け
        self.app.text.configure(yscrollcommand=self.app.ysb.set)
        # 左から行番号、入力欄、スクロールウィジェット
        self.app.line_numbers.grid(row=0, column=0, sticky=(tk.N, tk.S))
        self.app.text.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.app.ysb.grid(row=0, column=2, sticky=(tk.N, tk.S))
        self.app.f1.columnconfigure(1, weight=1)
        self.app.f1.rowconfigure(0, weight=1)
        self.app.f1.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.W, tk.E))
        # テキスト入力欄のみ拡大されるように
        self.app.columnconfigure(1, weight=1)
        self.app.rowconfigure(0, weight=1)
        # テキストを読み取り専用にする
        self.app.text.configure(state='disabled')
        # テキストにフォーカスを当てる
        self.app.text.focus()
        self.app.epc.create_event_text()

    def frame_image(self):
        """フレーム内にイメージフレーム表示.

        ・メインウインドウの右側にイメージキャンバス、スクロールバーを表示する。
        """
        self.app.f1 = tk.Frame(self.app, relief=tk.RIDGE, bd=2)
        self.app.image_space = tk.Canvas(self.app.f1, bg="black", width=30)
        self.app.image_ysb = ttk.Scrollbar(
            self.app.f1,
            orient=tk.VERTICAL,
            command=self.app.image_space.yview
        )
        self.app.image_xsb = ttk.Scrollbar(
            self.app.f1,
            orient=tk.HORIZONTAL,
            command=self.app.image_space.xview
        )
        self.app.image_space.configure(xscrollcommand=self.app.image_xsb.set)
        self.app.image_space.configure(yscrollcommand=self.app.image_ysb.set)
        self.app.image_space.grid(
            row=0,
            column=1,
            sticky=(tk.N, tk.S, tk.W, tk.E)
        )
        self.app.image_ysb.grid(row=0, column=2, sticky=(tk.N, tk.S))
        self.app.image_xsb.grid(row=1, column=1, sticky=(tk.W, tk.E))
        self.app.f1.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.app.f1.columnconfigure(1, weight=1)
        self.app.f1.rowconfigure(0, weight=1)
        self.app.f1.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.W, tk.E))
        # デフォルトの画像を設定する
        self.app.image_space.photo = tk.PhotoImage(data=self.BLANK_IMAGE)
        self.app.image_on_space = self.app.image_space.create_image(
            0,
            0,
            anchor='nw',
            image=self.app.image_space.photo
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
        self.app.f1 = tk.Frame(self.app, relief=tk.RIDGE, bd=2)
        self.app.label1 = tk.Label(
            self.app.f1,
            text=self.app.dic.get_dict("Call name")
        )
        self.app.txt_yobi_name = ttk.Entry(
            self.app.f1, width=30,
            font=(self.app.font, pm.ProcessingMenuClass.font_size)
        )
        self.app.label2 = tk.Label(
            self.app.f1,
            text=self.app.dic.get_dict("Name")
        )
        self.app.txt_name = ttk.Entry(
            self.app.f1, width=40,
            font=(self.app.font, pm.ProcessingMenuClass.font_size)
        )
        self.app.f2 = tk.LabelFrame(
            self.app.f1,
            relief=tk.RIDGE,
            bd=2,
            text=self.app.dic.get_dict("Sex")
        )
        self.app.rdo1 = tk.Radiobutton(
            self.app.f2, value=0,
            variable=self.app.var,
            text=self.app.dic.get_dict("Man")
        )
        self.app.rdo2 = tk.Radiobutton(
            self.app.f2, value=1,
            variable=self.app.var,
            text=self.app.dic.get_dict("Woman")
        )
        self.app.rdo3 = tk.Radiobutton(
            self.app.f2, value=2,
            variable=self.app.var,
            text=self.app.dic.get_dict("Other")
        )
        self.app.rdo1.grid(row=0, column=1)
        self.app.rdo2.grid(row=1, column=1)
        self.app.rdo3.grid(row=2, column=1)
        self.app.f3 = tk.LabelFrame(
            self.app.f1,
            relief=tk.RIDGE,
            bd=2,
            text=self.app.dic.get_dict("Portrait")
        )
        self.app.cv = self.app.foto_canvas = tk.Canvas(
            self.app.f3,
            bg="black",
            width=149,
            height=199
        )
        self.app.foto_canvas.grid(row=0, column=0)
        self.app.label3 = tk.Label(
            self.app.f1,
            text=self.app.dic.get_dict("Birthday")
        )
        self.app.txt_birthday = ttk.Entry(
            self.app.f1, width=40,
            font=(self.app.font, pm.ProcessingMenuClass.font_size)
        )
        self.app.f4 = tk.Frame(self.app.f1)
        self.app.foto_button = ttk.Button(
            self.app.f4,
            text=self.app.dic.get_dict("Insert"),
            width=str(self.app.dic.get_dict("Insert")),
            command=self.app.spc.btn_click
        )
        self.app.foto_button_calcel = ttk.Button(
            self.app.f4,
            width=str(self.app.dic.get_dict("Delete")),
            text=self.app.dic.get_dict("Delete"),
            command=self.app.spc.clear_btn_click
        )
        self.app.foto_button.grid(row=0, column=1)
        self.app.foto_button_calcel.grid(row=1, column=1)
        self.app.label4 = tk.Label(
            self.app.f1,
            text=self.app.dic.get_dict("Biography")
        )
        self.app.text_body = tk.Text(
            self.app.f1,
            width=80,
            font=(self.app.font, pm.ProcessingMenuClass.font_size)
        )
        self.app.label1.grid(row=0, column=1, columnspa=2)
        self.app.txt_yobi_name.grid(row=1, column=1, columnspa=2)
        self.app.f2.grid(row=2, column=1, rowspan=2)
        self.app.f4.grid(row=3, column=2)
        self.app.f3.grid(row=0, column=3, rowspan=4)
        self.app.label2.grid(row=0, column=4, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.app.txt_name.grid(row=1, column=4)
        self.app.label3.grid(row=2, column=4)
        self.app.txt_birthday.grid(row=3, column=4)
        self.app.label4.grid(row=4, column=1, columnspa=4)
        self.app.text_body.grid(
            row=5,
            column=1,
            columnspa=4,
            sticky=(tk.N, tk.S, tk.W, tk.E)
        )
        self.app.f1.columnconfigure(1, weight=1)
        self.app.f1.columnconfigure(4, weight=1)
        self.app.f1.rowconfigure(5, weight=1)

        self.app.f1.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.app.columnconfigure(1, weight=1)
        self.app.rowconfigure(0, weight=1)
        # デフォルトの画像を設定する
        self.app.cv.photo = tk.PhotoImage(data=self.BLANK_IMAGE)
        self.app.image_on_canvas = self.app.cv.create_image(
            0,
            0,
            anchor='nw',
            image=self.app.cv.photo
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
