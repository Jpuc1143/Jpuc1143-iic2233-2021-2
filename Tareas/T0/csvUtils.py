def read_csv(path, max_split):
    data = []

    file = open(path, "r")
    for line in file:
        data.append(line.strip().split(",", max_split))

    return data

def write_csv(path, data):
    file = open(path, "r")    
    header = file.readline()
    file.close()

    file = open(path, "w")
    file.write(header)

    if type(data) is dict:
        for key in data:
            for comment in data[key]:
                file.write(",".join(comment) + "\n")
    else:
        for line in data:
            file.write(",".join(line) + "\n")

    file.close()
