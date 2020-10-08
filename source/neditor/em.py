#!/usr/bin/env python3
class EditMenuClass():
    """編集メニューバーのクラス.

    ・編集メニューバーにあるプログラム群

    Args:
        app (instance): MainProcessingClass のインスタンス
    """
    def __init__(self, app):
        self.app = app

    def redo(self, event=None):
        """Redo.

        ・Redo処理を行う。

        Args:
            event (instance): tkinter.Event のインスタンス
        """
        self.app.text.edit_redo()

    def undo(self, event=None):
        """Undo.

        ・Uedo処理を行う。

        Args:
            event (instance): tkinter.Event のインスタンス
        """
        self.app.text.edit_undo()

    def copy(self, event=None):
        """Copy.

        ・Copy処理を行う。

        Args:
            event (instance): tkinter.Event のインスタンス
        """
        self.app.clipboard_clear()
        self.app.clipboard_append(self.app.text.selection_get())

    def cut(self, event=None):
        """Cut.

        ・Cut処理を行う。

        Args:
            event (instance): tkinter.Event のインスタンス
        """
        self.copy()
        self.app.text.delete("sel.first", "sel.last")

    def paste(self, event=None):
        """Paste.

        ・Paste処理を行う。

        Args:
            event (instance): tkinter.Event のインスタンス
        """
        self.app.text.insert('insert', self.app.clipboard_get())
