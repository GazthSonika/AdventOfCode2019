def load(file, sep='\n'):
    with open(file, 'r') as f:
        return f.read().split(sep)
        