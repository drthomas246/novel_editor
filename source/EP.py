#!/usr/bin/env python3
class EventProcessingClass():
    """ウインドウイベントのクラス.

    ・ウインドウイベントにあるプログラム群

    Args:
        app (instance): MainProcessingClassインスタンス

    """
    def __init__(self, app):
        self.APP = app

    def create_event_text(self):
        """テキストイベントの設定.

        ・テキストボックスにイベントを追加する。

        """
        # テキスト内でのスクロール時
        self.APP.text.bind('<<Scroll>>', self.APP.sfc.update_line_numbers)
        self.APP.text.bind('<Up>', self.APP.sfc.update_line_numbers)
        self.APP.text.bind('<Down>', self.APP.sfc.update_line_numbers)
        self.APP.text.bind('<Left>', self.APP.sfc.update_line_numbers)
        self.APP.text.bind('<Right>', self.APP.sfc.update_line_numbers)
        # テキストの変更時
        self.APP.text.bind('<<Change>>', self.APP.sfc.change_setting)
        # キー場押されたときの処理
        self.APP.text.bind("<Any-KeyPress>", self.APP.fpc.push_keys)
        # ウィジェットのサイズが変わった際。行番号の描画を行う
        self.APP.text.bind('<Configure>', self.APP.sfc.update_line_numbers)
        # Tab押下時(インデント、又はコード補完)
        self.APP.text.bind('<Tab>', self.APP.cpc.tab)
        # ルビを振る
        self.APP.text.bind('<Control-Key-r>', self.APP.pmc.ruby_huri)
        # 開くダイアロクを表示する
        self.APP.text.bind('<Control-Key-e>', self.APP.fmc.open_file)
        # 保存ダイアロクを表示する
        self.APP.text.bind('<Control-Key-w>', self.APP.fmc.save_file)
        # 小説家になろうを開く
        self.APP.text.bind(
            '<Control-Key-u>',
            self.APP.pmc.open_becoming_novelist_page
        )
        # 検索ダイアログを開く
        self.APP.text.bind('<Control-Key-f>', self.APP.fpc.find_dialog)
        # 置換ダイアログを開く
        self.APP.text.bind('<Control-Key-l>', self.APP.fpc.replacement_dialog)
        # 上書き保存する
        self.APP.text.bind('<Control-Key-s>', self.APP.fmc.overwrite_save_file)
        # 新規作成する
        self.APP.text.bind('<Control-Key-n>', self.APP.fmc.new_open)
        # helpページを開く
        self.APP.text.bind('<Control-Key-h>', self.APP.hmc.help)
        # Versionページを開く
        self.APP.text.bind('<Control-Shift-Key-V>', self.APP.hmc.version)
        # 文字数と行数をカウントすShift-る
        self.APP.text.bind('<Control-Shift-Key-C>', self.APP.pmc.count_moji)
        # redo処理
        self.APP.text.bind('<Control-Shift-Key-Z>', self.APP.emc.redo)
        # uedo処理
        self.APP.text.bind('<Control-Key-z>', self.APP.emc.undo)
        # フォントサイズの変更
        self.APP.text.bind('<Control-Shift-Key-F>', self.APP.pmc.font_dialog)
        # 意味を検索
        self.APP.text.bind(
            '<Control-Shift-Key-D>',
            self.APP.pmc.find_wikipedia
        )
        # 文章を読み上げ
        self.APP.text.bind('<Control-Shift-Key-R>', self.APP.pmc.read_text)
        # yahoo文字列解析
        self.APP.text.bind('<Control-Key-y>', self.APP.pmc.yahoo)

    def create_event_character(self):
        """キャラクター欄のイベント設定.

        ・キャラクター関係のボックスにイベントを追加する。

        """
        # 開くダイアロクを表示する
        self.APP.txt_yobi_name.bind('<Control-Key-e>', self.APP.fmc.open_file)
        self.APP.txt_name.bind('<Control-Key-e>', self.APP.fmc.open_file)
        self.APP.txt_birthday.bind('<Control-Key-e>', self.APP.fmc.open_file)
        self.APP.text_body.bind('<Control-Key-e>', self.APP.fmc.open_file)
        # 保存ダイアロクを表示する
        self.APP.txt_yobi_name.bind('<Control-Key-w>', self.APP.fmc.save_file)
        self.APP.txt_name.bind('<Control-Key-w>', self.APP.fmc.save_file)
        self.APP.txt_birthday.bind('<Control-Key-w>', self.APP.fmc.save_file)
        self.APP.text_body.bind('<Control-Key-w>', self.APP.fmc.save_file)
        # 小説家になろうを開く
        self.APP.txt_yobi_name.bind(
            '<Control-Key-u>',
            self.APP.pmc.open_becoming_novelist_page
        )
        self.APP.txt_name.bind(
            '<Control-Key-u>',
            self.APP.pmc.open_becoming_novelist_page
        )
        self.APP.txt_birthday.bind(
            '<Control-Key-u>',
            self.APP.pmc.open_becoming_novelist_page
        )
        self.APP.text_body.bind(
            '<Control-Key-u>',
            self.APP.pmc.open_becoming_novelist_page
        )
        # 検索ダイアログを開く
        self.APP.txt_yobi_name.bind(
            '<Control-Key-f>',
            self.APP.fpc.find_dialog
        )
        self.APP.txt_name.bind('<Control-Key-f>', self.APP.fpc.find_dialog)
        self.APP.txt_yobi_name.bind(
            '<Control-Key-f>',
            self.APP.fpc.find_dialog
        )
        self.APP.text_body.bind('<Control-Key-f>', self.APP.fpc.find_dialog)
        # 上書き保存する
        self.APP.txt_yobi_name.bind(
            '<Control-Key-s>',
            self.APP.fmc.overwrite_save_file
        )
        self.APP.txt_name.bind(
            '<Control-Key-s>',
            self.APP.fmc.overwrite_save_file
        )
        self.APP.txt_birthday.bind(
            '<Control-Key-s>',
            self.APP.fmc.overwrite_save_file
        )
        self.APP.text_body.bind(
            '<Control-Key-s>',
            self.APP.fmc.overwrite_save_file
        )
        # 新規作成する
        self.APP.txt_yobi_name.bind('<Control-Key-n>', self.APP.fmc.new_open)
        self.APP.txt_name.bind('<Control-Key-n>', self.APP.fmc.new_open)
        self.APP.txt_yobi_name.bind('<Control-Key-n>', self.APP.fmc.new_open)
        self.APP.text_body.bind('<Control-Key-n>', self.APP.fmc.new_open)
        # helpページを開く
        self.APP.txt_yobi_name.bind('<Control-Key-h>', self.APP.hmc.help)
        self.APP.txt_name.bind('<Control-Key-h>', self.APP.hmc.help)
        self.APP.txt_birthday.bind('<Control-Key-h>', self.APP.hmc.help)
        self.APP.text_body.bind('<Control-Key-h>', self.APP.hmc.help)
        # Versionページを開く
        self.APP.txt_yobi_name.bind(
            '<Control-Shift-Key-V>',
            self.APP.hmc.version
        )
        self.APP.txt_name.bind('<Control-Shift-Key-V>', self.APP.hmc.version)
        self.APP.txt_birthday.bind(
            '<Control-Shift-Key-V>',
            self.APP.hmc.version
        )
        self.APP.txt_yobi_name.bind(
            '<Control-Shift-Key-V>',
            self.APP.hmc.version
        )
        # redo処理
        self.APP.txt_yobi_name.bind('<Control-Shift-Key-Z>', self.APP.emc.redo)
        self.APP.txt_name.bind('<Control-Shift-Key-Z>', self.APP.emc.redo)
        self.APP.txt_birthday.bind('<Control-Shift-Key-Z>', self.APP.emc.redo)
        self.APP.text_body.bind('<Control-Shift-Key-Z>', self.APP.emc.redo)
        # undo処理
        self.APP.txt_yobi_name.bind('<Control-Key-z>', self.APP.emc.undo)
        self.APP.txt_name.bind('<Control-Key-z>', self.APP.emc.undo)
        self.APP.txt_birthday.bind('<Control-Key-z>', self.APP.emc.undo)
        self.APP.text_body.bind('<Control-Key-z>', self.APP.emc.undo)
        # フォントサイズの変更
        self.APP.txt_yobi_name.bind(
            '<Control-Shift-Key-F>',
            self.APP.pmc.font_dialog
        )
        self.APP.txt_name.bind(
            '<Control-Shift-Key-F>',
            self.APP.pmc.font_dialog
        )
        self.APP.txt_birthday.bind(
            '<Control-Shift-Key-F>',
            self.APP.pmc.font_dialog
        )
        self.APP.text_body.bind(
            '<Control-Shift-Key-F>',
            self.APP.pmc.font_dialog
        )

    def create_event_image(self):
        """イメージイベントの設定.

        ・イメージキャンバスにイベントを追加する。

        """
        self.APP.image_space.bind('<MouseWheel>', self.APP.sfc.mouse_y_scroll)
        self.APP.image_space.bind(
            '<Control-MouseWheel>',
            self.APP.sfc.mouse_image_scroll
        )

    def create_event(self):
        """ツリービューイベントの設定.

        ・ツリービューにイベントを追加する。

        """
        # ツリービューをダブルクリックしたときにその項目を表示する
        self.APP.tree.bind("<Double-1>", self.APP.lmc.on_double_click)
        # ツリービューの名前を変更する
        self.APP.tree.bind("<Control-Key-g>", self.APP.lmc.on_name_click)
        # ツリービューで右クリックしたときにダイアログを表示する
        self.APP.tree.bind("<Button-3>", self.APP.lmc.message_window)
