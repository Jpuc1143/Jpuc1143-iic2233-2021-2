class CsvDb:
    path = None
    data = []
    max_split = None

    def __init__(self, path, max_split=):
        self.path = path
        self.max_split = max_split

        file = open("r", path)
        for line in file:
            data.append(line.strip().split(",", max_split))
        file.close()

    def __del__(self):
        self.write()

    def write(self):
        # TODO: implement
        pass

