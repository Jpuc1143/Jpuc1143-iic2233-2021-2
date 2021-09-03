def read_csv(path, max_split):
    data = []

    file = open(path, "r", encoding="utf-8")
    for line in file:
        if line == "\n":
            data.append(None)
        else:
            data.append(line.strip().split(",", max_split))

    return data


def write_csv(path, data):
    file = open(path, "r", encoding="utf-8")
    header = file.readline()
    file.close()

    file = open(path, "w", encoding="utf-8")
    file.write(header)

    # Yo: Mamá podemos tener polimorfismo hoy día?
    # Mamá: pero si ya tenemos polimorfismo en casa
    # Polimorfismo en casa:
    if type(data) is dict:
        for key in data:
            for comment in data[key]:
                file.write(",".join(comment) + "\n")

    elif type(data) is set:
        for line in data:
            file.write(line + "\n")

    else:
        for line in data:
            if line is None:
                file.write("\n")
            else:
                file.write(",".join(line) + "\n")

    file.close()
