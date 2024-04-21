#!/usr/bin/env python3
import sys
import os

sys.path.append(os.getcwd())

import neditor
import locale


if __name__ == "__main__":
    # 多言語化処理
    locale_var = locale.getlocale()
    # タイトルを表示する
    root = neditor.main_window_create(locale_var)
    # ループする
    root.mainloop()
