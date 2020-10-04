with open('.coverage') as f:
    t = f.read()
    s = t.replace(
        'C:\\\\Users\\\\drtho\\\\github\\\\novel_editor\\\\source\\\\',
        "/home/scrutinizer/build/source/"
    )

with open('.coverage', mode='w') as f:
    f.write(s)
