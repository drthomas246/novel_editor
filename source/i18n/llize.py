#!/usr/bin/env python3
import os
import ast


class Localization:
    """多言語化のクラス.

    ・多言語化にあるプログラム群

    Args:
        locale_var (str): ロケーション
        FILE_NAME (str): ファイル名
        TRANSLATION_DATA (str): 翻訳データ
    """

    def __init__(self, locale_var, FILE_NAME, TRANSLATION_DATA):
        path_to_locale_dir = os.path.abspath(
            os.path.join(os.getcwd(), "./locale/{0}/".format(locale_var[0]))
        )
        if os.path.exists(path_to_locale_dir) is False:
            os.makedirs(path_to_locale_dir)
            with open(
                "{0}/{1}".format(path_to_locale_dir, FILE_NAME),
                encoding="utf-8",
                mode="w",
            ) as f:
                f.write(TRANSLATION_DATA)

        with open(
            "{0}/{1}".format(path_to_locale_dir, FILE_NAME), encoding="utf-8"
        ) as f:
            l_strip = f.read()

        self.dic = ast.literal_eval(l_strip)

    def get_dict(self, list):
        """翻訳結果の取得の処理.

        ・翻訳結果を取得し返す。なければデフォルト値を返す。

        Args:
            list (str): デフォルト値

        Returns:
            str: 翻訳結果
        """
        if self.dic[list]:
            dic = self.dic[list]
        else:
            dic = list

        return dic
