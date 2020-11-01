#!/usr/bin/env python3
from . import main


class EventProcessingClass(main.MainClass):
    """ウインドウイベントのクラス.

    ・ウインドウイベントにあるプログラム群

    Args:
        app (instance): MainProcessingClass のインスタンス
        locale_var (str): ロケーション
        master (instance): toplevel のインスタンス
    """
    def __init__(self, app, locale_var, master=None):
        super().__init__(locale_var, master)
        self.app = app

    def create_event_text(self):
        """テキストイベントの設定.

        ・テキストボックスにイベントを追加する。
        """
        # テキスト内でのスクロール時
        self.app.text.bind('<<Scroll>>', self.app.spc.update_line_numbers)
        self.app.text.bind('<Up>', self.app.spc.update_line_numbers)
        self.app.text.bind('<Down>', self.app.spc.update_line_numbers)
        self.app.text.bind('<Left>', self.app.spc.update_line_numbers)
        self.app.text.bind('<Right>', self.app.spc.update_line_numbers)
        # テキストの変更時
        self.app.text.bind('<<Change>>', self.app.spc.change_setting)
        # キー場押されたときの処理
        self.app.text.bind("<Any-KeyPress>", self.app.fpc.push_keys)
        # ウィジェットのサイズが変わった際。行番号の描画を行う
        self.app.text.bind('<Configure>', self.app.spc.update_line_numbers)
        # Tab押下時(インデント、又はコード補完)
        self.app.text.bind('<Tab>', self.app.cpc.tab)
        # ルビを振る
        self.app.text.bind('<Control-Key-r>', self.app.pmc.ruby_huri)
        # 開くダイアロクを表示する
        self.app.text.bind('<Control-Key-e>', self.app.fmc.open_file)
        # 保存ダイアロクを表示する
        self.app.text.bind('<Control-Key-w>', self.app.fmc.save_file)
        # 小説家になろうを開く
        self.app.text.bind(
            '<Control-Key-u>',
            self.app.pmc.open_becoming_novelist_page
        )
        # 検索ダイアログを開く
        self.app.text.bind('<Control-Key-f>', self.app.fpc.find_dialog)
        # 置換ダイアログを開く
        self.app.text.bind('<Control-Key-l>', self.app.fpc.replacement_dialog)
        # 上書き保存する
        self.app.text.bind('<Control-Key-s>', self.app.fmc.overwrite_save_file)
        # 新規作成する
        self.app.text.bind('<Control-Key-n>', self.app.fmc.new_open)
        # helpページを開く
        self.app.text.bind('<Control-Key-h>', self.app.hmc.help)
        # Versionページを開く
        self.app.text.bind('<Control-Shift-Key-V>', self.app.hmc.version)
        # 文字数と行数をカウントすShift-る
        self.app.text.bind('<Control-Shift-Key-C>', self.app.pmc.count_moji)
        # redo処理
        self.app.text.bind('<Control-Shift-Key-Z>', self.app.emc.redo)
        # uedo処理
        self.app.text.bind('<Control-Key-z>', self.app.emc.undo)
        # フォントサイズの変更
        self.app.text.bind('<Control-Shift-Key-F>', self.app.pmc.font_dialog)
        # 意味を検索
        self.app.text.bind(
            '<Control-Shift-Key-D>',
            self.app.pmc.find_wikipedia
        )
        # 文章を読み上げ
        self.app.text.bind('<Control-Shift-Key-R>', self.app.pmc.read_text)
        # yahoo文字列解析
        self.app.text.bind('<Control-Key-y>', self.app.pmc.yahoo)

    def create_event_character(self):
        """キャラクター欄のイベント設定.

        ・キャラクター関係のボックスにイベントを追加する。
        """
        # 開くダイアロクを表示する
        self.app.txt_yobi_name.bind('<Control-Key-e>', self.app.fmc.open_file)
        self.app.txt_name.bind('<Control-Key-e>', self.app.fmc.open_file)
        self.app.txt_birthday.bind('<Control-Key-e>', self.app.fmc.open_file)
        self.app.text_body.bind('<Control-Key-e>', self.app.fmc.open_file)
        # 保存ダイアロクを表示する
        self.app.txt_yobi_name.bind('<Control-Key-w>', self.app.fmc.save_file)
        self.app.txt_name.bind('<Control-Key-w>', self.app.fmc.save_file)
        self.app.txt_birthday.bind('<Control-Key-w>', self.app.fmc.save_file)
        self.app.text_body.bind('<Control-Key-w>', self.app.fmc.save_file)
        # 小説家になろうを開く
        self.app.txt_yobi_name.bind(
            '<Control-Key-u>',
            self.app.pmc.open_becoming_novelist_page
        )
        self.app.txt_name.bind(
            '<Control-Key-u>',
            self.app.pmc.open_becoming_novelist_page
        )
        self.app.txt_birthday.bind(
            '<Control-Key-u>',
            self.app.pmc.open_becoming_novelist_page
        )
        self.app.text_body.bind(
            '<Control-Key-u>',
            self.app.pmc.open_becoming_novelist_page
        )
        # 検索ダイアログを開く
        self.app.txt_yobi_name.bind(
            '<Control-Key-f>',
            self.app.fpc.find_dialog
        )
        self.app.txt_name.bind('<Control-Key-f>', self.app.fpc.find_dialog)
        self.app.txt_yobi_name.bind(
            '<Control-Key-f>',
            self.app.fpc.find_dialog
        )
        self.app.text_body.bind('<Control-Key-f>', self.app.fpc.find_dialog)
        # 上書き保存する
        self.app.txt_yobi_name.bind(
            '<Control-Key-s>',
            self.app.fmc.overwrite_save_file
        )
        self.app.txt_name.bind(
            '<Control-Key-s>',
            self.app.fmc.overwrite_save_file
        )
        self.app.txt_birthday.bind(
            '<Control-Key-s>',
            self.app.fmc.overwrite_save_file
        )
        self.app.text_body.bind(
            '<Control-Key-s>',
            self.app.fmc.overwrite_save_file
        )
        # 新規作成する
        self.app.txt_yobi_name.bind('<Control-Key-n>', self.app.fmc.new_open)
        self.app.txt_name.bind('<Control-Key-n>', self.app.fmc.new_open)
        self.app.txt_yobi_name.bind('<Control-Key-n>', self.app.fmc.new_open)
        self.app.text_body.bind('<Control-Key-n>', self.app.fmc.new_open)
        # helpページを開く
        self.app.txt_yobi_name.bind('<Control-Key-h>', self.app.hmc.help)
        self.app.txt_name.bind('<Control-Key-h>', self.app.hmc.help)
        self.app.txt_birthday.bind('<Control-Key-h>', self.app.hmc.help)
        self.app.text_body.bind('<Control-Key-h>', self.app.hmc.help)
        # Versionページを開く
        self.app.txt_yobi_name.bind(
            '<Control-Shift-Key-V>',
            self.app.hmc.version
        )
        self.app.txt_name.bind('<Control-Shift-Key-V>', self.app.hmc.version)
        self.app.txt_birthday.bind(
            '<Control-Shift-Key-V>',
            self.app.hmc.version
        )
        self.app.txt_yobi_name.bind(
            '<Control-Shift-Key-V>',
            self.app.hmc.version
        )
        # redo処理
        self.app.txt_yobi_name.bind('<Control-Shift-Key-Z>', self.app.emc.redo)
        self.app.txt_name.bind('<Control-Shift-Key-Z>', self.app.emc.redo)
        self.app.txt_birthday.bind('<Control-Shift-Key-Z>', self.app.emc.redo)
        self.app.text_body.bind('<Control-Shift-Key-Z>', self.app.emc.redo)
        # undo処理
        self.app.txt_yobi_name.bind('<Control-Key-z>', self.app.emc.undo)
        self.app.txt_name.bind('<Control-Key-z>', self.app.emc.undo)
        self.app.txt_birthday.bind('<Control-Key-z>', self.app.emc.undo)
        self.app.text_body.bind('<Control-Key-z>', self.app.emc.undo)
        # フォントサイズの変更
        self.app.txt_yobi_name.bind(
            '<Control-Shift-Key-F>',
            self.app.pmc.font_dialog
        )
        self.app.txt_name.bind(
            '<Control-Shift-Key-F>',
            self.app.pmc.font_dialog
        )
        self.app.txt_birthday.bind(
            '<Control-Shift-Key-F>',
            self.app.pmc.font_dialog
        )
        self.app.text_body.bind(
            '<Control-Shift-Key-F>',
            self.app.pmc.font_dialog
        )

    def create_event_image(self):
        """イメージイベントの設定.

        ・イメージキャンバスにイベントを追加する。
        """
        self.app.image_space.bind('<MouseWheel>', self.app.spc.mouse_y_scroll)
        self.app.image_space.bind(
            '<Control-MouseWheel>',
            self.app.spc.mouse_image_scroll
        )

    def create_event(self):
        """ツリービューイベントの設定.

        ・ツリービューにイベントを追加する。
        """
        # ツリービューをダブルクリックしたときにその項目を表示する
        self.app.tree.bind("<Double-1>", self.app.lmc.on_double_click)
        # ツリービューの名前を変更する
        self.app.tree.bind("<Control-Key-g>", self.app.lmc.on_name_click)
        # ツリービューで右クリックしたときにダイアログを表示する
        self.app.tree.bind("<Button-3>", self.app.lmc.message_window)
