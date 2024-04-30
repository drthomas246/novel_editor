#!/usr/bin/env python3
import sys
import os

sys.path.append(os.getcwd())

import NovelEditor
import locale


class StartProsess:
    """スタートプロセスクラス.

    ・一番初めに開かれるクラス
    """

    if __name__ == "__main__":
        # 多言語化処理
        locale_var = locale.getlocale()
        # タイトルを表示する
        root = NovelEditor.main_window_create(locale_var)
        # ループする
        root.mainloop()


StartProsess()
