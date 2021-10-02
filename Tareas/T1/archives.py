from tribute import Tribute
from arena import Arena
from item import Consumable, Weapon, SpecialItem
from environment import Beach, Mountain, Forest


def load_tributes(path):
    tributes = {}
    file = open(path, "r")
    file.readline()
    for line in file:
        data = line.strip("\n").split(",")
        tributes[data[0]] = Tribute(data)

    file.close()
    return tributes

def load_arenas(path, parent):
    arenas = []
    file = open(path, "r")
    file.readline()
    for line in file:
        data = line.strip("\n").split(",")
        arenas.append(Arena(data[0], data[1], float(data[2]), parent))

    file.close()
    return arenas

def load_items(path):
    items = {}
    file = open(path, "r")
    file.readline()
    for line in file:
        data = line.strip("\n").split(",")
        if data[1] == "consumible":
            items[data[0]] = Consumable(data[0], int(data[2]))
        elif data[1] == "arma":
            items[data[0]] = Weapon(data[0], int(data[2]))
        elif data[1] == "especial":
            items[data[0]] = SpecialItem(data[0], int(data[2]))

    file.close()
    return items

def load_environments(path):
    environments = {}
    file = open(path, "r")
    file.readline()
    for line in file:
        data = line.strip("\n").split(",")
        events = {}
        for event in data[1:]:
            split_event = event.split(";")
            events[split_event[0]] = int(split_event[1])
        
        if data[0] == "playa":
            environment = Beach(events)
        if data[0] == "montaña":
            environment = Mountain(events)
        if data[0] == "bosque":
            environment = Forest(events)
        environments[environment.name] = environment

    file.close()
    return environments
