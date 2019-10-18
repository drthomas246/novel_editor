import os
import glob
import zipfile
import tkinter.filedialog as filedialog
import shutil

tree_folder = [['data/character','キャラクター'],['data/occupation','職種'],['data/space','場所'],['data/event','イベント'],['data/nobel','小説']]

fTyp = [("小説エディタ",".ned")]
iDir = os.path.abspath(os.path.dirname(__file__))
filepath = filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
# ファイル名があるとき
if not filepath == "":
    with zipfile.ZipFile(filepath) as existing_zip:
        existing_zip.extractall('./data')

    for val in tree_folder:
        files=glob.glob("{0}/*".format(val[0]))
        for file in files:
            if val[0] == tree_folder[0][0]:
                f = open(file, 'r', encoding='shift-jis')
                text_text=f.read()
                text_text='<?xml version="1.0"?>\n<data>\n\t<call></call>\n\t<name></name>\n\t<sex>0</sex>\n\t<birthday></birthday>\n\t<body>{0}</body>\n</data>'.format(text_text)
                f.close()
                f = open(file, 'w', encoding='utf-8')
                f.write(text_text)
                f.close()
            else:
                f = open(file, 'r', encoding='shift-jis')
                text_text=f.read()
                f.close()
                f = open(file, 'w', encoding='utf-8')
                f.write(text_text)
            f.close()
    shutil.make_archive(filepath,"zip","./data")
            # 拡張子の変更を行う
    shutil.move("{0}.zip".format(filepath),"{0}.ned".format(filepath))