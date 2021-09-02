def read_csv(path, max_split):
    data = []

    file = open(path, "r")
    for line in file:
        data.append(line.strip().split(",", max_split))

    return data

def write_csv(path):
    # TODO: implementar
    pass
