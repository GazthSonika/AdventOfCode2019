def load(file, sep='\n'):
    with open(file, 'r') as f:
        if sep:
            return f.read().split(sep)
        return f.read()
        