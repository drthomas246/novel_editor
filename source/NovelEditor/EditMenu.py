#!/usr/bin/env python3
from . import Definition


class EditMenuClass(Definition.DefinitionClass):
    """編集メニューバーのクラス.

    ・編集メニューバーにあるプログラム群

    Args:
        app (instance): MainProcessingClass のインスタンス
        locale_var (str): ロケーション
        master (instance): toplevel のインスタンス
    """

    def __init__(self, app, locale_var, master=None):
        super().__init__(locale_var, master)
        self.app = app

    def redo(self, event=None):
        """Redo.

        ・Redo処理を行う。

        Args:
            event (instance): tkinter.Event のインスタンス
        """
        self.app.NovelEditor.edit_redo()

    def undo(self, event=None):
        """Undo.

        ・Uedo処理を行う。

        Args:
            event (instance): tkinter.Event のインスタンス
        """
        self.app.NovelEditor.edit_undo()

    def copy(self, event=None):
        """Copy.

        ・Copy処理を行う。

        Args:
            event (instance): tkinter.Event のインスタンス
        """
        self.app.clipboard_clear()
        self.app.clipboard_append(self.app.NovelEditor.selection_get())

    def cut(self, event=None):
        """Cut.

        ・Cut処理を行う。

        Args:
            event (instance): tkinter.Event のインスタンス
        """
        self.copy()
        self.app.NovelEditor.delete("sel.first", "sel.last")

    def paste(self, event=None):
        """Paste.

        ・Paste処理を行う。

        Args:
            event (instance): tkinter.Event のインスタンス
        """
        self.app.NovelEditor.insert("insert", self.app.clipboard_get())
