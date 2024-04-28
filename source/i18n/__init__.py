#!/usr/bin/env python3
from . import llize
from . import data


def initialize(locate_var):
    """多言語化の初期処理.

    ・多言語化の初期処理をする。

    Args:
        locale_var (str): ロケーション

    Returns:
        instance: 多言語化のクラスのインスタンス
    """
    instance = llize.Localization(locate_var, "neditor.txt", data.TRANSLATION_DATA)
    return instance
