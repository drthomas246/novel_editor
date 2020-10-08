#!/usr/bin/env python3
from . import llize


def initialize(locate_var):
    """多言語化の初期処理.

    ・多言語化の初期処理をする。

    Args:
        locale_var (str): ロケーション

    Returns:
        instance: 多言語化のクラスのインスタンス
    """
    instance = llize.Localization(locate_var, NEDITOR)
    return instance


NEDITOR = '''{
    "Novel Editor" : "",
    "Character" : "",
    "Occupation" : "" ,
    "Space" : "" ,
    "Event" : "" ,
    "Image" : "" ,
    "Novel" : "",
    "Newfile" : "" ,
    "Open" : "" ,
    "Save" : "" ,
    "Save as" : "" ,
    "Close" : "" ,
    "File" : "" ,
    "Redo" : "" ,
    "Undo" : "" ,
    "Cut" : "" ,
    "Copy" : "" ,
    "Paste" : "" ,
    "Find" : "" ,
    "Replacement" : "" ,
    "Edit" : "" ,
    "Ruby" : "" ,
    "Count charactors" : "" ,
    "Meaning of letters" : "" ,
    "Read aloud" : "" ,
    "Sentence structure" : "" ,
    "Font size" : "" ,
    "Open [Become a Novelist]" : "" ,
    "Processing" : "" ,
    "Increase item" : "" ,
    "Delete item" : "" ,
    "Rename item" : "" ,
    "Item" : "" ,
    "Help" : "" ,
    "Version" : "" ,
    "Call name" : "" ,
    "Name" : "" ,
    "Sex" : "" ,
    "Man" : "" ,
    "Woman" : "" ,
    "Other" : "" ,
    "Portrait" : "" ,
    "Birthday" : "" ,
    "Insert" : "" ,
    "Delete" : "" ,
    "Biography" : "" ,
    "Double startup is not possible." : "" ,
    "Select and right click" : "" ,
    "Do you want to overwrite?" : "" ,
    "Do you want to discard the current edit and create a new one?" : "" ,
    "Can I quit?" : "" ,
    "Change" : "" ,
    "Rename {0}" : "" ,
    "Novel Editor/{0}/{1}" : "" ,
    "Delete {0} item?" : "" ,
    "Number of characters etc" : "" ,
    "Characters : {0} Lines : {1}\\n Manuscript papers : {2}" : "" ,
    "Meaning of [{0}]" : "" ,
    "Can't find." : "" ,
    "gif image" : "" ,
    "Cancel" : "" ,
    "Yahoo! Client ID" : "" ,
    "Yahoo! Client ID is not find.\\nRead Readme.pdf and set it again." : "" ,
    "Insert in {0}" : "" ,
    "Asc find" : "" ,
    "Stop" : "" ,
    "Resize" : "" ,
}'''
