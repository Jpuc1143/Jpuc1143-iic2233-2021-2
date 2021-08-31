def readCsv(path, max_split):
    data = []

    file = open(path, "r")
    for line in file:
        data.append(line.strip().split(",", max_split))

    return data

def writeCsv(path):
    # TODO: implementar
    pass
