#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
import zipfile
import shutil
import webbrowser
import platform
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as Font
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog

import jaconv
from janome.tokenizer import Tokenizer

class CustomText(tk.Text):
    """Textの、イベントを拡張したウィジェット."""
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

class LineFrame(ttk.Frame):
    """メインフレーム処理."""
    def __init__(self, master=None, **kwargs):
        """初期設定"""
        super().__init__(master, **kwargs)
        self.initialize()
        self.create_widgets()
        self.create_event()

    def initialize(self):
        """初期化処理"""
        # 今の処理ししているファイルのパス
        self.now_path = ""
        # 現在開いているファイル
        self.file_path = ""
        # 検索文字列
        self.last_text=""
        # 現在入力中の初期テキスト
        self.text_text=""
        # 文字の大きさ
        self.int_var=16
        pf = platform.system()
        if pf == 'Windows':
            self.font="メイリオ"
        elif pf == 'Darwin':
            self.font="Osaka-等幅"
        elif pf == 'Linux':
            self.font="IPAゴシック"
        # dataフォルダがあるときは、削除する
        if os.path.isdir('./data'):
            shutil.rmtree('./data')
        # 新しくdataフォルダを作成する
        for val in tree_folder:
            os.makedirs('./{0}'.format(val[0]))

    def create_widgets(self):
        """ウェジット配置"""
        # ツリーコントロール、入力欄、行番号欄、スクロール部分を作成
        self.tree = ttk.Treeview(self,show="tree")
        self.text = CustomText(self,font=(self.font,self.int_var),undo=True)
        self.line_numbers = tk.Canvas(self, width=30)
        self.ysb = ttk.Scrollbar(
            self, orient=tk.VERTICAL, command=self.text.yview)
        # 入力欄にスクロールを紐付け
        self.text.configure(yscrollcommand=self.ysb.set)
        # 左から行番号、入力欄、スクロールウィジェット
        self.tree.grid(row=0, column=0, sticky=(tk.N, tk.S))
        self.line_numbers.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.text.grid(row=0, column=2, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.ysb.grid(row=0, column=3, sticky=(tk.N, tk.S))
        # テキスト入力欄のみ拡大されるように
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        # ツリービューのリスト表示
        self.TreeGetLoop()
        # テキストを読み取り専用にする
        self.text.configure(state='disabled')
        # テキストにフォーカスを当てる
        self.text.focus()

    def create_event(self):
        """イベントの設定."""
        # テキスト内でのスクロール時
        self.text.bind('<<Scroll>>', self.update_line_numbers)
        self.text.bind('<Up>', self.update_line_numbers)
        self.text.bind('<Down>', self.update_line_numbers)
        self.text.bind('<Left>', self.update_line_numbers)
        self.text.bind('<Right>', self.update_line_numbers)
        # テキストの変更時
        self.text.bind('<<Change>>', self.Change_setting)
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
        # 上書き保存する
        self.text.bind('<Control-Key-s>', self.overwrite_save_file)
        # 新規作成する
        self.text.bind('<Control-Key-n>', self.new_open)
        # helpページを開く
        self.text.bind('<Control-Key-h>',self.open_help)
        # 文字数と行数をカウントする
        self.text.bind('<Control-Shift-Key-C>', self.moji_count)
        # redo処理
        self.text.bind('<Control-Shift-Key-Z>', self.redo)
        # フォントサイズの変更
        self.text.bind('<Control-Shift-Key-F>', self.font_dialog)
        # ツリービューをダブルクリックしたときにその項目を表示する
        self.tree.bind("<Double-1>", self.OnDoubleClick)
        self.tree.bind("<Control-Key-g>", self.On_name_Click)
        # ツリービューで右クリックしたときにダイアログを表示する
        self.tree.bind("<Button-3>", self.message_window)

    def create_tags(self):
        """タグの作成"""
        i = 0
        system_dic= "喜寛,固有名詞,ヨシヒロ"
        # キャラクターから一覧を作る。
        children = self.tree.get_children('data/character')
        for child in children:
            # ユーザー定義辞書の設定
            reading = ""
            childname = self.tree.item(child,"text")
            for token in tokenizer.tokenize(childname):
                reading += token.phonetic
            system_dic += "\n{0},固有名詞,{1}".format(childname,reading)
            # タグの作成
            self.text.tag_configure(
                childname, foreground=color[i]
            )
            i += 1
        f = open("./userdic.csv",'w', encoding='utf-8')
        f.write(system_dic)
        f.close()
        # Janomeを使って日本語の形態素解析
        self.t = Tokenizer("./userdic.csv", udic_type="simpledic", udic_enc="utf8")

    def all_highlight(self, event=None):
        """全てハイライト"""
        # 全てのテキストを取得
        src = self.text.get('1.0', 'end - 1c')
        # 全てのハイライトを一度解除する
        for tag in self.text.tag_names():
            self.text.tag_remove(tag, '1.0', 'end')

        # ハイライトする
        self._highlight('1.0', src)

    def line_highlight(self, event=None):
        """現在行だけハイライト"""
        start = 'insert linestart'
        end = 'insert lineend'
        # 現在行のテキストを取得
        src = self.text.get(start, end)
        # その行のハイライトを一度解除する
        for tag in self.text.tag_names():
            self.text.tag_remove(tag, start, end)

        # ハイライトする
        self._highlight(start, src)

    def _highlight(self, start, src):
        """ハイライトの共通処理"""
        self.create_tags()
        self.text.mark_set('range_start', start)
        # 形態素解析を行う
        for token in self.t.tokenize(src):
            content=token.surface
            self.text.mark_set(
                'range_end', 'range_start+{0}c'.format(len(content))
            )
            # 全角スペースの時は一つずらす
            if src[0]=="\u3000":
                self.text.tag_add(content, 'range_start+1c', 'range_end+1c')
            else:
                self.text.tag_add(content, 'range_start', 'range_end')
            self.text.mark_set('range_start', 'range_end')

    def font_dialog(self,event=None):
        """フォントサイズダイアログを作成"""
        self.sub_wins = tk.Toplevel(self)
        self.sub_wins.geometry("200x75")
        self.intSpin = ttk.Spinbox(self.sub_wins,from_=12,to=72)
        self.intSpin.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E,ipady=3)
        button = ttk.Button(
            self.sub_wins,
            text = 'サイズ変更',
            width = str('サイズ変更'),
            padding = (10, 5),
            command = self.size_Change
            )
        button.grid(row=1, column=1)
        self.intSpin.set(self.int_var)
        self.sub_wins.title(u'フォントサイズの変更')

    def size_Change(self):
        """フォントのサイズを変える"""
        # 比較のため数値列に変更
        self.int_var = int(self.intSpin.get())
        if self.int_var < 12: # 12より下の値を入力した時、12にする
            self.int_var = 12
        elif 72 < self.int_var: # 72より上の値を入力した時、72にする
            self.int_var = 72
        # 文字列にもどす
        self.int_var=str(self.int_var)
        self.sub_wins.destroy()
        # フォントサイズの変更
        self.text.configure(font=(self.font, self.int_var))

    def open_url(self,event=None):
        """小説家になろうのユーザーページを開く"""
        webbrowser.open("https://syosetu.com/user/top/")

    def open_help(self,event=None):
        """helpページを開く"""
        webbrowser.open('file://' + os.path.dirname(os.path.abspath(os.path.dirname(__file__))) + "/README.html")

    def isHiragana(self,char):
        """引数がひらがなならTrue、さもなければFalseを返す"""
        return (0x3040 < ord(char) < 0x3094)

    def ruby(self,event=None):
        """ルビをふる"""
        hon = ""
        # 選択文字列を切り取る
        set_ruby = self.text.get('sel.first','sel.last')
        # 選択文字列を削除する
        self.text.delete('sel.first','sel.last')
        # 形態素解析を行う
        for token in tokenizer.tokenize(set_ruby):
            # ルビの取得
            ruby = ""
            ruby = jaconv.kata2hira(token.reading)
            # 解析している文字のひらがなの部分を取得
            hira = ""
            for i in token.surface:
                if self.isHiragana(i):
                    hira += i
            # ルビがないときと、記号の時の処理
            if ruby.replace(hira, '') == "" or token.part_of_speech.split(",")[0] == "記号":
                hon += token.surface
            else:
                # ルビ振りを行う
                hon += "|{0}≪{1}≫{2}".format(token.surface.replace(hira, ''),ruby.replace(hira, ''),hira)

        # テキストを表示する
        self.text.insert('insert', hon)

    def redo(self,event=None):
        """redo処理を行う"""
        self.text.edit_redo()

    def moji_count(self,event=None):
        """文字数と行数を表示する"""
        # 行数の取得
        new_line = int(self.text.index('end-1c').split('.')[0])
        # メッセージボックスの表示
        messagebox.showinfo(u"文字数と行数", "文字数 : {0}文字　行数 : {1}行".format(len(self.text.get('1.0', 'end'))-new_line,new_line))

    def new_file(self):
        """新規作成をするための準備"""
        self.initialize()
        for val in tree_folder:
            self.tree.delete(val[0])

        # ツリービューを表示する
        self.TreeGetLoop()
        self.text.delete('1.0', 'end')
        self.winfo_toplevel().title(u"小説エディタ")
        # テキストを読み取り専用にする
        self.text.configure(state='disabled')
        # テキストにフォーカスを当てる
        self.text.focus()

    def new_open(self,event=None):
        """新規作成をする"""
        if not self.text.get('1.0', 'end - 1c') == self.text_text:
            if messagebox.askokcancel(u"小説エディタ", u"上書き保存しますか？"):
                self.overwrite_save_file()
                self.new_file()

            elif messagebox.askokcancel(u"小説エディタ", u"今の編集を破棄して新規作成しますか？"):
                self.new_file()
        else:
            self.new_file()

    def overwrite_save_file(self,event=None):
        """上書き保存処理"""
        # ファイルパスが存在するとき
        if not self.file_path == "":
            # 編集中のファイルを保存する
            self.open_file_save(self.now_path)
            # zipファイルにまとめる
            shutil.make_archive(self.file_path,"zip","./data")
            # 拡張子の変更を行う
            shutil.move("{0}.zip".format(self.file_path),"{0}.ned".format(self.file_path))
        # ファイルパスが存在しないとき
        else:
            # 保存ダイアログを開く
            self.save_file()

    def save_file(self,event=None):
        """ファイルを保存処理"""
        # ファイル保存ダイアログを表示する
        fTyp = [("小説エディタ",".ned")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        filepath = filedialog.asksaveasfilename(filetypes = fTyp,initialdir = iDir)
        # ファイルパスが決まったとき
        if not filepath == "":
            # 拡張子を除いて保存する
            self.file_path, ___ = os.path.splitext(filepath)
            # 上書き保存処理
            self.overwrite_save_file()

    def open_file(self,event=None):
        """ファイルを開く処理"""
        # ファイルを開くダイアログを開く
        fTyp = [("小説エディタ",".ned")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        filepath = filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
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
            self.TreeGetLoop()
            # ファイルパスを拡張子抜きで表示する
            filepath, ___ = os.path.splitext(filepath)
            self.file_path = filepath
            self.now_path = ""
            # テキストビューを新にする
            self.text.delete('1.0', 'end')

    def TreeGetLoop(self):
        """フォルダにあるファイルを取得してツリービューに挿入."""
        for val in tree_folder:
            self.tree.insert('', 'end', val[0], text=val[1])
            # フォルダのファイルを取得
            path = "./{0}".format(val[0])
            files = os.listdir(path)
            for filename in files:
                self.tree.insert(val[0], 'end', text=os.path.splitext(filename)[0])

    def find_dialog(self,event=None):
        """検索ボックスを作成する"""
        sub_win = tk.Toplevel(self)
        sub_win.geometry("260x75")
        self.text_var = ttk.Entry(sub_win,width=40)
        self.text_var.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E,ipady=3)
        button = ttk.Button(
            sub_win,
            text = '検索',
            width = str('検索'),
            padding = (10, 5),
            command = self.search
            )
        button.grid(row=1, column=1)
        # 最前面に表示し続ける
        sub_win.attributes("-topmost", True)
        sub_win.title(u'検索')
        self.text_var.focus()

    def search_start(self, texts):
        """検索の初回処理."""
        # 各変数の初期化
        self.next_pos_index = 0
        self.all_pos = []

        # はじめは1.0から検索し、見つかれば、それの最後+1文字の時点から再検索
        # all_posには、['1.7', '3,1', '5.1'...]のような検索文字が見つかった地点の最初のインデックスが入っていく
        start_index = '1.0'
        while True:
            pos = self.text.search(texts, start_index, stopindex='end')
            if not pos:  # 検索文字がもう見つからければbreak
                break
            self.all_pos.append(pos)
            start_index = '{0} + 1c'.format(pos)  # 最後から+1文字を起点に、再検索

        # 最初のマッチ部分、all_pos[0]を選択させておく
        self.search_next(texts)

    def search_next(self, texts):
        """検索の続きの処理."""
        try:
            # 今回のマッチ部分の取得を試みる
            pos = self.all_pos[self.next_pos_index]
        except IndexError:
            # all_posが空でなくIndexErrorならば、全てのマッチを見た、ということ
            # なのでnext_post_indexを0にし、最初からまたマッチを見せる
            if self.all_pos:
                self.next_pos_index = 0
                self.search_next(texts)
        else:
            # 次のマッチ部分を取得できればここ
            start = pos
            end = '{0} + {1}c'.format(pos, len(texts))

            # マッチ部分〜マッチ部分+文字数分 の範囲を選択する
            self.text.tag_add('sel', start, end)

            # インサートカーソルをマッチした部分に入れ、スクロール、フォーカスも合わせておく
            self.text.mark_set('insert', start)
            self.text.see('insert')
            self.text.focus()
            # 次回取得分のために+1
            self.next_pos_index += 1

    def search(self, event=None):
        """文字の検索を行う."""
        # 現在選択中の部分を解除
        self.text.tag_remove('sel', '1.0', 'end')

        # 現在検索ボックスに入力されてる文字
        now_text = self.text_var.get()

        if not now_text:
            # 空欄だったら処理しない
            pass
        elif now_text != self.last_text:
            # 前回の入力と違う文字なら、検索を最初から行う
            self.search_start(now_text)
        else:
            # 前回の入力と同じなら、検索の続きを行う
            self.search_next(now_text)

        # 今回の入力を、「前回入力文字」にする
        self.last_text = now_text

    def message_window(self,event=None):
        """ツリービューの選択ダイアログを表示する."""
        curItem = self.tree.focus()              #選択アイテムの認識番号取得
        parentItem = self.tree.parent(curItem)   #親アイテムの認識番号取得
        # 親アイテムをクリックしたとき
        if str(self.tree.item(curItem)["text"]) and (not str(self.tree.item(parentItem)["text"])):
            # サブダイヤログを表示する
            self.sub_win = tk.Toplevel(self)
            self.sub_win.geometry("260x75")
            self.txt = ttk.Entry(self.sub_win,width=40)
            self.txt.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E,ipady=3)
            button = ttk.Button(
                self.sub_win,
                text = '実行',
                width = str('実行'),
                padding = (10, 5),
                command = self.SubWinOk
                )
            button.grid(row=1, column=0)
            button = ttk.Button(
                self.sub_win,
                text = 'キャンセル',
                width = str('キャンセル'),
                padding = (10, 5),
                command = self.sub_win.destroy
                )
            button.grid(row=1, column=1)
            self.txt.focus()
            self.sub_win.title(u'{0}に挿入'.format(self.tree.item(curItem)["text"]))
        # 子アイテムを右クリックしたとき
        else:
            if str(self.tree.item(curItem)["text"]):
                # 項目を削除する
                file_name = self.tree.item(curItem)["text"]
                text = self.tree.item(parentItem)["text"]
                # ＯＫ、キャンセルダイアログを表示し、ＯＫを押したとき
                if messagebox.askokcancel(u"項目削除", "{0}を削除しますか？".format(file_name)):
                    # パスを取得する
                    for val in tree_folder:
                        if text == val[1]:
                            path = "./{0}/{1}.txt".format(val[0],file_name)
                            self.tree.delete(curItem)
                            self.now_path=""
                            break
                    # パスが存在したとき
                    if not path == "":
                        os.remove(path)
                        self.text.delete('1.0', tk.END)
                        self.text.focus()

    def SubWinOk(self):
        """ツリービューの選択ダイアログの実行ボタンが押されたとき."""
        # テキストを読み取り専用を解除する
        self.text.configure(state='normal')
        file_name=self.txt.get()
        self.sub_win.destroy()
        self.open_file_save(self.now_path)
        curItem = self.tree.focus()              #選択アイテムの認識番号取得
        text = self.tree.item(curItem)["text"]
        path = ""
        # 選択されているフォルダを見つける
        for val in tree_folder:
            if text == val[1]:
                path = "./{0}/{1}.txt".format(val[0],file_name)
                tree = self.tree.insert(val[0], 'end', text=file_name)
                self.now_path = path
                break

        # パスが存在すれば新規作成する
        if not path == "":
            self.text.delete('1.0', tk.END)
            f = open(path, mode='w')
            f.write("")
            f.close()
            # ツリービューを選択状態にする
            self.tree.see(tree)
            self.tree.selection_set(tree)
            self.winfo_toplevel().title(u"小説エディタ\\{0}\\{1}".format(text,file_name))
            self.text.focus()
            self.create_tags()

    def open_file_save(self,path):
        """開いてるファイルを保存する."""
        # 編集ファイルを保存する
        if not path == "":
            f = open(path,'w')
            f.write(self.text.get("1.0",tk.END+'-1c'))
            f.close()
            self.now_path = path

    def OnDoubleClick(self, event=None):
        """ツリービューをダブルクリックしたとき."""
        curItem = self.tree.focus()              #選択アイテムの認識番号取得
        parentItem = self.tree.parent(curItem)   #親アイテムの認識番号取得
        text = self.tree.item(parentItem)["text"]
        # 開いているファイルを保存
        self.open_file_save(self.now_path)
        # テキストを読み取り専用を解除する
        self.text.delete('1.0', 'end')
        self.text.configure(state='disabled')
        # 条件によって分離
        sub_text = self.tree.item(curItem)["text"]
        path = ""
        for val in tree_folder:
            if text == val[1]:
                path = "./{0}/{1}.txt".format(val[0],sub_text)
                self.now_path = path
                # テキストを読み取り専用を解除する
                self.text.configure(state='normal')
                self.text.focus()
                self.path_read_text(text,sub_text)
                return

        self.now_path = ""

    def path_read_text(self,text,sub_text):
        # パスが存在すれば読み込んで表示する
        if not self.now_path == "":
            self.text.delete('1.0', tk.END)
            f = open(self.now_path)
            self.text_text=f.read()
            self.text.insert(tk.END,self.text_text)
            f.close()
            self.winfo_toplevel().title(u"小説エディタ\\{0}\\{1}".format(text,sub_text))
            # シンタックスハイライトをする
            self.all_highlight()

    def On_name_Click(self, event=None):
        curItem = self.tree.focus()              #選択アイテムの認識番号取得
        parentItem = self.tree.parent(curItem)   #親アイテムの認識番号取得
        text = self.tree.item(parentItem)["text"]
        if not text == "":
            self.sub_name_win = tk.Toplevel(self)
            self.sub_name_win.geometry("260x75")
            self.txt_name = ttk.Entry(self.sub_name_win,width=40)
            self.txt_name.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E,ipady=3)
            co_text = self.tree.item(curItem)["text"]
            button = ttk.Button(
                self.sub_name_win,
                text = '実行',
                width = str('実行'),
                padding = (10, 5),
                command = self.SubWin_name_Ok
                )
            button.grid(row=1, column=0)
            button = ttk.Button(
                self.sub_name_win,
                text = 'キャンセル',
                width = str('キャンセル'),
                padding = (10, 5),
                command = self.sub_name_win.destroy
                )
            button.grid(row=1, column=1)
            self.txt_name.focus()
            self.txt_name.insert(tk.END,co_text)
            self.txt_name.select_range(0, 'end')
            self.sub_name_win.title(u'{0}の名前を変更'.format(co_text))

    def SubWin_name_Ok(self, event=None):
        curItem = self.tree.focus()              #選択アイテムの認識番号取得
        parentItem = self.tree.parent(curItem)   #親アイテムの認識番号取得
        text = self.tree.item(parentItem)["text"]
        sub_text = self.tree.item(curItem)["text"]
        co_text = self.txt_name.get()
        self.sub_name_win.destroy()
        for val in tree_folder:
            if text == val[1]:
                path1 = "./{0}/{1}.txt".format(val[0],sub_text)
                path2 = "./{0}/{1}.txt".format(val[0],co_text)
                self.now_path = path2
                # テキストの名前を変更する
                os.rename(path1, path2)
                self.tree.delete(curItem)
                Item = self.tree.insert(parentItem, 'end', text=co_text)
                self.tree.selection_set(Item)
                return

    def update_line_numbers(self,event=None):
        """行番号の描画."""
        # 現在の行番号を全て消す
        self.line_numbers.delete(tk.ALL)

        # Textの0, 0座標、つまり一番左上が何行目にあたるかを取得
        i = self.text.index("@0,0")
        while True:
            # dlineinfoは、その行がどの位置にあり、どんなサイズか、を返す
            # (3, 705, 197, 13, 18) のように帰る(x,y,width,height,baseline)
            dline= self.text.dlineinfo(i)
            # dlineinfoに、存在しない行や、スクロールしないと見えない行を渡すとNoneが帰る
            if dline is None:
                break
            else:
                y = dline[1]  # y座標を取得

            # (x座標, y座標, 方向, 表示テキスト)を渡して行番号のテキストを作成
            linenum = str(i).split(".")[0]
            self.line_numbers.create_text(3, y, anchor=tk.NW, text=linenum,font=("",12))
            i = self.text.index("%s+1line" % i)

    def Change_setting(self, event=None):
        """テキストの変更時"""
        self.update_line_numbers()
        # その行のハイライトを行う
        self.line_highlight()

    def tab(self,event=None):
        """タブ押下時の処理"""
        # 文字を選択していないとき
        sel_range = self.text.tag_ranges('sel')
        if not sel_range:
            return self.auto_complete()
        else:
            return

    def auto_complete(self):
        """補完リストの作成"""
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
            'insert')
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
        """コード補完リストの候補キーワードを作成する."""
        text = ''
        text, _, _ = self.get_current_insert_word()
        my_func_and_class = set()
        # コード補完リストをTreeviewにある'名前'から得る
        children = self.tree.get_children('data/character')
        for child in children:
            childname = self.tree.item(child,"text")
            # 前列の文字列と同じものを選び出す
            if childname.startswith(text) or childname.startswith(text.title()):
                my_func_and_class.add(childname)

        result = list(my_func_and_class)
        return result

    def remove_list(self,event=None):
        """コード補完リストの削除処理."""
        self.auto_complete_list.destroy()
        self.text.focus()  # テキストウィジェットにフォーカスを戻す

    def selection(self,event=None):
        """コード補完リストでの選択後の処理."""
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
        """現在入力中の単語と位置を取得する."""
        text = ''
        start_i = 1
        end_i = 0
        while True:
            start = 'insert-{0}c'.format(start_i)
            end = 'insert-{0}c'.format(end_i)
            text = self.text.get(start, end)
            # 1文字ずつ見て、スペース、改行、タブ、空文字、句読点にぶつかったら終わり
            if text in (' ', '　','\t', '\n', '','、','。'):
                text = self.text.get(end, 'insert')

                # 最終単語を取得する
                pri = [token.surface for token in tokenizer.tokenize(text)]
                hin = [token.part_of_speech.split(',')[0] for token in tokenizer.tokenize(text)]
                if len(pri)>0:
                    if hin[len(pri)-1] == '名詞':
                        text = pri[len(pri)-1]
                    else:
                        text = ""
                else:
                    text = ""

                end = 'insert-{0}c'.format(len(text))
                return text, end, 'insert'

            start_i += 1
            end_i += 1

def on_closing():
    """終了時の処理"""
    if messagebox.askokcancel(u"小説エディタ", u"終了してもいいですか？"):
        shutil.rmtree("./data")
        if os.path.isfile("./userdic.csv"):
            os.remove("./userdic.csv")

        root.destroy()

if __name__ == "__main__":
    # 初期処理
    tree_folder = [['data/character','キャラクター'],['data/occupation','職種'],['data/space','場所'],['data/event','イベント'],['data/nobel','小説']]
    color=['sky blue','yellow green','gold','salmon','orange','red','hot pink','dark orchid','purple','midnight blue','light slate blue','dodger blue','dark turquoise','cadet blue','maroon','tan1','rosy brown','indian red']
    # Janomeを使って日本語の形態素解析
    tokenizer = Tokenizer()
    root = tk.Tk()
    app = LineFrame(root)
    root.title(u'小説エディタ')
    app.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))

    # 画像ファイルのbase 64データ
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
    root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(data=data))
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.mainloop()