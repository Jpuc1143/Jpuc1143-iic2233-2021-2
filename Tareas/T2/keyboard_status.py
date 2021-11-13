class Keyboard:
    def __init__(self):
        self.status = dict()

    def __getitem__(self, key):
        return self.status.setdefault(key, False)

    def __setitem__(self, key, value):
        self.status[key] = value
