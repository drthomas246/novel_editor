import tkinter as tk
import tkinter.ttk as ttk


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


class CreateWindowClass():
    """画面の描画のクラス

    ・画面描画にあるプログラム群

    Args:
        app (instance): MainProcessingClassインスタンス

    """
    def __init__(self, app):
        self.APP = app
        self.BLANK_IMAGE = '''R0lGODlhHgAeAPcAAAAAAAAAMwAAZgAAmQAAzAAA/wAzAAAzMwAzZgAzmQAzzAAz
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

    def create_widgets(self):
        """画面の描画

        ・メインウインドウにウェジットを配置する。

        """
        # メニューの配置
        File_menu = tk.Menu(self.APP.menu_bar, tearoff=0)
        Edit_menu = tk.Menu(self.APP.menu_bar, tearoff=0)
        List_menu = tk.Menu(self.APP.menu_bar, tearoff=0)
        Processing_menu = tk.Menu(self.APP.menu_bar, tearoff=0)
        Help_menu = tk.Menu(self.APP.menu_bar, tearoff=0)
        # ファイルメニュー
        File_menu.add_command(
            label=u'新規作成(N)',
            under=5,
            accelerator='Ctrl+N',
            command=self.APP.fmc.new_open
        )
        File_menu.add_command(
            label=u'開く(O)',
            under=3,
            accelerator='Ctrl+E',
            command=self.APP.fmc.open_file
        )
        File_menu.add_separator()
        File_menu.add_command(
            label=u'保存(S)',
            under=3,
            accelerator='Ctrl+S',
            command=self.APP.fmc.overwrite_save_file
        )
        File_menu.add_command(
            label=u'名前を付けて保存(W)',
            under=9,
            accelerator='Ctrl+W',
            command=self.APP.fmc.save_file
        )
        File_menu.add_separator()
        File_menu.add_command(
            label=u'閉じる(C)',
            under=4,
            accelerator='Ctrl+C',
            command=self.APP.fmc.on_closing
        )
        self.APP.menu_bar.add_cascade(
            label=u'ファイル(F)',
            under=5,
            menu=File_menu
        )
        # 編集メニュー
        Edit_menu.add_command(
            label=u'やり直し(R)',
            under=5,
            accelerator='Ctrl+Shift+Z',
            command=self.APP.emc.redo
        )
        Edit_menu.add_command(
            label=u'戻る(U)',
            under=3,
            accelerator='Ctrl+Z',
            command=self.APP.emc.undo
        )
        Edit_menu.add_separator()
        Edit_menu.add_command(
            label=u'切り取り(X)',
            under=5,
            accelerator='Ctrl+X',
            command=self.APP.emc.cut
        )
        Edit_menu.add_command(
            label=u'コピー(C)',
            under=4,
            accelerator='Ctrl+C',
            command=self.APP.emc.copy
        )
        Edit_menu.add_command(
            label=u'貼り付け(V)',
            under=5,
            accelerator='Ctrl+V',
            command=self.APP.emc.paste
        )
        Edit_menu.add_separator()
        Edit_menu.add_command(
            label=u'検索(F)',
            under=3,
            accelerator='Ctrl+F',
            command=self.APP.fpc.find_dialog
        )
        Edit_menu.add_command(
            label=u'置換(L)',
            under=3,
            accelerator='Ctrl+L',
            command=self.APP.fpc.replacement_dialog
        )
        self.APP.menu_bar.add_cascade(
            label=u'編集(E)',
            under=3,
            menu=Edit_menu
        )
        # 処理メニュー
        Processing_menu.add_command(
            label=u'ルビをふる(R)',
            under=6,
            accelerator='Ctrl+R',
            command=self.APP.pmc.ruby_huri
        )
        Processing_menu.add_command(
            label=u'文字数のカウント(C)',
            under=9,
            accelerator='Ctrl+Shift+C',
            command=self.APP.pmc.count_moji
        )
        Processing_menu.add_command(
            label=u'選択文字の意味(M)',
            under=8,
            accelerator='Ctrl+Shift+F',
            command=self.APP.pmc.find_wikipedia
        )
        Processing_menu.add_command(
            label=u'文章の読み上げ(B)',
            under=8,
            accelerator='Ctrl+Shift+R',
            command=self.APP.pmc.read_text
        )
        Processing_menu.add_command(
            label=u'文章校正(Y)',
            under=5,
            accelerator='Ctrl+Y',
            command=self.APP.pmc.yahoo
        )
        Processing_menu.add_separator()
        Processing_menu.add_command(
            label=u'フォントサイズの変更(F)',
            under=11,
            accelerator='Ctrl+Shift+F',
            command=self.APP.pmc.font_dialog
        )
        Processing_menu.add_separator()
        Processing_menu.add_command(
            label=u'「小説家になろう」のページを開く(U)',
            under=17,
            accelerator='Ctrl+U',
            command=self.APP.pmc.open_becoming_novelist_page
        )
        self.APP.menu_bar.add_cascade(
            label=u'処理(P)',
            under=3,
            menu=Processing_menu
        )
        # リストメニュー
        List_menu.add_command(
            label=u'項目を増やす(U)',
            under=7,
            accelerator='選択右クリック',
            command=self.APP.lmc.message_window
        )
        List_menu.add_command(
            label=u'項目を削除(D)',
            under=6,
            accelerator='選択右クリック',
            command=self.APP.lmc.message_window
        )
        List_menu.add_command(
            label=u'項目の名前を変更(C)',
            under=9,
            accelerator='Ctrl+G',
            command=self.APP.lmc.on_name_click
        )
        self.APP.menu_bar.add_cascade(
            label=u'リスト(L)',
            under=4,
            menu=List_menu
        )
        # ヘルプメニュー
        Help_menu.add_command(
            label=u'ヘルプ(H)',
            under=4,
            accelerator='Ctrl+H',
            command=self.APP.hmc.help
        )
        Help_menu.add_command(
            label=u'バージョン情報(V)',
            under=8,
            accelerator='Ctrl+Shift+V',
            command=self.APP.hmc.version
        )
        self.APP.menu_bar.add_cascade(
            label=u'ヘルプ(H)',
            under=4,
            menu=Help_menu
        )
        # ツリーコントロール、入力欄、行番号欄、スクロール部分を作成
        self.APP.tree = ttk.Treeview(self.APP, show="tree")
        self.APP.tree.grid(row=0, column=0, sticky=(tk.N, tk.S))
        self.frame()
        self.APP.fmc.tree_get_loop()

    def frame(self):
        """フレーム内にテキストボックスを表示

        ・メインウインドウの右側に行番号、テキストボックス、スクロールバー
        を表示する。

        """
        # f1フレームにテキストエディタを表示
        self.APP.f1 = tk.Frame(self.APP, relief=tk.RIDGE, bd=2)
        self.APP.text = CustomText(
            self.APP.f1,
            font=(self.APP.font, self.APP.pmc.font_size),
            undo=True
        )
        self.APP.line_numbers = tk.Canvas(self.APP.f1, width=30)
        self.APP.ysb = ttk.Scrollbar(
            self.APP.f1,
            orient=tk.VERTICAL,
            command=self.APP.text.yview
        )
        # 入力欄にスクロールを紐付け
        self.APP.text.configure(yscrollcommand=self.APP.ysb.set)
        # 左から行番号、入力欄、スクロールウィジェット
        self.APP.line_numbers.grid(row=0, column=0, sticky=(tk.N, tk.S))
        self.APP.text.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.APP.ysb.grid(row=0, column=2, sticky=(tk.N, tk.S))
        self.APP.f1.columnconfigure(1, weight=1)
        self.APP.f1.rowconfigure(0, weight=1)
        self.APP.f1.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.W, tk.E))
        # テキスト入力欄のみ拡大されるように
        self.APP.columnconfigure(1, weight=1)
        self.APP.rowconfigure(0, weight=1)
        # テキストを読み取り専用にする
        self.APP.text.configure(state='disabled')
        # テキストにフォーカスを当てる
        self.APP.text.focus()
        self.APP.epc.create_event_text()

    def frame_image(self):
        """フレーム内にイメージフレーム表示

        ・メインウインドウの右側にイメージキャンバス、スクロールバーを表示する。

        """
        self.APP.f1 = tk.Frame(self.APP, relief=tk.RIDGE, bd=2)
        self.APP.image_space = tk.Canvas(self.APP.f1, bg="black", width=30)
        self.APP.image_ysb = ttk.Scrollbar(
            self.APP.f1,
            orient=tk.VERTICAL,
            command=self.APP.image_space.yview
        )
        self.APP.image_xsb = ttk.Scrollbar(
            self.APP.f1,
            orient=tk.HORIZONTAL,
            command=self.APP.image_space.xview
        )
        self.APP.image_space.configure(xscrollcommand=self.APP.image_xsb.set)
        self.APP.image_space.configure(yscrollcommand=self.APP.image_ysb.set)
        self.APP.image_space.grid(
            row=0,
            column=1,
            sticky=(tk.N, tk.S, tk.W, tk.E)
        )
        self.APP.image_ysb.grid(row=0, column=2, sticky=(tk.N, tk.S))
        self.APP.image_xsb.grid(row=1, column=1, sticky=(tk.W, tk.E))
        self.APP.f1.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.APP.f1.columnconfigure(1, weight=1)
        self.APP.f1.rowconfigure(0, weight=1)
        self.APP.f1.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.W, tk.E))
        # デフォルトの画像を設定する
        self.APP.image_space.photo = tk.PhotoImage(data=self.BLANK_IMAGE)
        self.APP.image_on_space = self.APP.image_space.create_image(
            0,
            0,
            anchor='nw',
            image=self.APP.image_space.photo
        )
        self.APP.epc.create_event_image()

    def frame_character(self):
        """フレーム内にイメージフレーム表示

        ・メインウインドウの右側に呼び名、似顔絵、名前、誕生日、略歴を表示する。

        """
        # チェック有無変数
        self.APP.var = tk.IntVar()
        # value=0のラジオボタンにチェックを入れる
        self.APP.var.set(0)
        self.APP.f1 = tk.Frame(self.APP, relief=tk.RIDGE, bd=2)
        self.APP.label1 = tk.Label(self.APP.f1, text=u"呼び名")
        self.APP.txt_yobi_name = ttk.Entry(
            self.APP.f1, width=30,
            font=(self.APP.font, self.APP.pmc.font_size)
        )
        self.APP.label2 = tk.Label(self.APP.f1, text=u"名前")
        self.APP.txt_name = ttk.Entry(
            self.APP.f1, width=40,
            font=(self.APP.font, self.APP.pmc.font_size)
        )
        self.APP.f2 = tk.LabelFrame(
            self.APP.f1,
            relief=tk.RIDGE,
            bd=2,
            text=u"性別"
        )
        self.APP.rdo1 = tk.Radiobutton(
            self.APP.f2, value=0,
            variable=self.APP.var,
            text=u'男'
        )
        self.APP.rdo2 = tk.Radiobutton(
            self.APP.f2, value=1,
            variable=self.APP.var,
            text=u'女'
        )
        self.APP.rdo3 = tk.Radiobutton(
            self.APP.f2, value=2,
            variable=self.APP.var,
            text=u'その他'
        )
        self.APP.rdo1.grid(row=0, column=1)
        self.APP.rdo2.grid(row=1, column=1)
        self.APP.rdo3.grid(row=2, column=1)
        self.APP.f3 = tk.LabelFrame(
            self.APP.f1,
            relief=tk.RIDGE,
            bd=2,
            text=u"似顔絵"
        )
        self.APP.cv = self.APP.foto_canvas = tk.Canvas(
            self.APP.f3,
            bg="black",
            width=149,
            height=199
        )
        self.APP.foto_canvas.grid(row=0, column=0)
        self.APP.label3 = tk.Label(self.APP.f1, text=u"誕生日")
        self.APP.txt_birthday = ttk.Entry(
            self.APP.f1, width=40,
            font=(self.APP.font, self.APP.pmc.font_size)
        )
        self.APP.f4 = tk.Frame(self.APP.f1)
        self.APP.foto_button = ttk.Button(
            self.APP.f4,
            width=5,
            text=u'挿入',
            command=self.APP.sfc.btn_click
        )
        self.APP.foto_button_calcel = ttk.Button(
            self.APP.f4,
            width=5,
            text=u'消去',
            command=self.APP.sfc.clear_btn_click
        )
        self.APP.foto_button.grid(row=0, column=1)
        self.APP.foto_button_calcel.grid(row=1, column=1)
        self.APP.label4 = tk.Label(self.APP.f1, text=u"略歴")
        self.APP.text_body = tk.Text(
            self.APP.f1,
            width=80,
            font=(self.APP.font, self.APP.pmc.font_size)
        )
        self.APP.label1.grid(row=0, column=1, columnspa=2)
        self.APP.txt_yobi_name.grid(row=1, column=1, columnspa=2)
        self.APP.f2.grid(row=2, column=1, rowspan=2)
        self.APP.f4.grid(row=3, column=2)
        self.APP.f3.grid(row=0, column=3, rowspan=4)
        self.APP.label2.grid(row=0, column=4, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.APP.txt_name.grid(row=1, column=4)
        self.APP.label3.grid(row=2, column=4)
        self.APP.txt_birthday.grid(row=3, column=4)
        self.APP.label4.grid(row=4, column=1, columnspa=4)
        self.APP.text_body.grid(
            row=5,
            column=1,
            columnspa=4,
            sticky=(tk.N, tk.S, tk.W, tk.E)
        )
        self.APP.f1.columnconfigure(1, weight=1)
        self.APP.f1.columnconfigure(4, weight=1)
        self.APP.f1.rowconfigure(5, weight=1)

        self.APP.f1.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.APP.columnconfigure(1, weight=1)
        self.APP.rowconfigure(0, weight=1)
        # デフォルトの画像を設定する
        self.APP.cv.photo = tk.PhotoImage(data=self.BLANK_IMAGE)
        self.APP.image_on_canvas = self.APP.cv.create_image(
            0,
            0,
            anchor='nw',
            image=self.APP.cv.photo
        )

        # キャラクターイベントを追加
        self.APP.epc.create_event_character()
