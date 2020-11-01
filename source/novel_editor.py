#!/usr/bin/env python3
import locale

import neditor


if __name__ == "__main__":
    # 多言語化処理
    locale_var = locale.getdefaultlocale()
    # タイトルを表示する
    root = neditor.main_window_create(locale_var)
    # ループする
    root.mainloop()
