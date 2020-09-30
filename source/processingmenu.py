import webbrowser
import tkinter.messagebox as messagebox


class ProcessingMenuClass():
    def __init__(self, app):
        self.APP = app

    def find_wikipedia(self, wiki_wiki):
        """意味を検索

        ・Wikipedia-APIライブラリを使ってWikipediaから選択文字の意味を
        検索する。

        Args:
            wiki_wiki (instance): Wikipedia-APIのインスタンス

        """
        # wikipediaから
        select_text = self.APP.text.selection_get()
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

    def open_becoming_novelist_page(self):
        """小説家になろうのユーザーページを開く

        ・インターネットブラウザで小説家になろうのユーザーページを開く。

        """
        webbrowser.open("https://syosetu.com/user/top/")
