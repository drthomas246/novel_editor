import re

from janome.tokenizer import Tokenizer


class HighlightProcessingClass():
    """ハイライトのクラス

    ・ハイライトするためのプログラム群

    Args:
        app (instance): MainProcessingClassインスタンス
        tokenizer (instance): Tokenizerインスタンス

    """
    def __init__(self, app, tokenizer):
        self.COLOR = [
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
        self.APP = app
        self.TOKENIZER = tokenizer

    def all_highlight(self):
        """全てハイライト

        ・開く処理等の時にすべての行をハイライトする。

        """
        # 全てのテキストを取得
        src = self.APP.text.get('1.0', 'end - 1c')
        # 全てのハイライトを一度解除する
        for tag in self.APP.text.tag_names():
            self.APP.text.tag_remove(tag, '1.0', 'end')

        # ハイライトする
        self.highlight('1.0', src, 'end')

    def line_highlight(self, replacement_check, find_text, next_pos):
        """現在行だけハイライト

        ・入力等の変更時に現在の行のみをハイライトする。

        Args:
            replacement_check (bool): 検索ダイアログが表示されているTrue
            find_text (str): 検索文字列
            next_pos (str): 検索位置 例.(1.0)

        """
        start = 'insert linestart'
        end = 'insert lineend'
        # 現在行のテキストを取得
        src = self.APP.text.get(start, end)
        # その行のハイライトを一度解除する
        for tag in self.APP.text.tag_names():
            self.APP.text.tag_remove(tag, start, end)

        # ハイライトする
        self.highlight(start, src, end)
        # 置換処理時に選択する
        if replacement_check == 1:
            start = next_pos
            end = '{0} + {1}c'.format(next_pos, len(find_text))
            self.APP.text.tag_add('sel', start, end)

    def highlight(self, start, src, end):
        """ハイライトの共通処理

        ・ハイライトする文字が見つかったらハイライト処理をする。
        先頭の文字が全角スペースならば、一文字ずらしてハイライトする。

        Args:
            start (str): はじめの位置 例.(1.0)
            src (str): ハイライトする文章
            end (str): 終わりの位置

        """
        self.create_tags()
        self.APP.text.mark_set('range_start', start)
        space_count = re.match(r"\u3000*", self.APP.text.get(start, end)).end()
        # 形態素解析を行う
        for token in self.t.tokenize(src):
            content = token.surface
            self.APP.text.mark_set(
                'range_end', 'range_start+{0}c'
                .format(len(content))
            )
            # 全角スペースの時はずらす
            if space_count > 0:
                self.APP.text.tag_add(
                    content,
                    'range_start+{0}c'.format(space_count),
                    'range_end+{0}c'.format(space_count)
                )
            else:
                self.APP.text.tag_add(content, 'range_start', 'range_end')
            self.APP.text.mark_set('range_start', 'range_end')

    def create_tags(self):
        """タグの作成

        ・キャラクターの名前をJanomeの形態素解析にかかるようにする。
        キャラクターの名前を色付きにする。

        """
        i = 0
        system_dic = u"喜寛,固有名詞,ヨシヒロ"
        # キャラクターから一覧を作る。
        children = self.APP.tree.get_children('data/character')
        for child in children:
            # ユーザー定義辞書の設定
            reading = ""
            childname = self.APP.tree.item(child, "text")
            for token in self.TOKENIZER.tokenize(childname):
                reading += token.phonetic
            system_dic += u"\n{0},固有名詞,{1}".format(childname, reading)
            # タグの作成
            self.APP.text.tag_configure(
                childname,
                foreground=self.COLOR[i % len(self.COLOR)],
                font=(self.APP.font, self.APP.pmc.font_size, "bold")
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
