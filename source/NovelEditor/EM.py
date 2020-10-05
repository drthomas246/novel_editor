#!/usr/bin/env python3
class EditMenuClass():
    """編集メニューバーのクラス.

    ・編集メニューバーにあるプログラム群

    Args:
        app (instance): MainProcessingClass のインスタンス
    """
    def __init__(self, app):
        self.APP = app

    def redo(self, event=None):
        """Redo.

        ・Redo処理を行う。

        Args:
            event (instance): tkinter.Event のインスタンス
        """
        self.APP.text.edit_redo()

    def undo(self, event=None):
        """Undo.

        ・Uedo処理を行う。

        Args:
            event (instance): tkinter.Event のインスタンス
        """
        self.APP.text.edit_undo()

    def copy(self, event=None):
        """Copy.

        ・Copy処理を行う。

        Args:
            event (instance): tkinter.Event のインスタンス
        """
        self.APP.clipboard_clear()
        self.APP.clipboard_append(self.APP.text.selection_get())

    def cut(self, event=None):
        """Cut.

        ・Cut処理を行う。

        Args:
            event (instance): tkinter.Event のインスタンス
        """
        self.copy()
        self.APP.text.delete("sel.first", "sel.last")

    def paste(self, event=None):
        """Paste.

        ・Paste処理を行う。

        Args:
            event (instance): tkinter.Event のインスタンス
        """
        self.APP.text.insert('insert', self.APP.clipboard_get())
