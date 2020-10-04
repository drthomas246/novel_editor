with open('.coverage') as f:
    t = f.read()

with open('.coverage', mode='w') as f:
    f.write(t)
