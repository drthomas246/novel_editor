#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
import zipfile
import shutil
import webbrowser
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
import tkinter.filedialog as filedialog

import jaconv
from janome.tokenizer import Tokenizer

tree_folder = [['data/character','キャラクター'],['data/occupation','職種'],['data/space','場所'],['data/event','イベント'],['data/nobel','小説']]

# Janomeを使って日本語の形態素解析
tokenizer = Tokenizer()

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
        super().__init__(master, **kwargs)
        self.initialize()
        self.create_widgets()
        self.create_event()

    def initialize(self):
        """初期化処理"""
        self.now_path = ""
        self.file_path = ""
        self.last_text=""
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
        self.text = CustomText(self,font=("",18),undo=True)
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
        # テキストにフォーカスを当てる
        self.text.focus()

    def create_event(self):
        """イベントの設定."""
        # テキスト内でのスクロール時
        self.text.bind('<<Scroll>>', self.update_line_numbers)
        # テキストの変更時
        self.text.bind('<<Change>>', self.update_line_numbers)
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
        # 文字数と行数をカウントする
        self.text.bind('<Control-Shift-Key-C>', self.moji_count)
        # redo処理
        self.text.bind('<Control-Shift-Key-Z>', self.redo)
        # ツリービューをダブルクリックしたときにその項目を表示する
        self.tree.bind("<Double-1>", self.OnDoubleClick)
        # ツリービューで右クリックしたときにダイアログを表示する
        self.tree.bind("<Button-3>", self.message_window)

    def open_url(self,event=None):
        """小説家になろうのユーザーページを開く"""
        webbrowser.open("https://syosetu.com/user/top/")

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
            filepath, ___ = os.path.splitext(filepath)
            self.file_path = filepath
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
        self.sub_win = tk.Toplevel(self)
        self.sub_win.geometry("260x75")
        self.text_var = ttk.Entry(self.sub_win,width=40)
        self.text_var.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E,ipady=3)
        button = ttk.Button(
            self.sub_win,
            text = '検索',
            width = str('検索'),
            padding = (10, 5),
            command = self.search
            )
        button.grid(row=1, column=1)
        # 最前面に表示し続ける
        self.sub_win.attributes("-topmost", True)
        self.sub_win.title(u'検索')
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
        """ダイアログを表示する."""
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
        """ダイアログの実行ボタンが押されたとき."""
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

        # 条件によって分離
        sub_text = self.tree.item(curItem)["text"]
        path = ""
        for val in tree_folder:
            if text == val[1]:
                path = "./{0}/{1}.txt".format(val[0],sub_text)
                self.now_path = path
                self.text.focus()
                break

        # パスが存在すれば読み込んで表示する
        if not path == "":
            self.text.delete('1.0', tk.END)
            f = open(path)
            self.text.insert(tk.END, f.read())
            f.close()
            self.winfo_toplevel().title(u"小説エディタ\\{0}\\{1}".format(text,sub_text))

    def update_line_numbers(self,event=None):
        """行番号の描画."""
        # 現在の行番号を全て消す
        self.line_numbers.delete(tk.ALL)

        # Textの0, 0座標、つまり一番左上が何行目にあたるかを取得
        first_row = self.text.index('@0,0')
        first_row_number = int(first_row.split('.')[0])
        current = first_row_number
        while True:
            # dlineinfoは、その行がどの位置にあり、どんなサイズか、を返す
            # (3, 705, 197, 13, 18) のように帰る(x,y,width,height,baseline)
            dline = self.text.dlineinfo('{0}.0'.format(current))
            # dlineinfoに、存在しない行や、スクロールしないと見えない行を渡すとNoneが帰る
            if dline is None:
                break
            else:
                y = dline[1]  # y座標を取得

            # (x座標, y座標, 方向, 表示テキスト)を渡して行番号のテキストを作成
            self.line_numbers.create_text(3, y, anchor=tk.NW, text=current,font=("",12))
            current += 1

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

if __name__ == "__main__":
    root = tk.Tk()

    app = LineFrame(root)
    root.title(u'小説エディタ')
    app.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.E, tk.W))

    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.update()