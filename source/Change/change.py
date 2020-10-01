import os
import glob
import zipfile
import tkinter.filedialog as filedialog
import shutil
import tkinter.ttk as ttk
import tkinter as tk

tree_folder = [['data/character','キャラクター'],['data/occupation','職種'],['data/space','場所'],['data/event','イベント'],['data/nobel','小説']]

def sub_name_OK():
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
                f = open(file, 'r', encoding='shift-jis')
                text_text=f.read()
                f.close()
                if val[0] == tree_folder[0][0]:
                    title,___=os.path.splitext(os.path.basename(file))
                    text_text='<?xml version="1.0"?>\n<data>\n\t<call>{0}</call>\n\t<name></name>\n\t<sex>0</sex>\n\t<birthday></birthday>\n\t<body>{1}</body>\n</data>'.format(title,text_text)
                f = open(file, 'w', encoding='utf-8')
                f.write(text_text)
                f.close()
        shutil.make_archive(filepath,"zip","./data")
                # 拡張子の変更を行う
        shutil.move("{0}.zip".format(filepath),"{0}".format(filepath))
        label1=tk.Label(root,text=u"変換終了")
        label1.grid(row=1, column=0)





root = tk.Tk()
button = ttk.Button(
            root,
            text = "変換",
            width = str("変換"),
            padding = (10, 5),
            command = sub_name_OK
        )
button.grid(row=0, column=0)
root.mainloop()
