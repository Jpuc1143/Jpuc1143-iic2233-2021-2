from copy import copy
from datetime import datetime
from enums import Menu

from arena import Arena
import parametros as p
import archives


class DCCapitolio:
    def __init__(self):
        self.available_tributes = archives.load_tributes(p.PATH_TRIBUTES)
        self.available_environments = archives.load_environments(p.PATH_ENVIRONMENTS)
        self.available_items = archives.load_items(p.PATH_ITEMS)
        self.available_arenas = archives.load_arenas(p.PATH_ARENAS, self)

        self.arena = None

        self.menu_state = Menu.START
        self.menu_options = {}

        self.saved_games = []

    def main_loop(self):
        user_input = None
        while True:
            if self.menu_state == Menu.START:
                self.load_list(p.PATH_SAVES)
                print("Bienvenidos Tributos a los Juegos de DCCapitolio!")
                print("Menu de Inicio")

                self.menu_options = {
                    "a": ("Entrar a DCCapitolio", Menu.CHOOSE_TRIBUTE),
                    "s": ("Cargar partida existente", Menu.LOAD_MENU),
                    "q": ("Salir", Menu.EXIT)
                        }

            elif self.menu_state == Menu.EXIT:
                return

            elif self.menu_state == Menu.CHOOSE_TRIBUTE:
                print("Elija su tributo:")
                self.menu_options = {}
                for number, tribute in enumerate(self.available_tributes.values(), start=1):
                    self.menu_options[str(number)] = \
                        (tribute.name + " de " + tribute.district,
                         Menu.SHOW_CANDIDATE_TRIBUTE, tribute)

                self.menu_options["w"] = ("Volver", Menu.START)
                self.menu_options["q"] = ("Salir de DCCapitolio", Menu.EXIT)

            elif self.menu_state == Menu.SHOW_CANDIDATE_TRIBUTE:
                player_tribute = copy(self.menu_options[user_input][2])
                self.menu_state = Menu.CONFIRM_TRIBUTE
                continue

            elif self.menu_state == Menu.CONFIRM_TRIBUTE:
                print(player_tribute)
                print("¿Este es su tributo?")

                self.menu_options = {
                    "a": ("Sí", Menu.CHOOSE_ARENA),
                    "w": ("Volver", Menu.CHOOSE_TRIBUTE),
                    "q": ("Salir de DCCapitolio", Menu.EXIT)
                        }

            elif self.menu_state == Menu.CHOOSE_ARENA:
                print("Elija la arena para pelear:")
                self.menu_options = {}
                for number, arena in enumerate(self.available_arenas.values(), start=1):
                    self.menu_options[str(number)] = \
                        (f"{arena.name} ({arena.difficulty})", Menu.NEW_ARENA, arena)

                self.menu_options["w"] = ("Volver", Menu.CHOOSE_TRIBUTE)
                self.menu_options["q"] = ("Salir de DCCapitolio", Menu.EXIT)

            elif self.menu_state == Menu.NEW_ARENA:
                self.arena = copy(self.menu_options[user_input][2])
                self.arena.player_tribute = player_tribute
                self.arena.player_tribute.arena = self.arena

                self.arena.choose_tributes()

                self.arena.save_id = len(self.saved_games)
                self.save(self.arena, p.PATH_SAVES)
                print(self.arena)
                self.menu_state = Menu.MAIN
                continue

            elif self.menu_state == Menu.LOAD_MENU:
                print("Elija su partida:")
                self.menu_options = {}
                for number, save in enumerate(self.saved_games, start=1):
                    name = self.saved_games[number-1][1].split(",")[3]
                    time = self.saved_games[number-1][1].split(";")[0].split(",")[4]
                    date = self.saved_games[number-1][0]
                    self.menu_options[str(number)] = (f"{name}, sobrevivido {time} horas ({date})",
                                                      Menu.LOAD)
                self.menu_options["x"] = ("Borrar partida", Menu.DELETE_MENU)
                self.menu_options["w"] = ("Volver", Menu.START)
                self.menu_options["q"] = ("Salir de DCCapitolio", Menu.EXIT)

            elif self.menu_state == Menu.LOAD:
                self.arena = Arena("a", "a", 1, self)
                save_id = int(user_input) - 1
                self.arena.deserialize(self.saved_games[save_id][1], save_id, self)
                print("Partida cargada exitosamente")
                self.menu_state = Menu.MAIN
                continue

            elif self.menu_state == Menu.DELETE_MENU:
                print("Elija la partida para borrar:")
                self.menu_options = {}
                for number, save in enumerate(self.saved_games, start=1):
                    name = self.saved_games[number-1][1].split(",")[3]
                    time = self.saved_games[number-1][1].split(";")[0].split(",")[4]
                    date = self.saved_games[number-1][0]
                    self.menu_options[str(number)] = (f"{name}, sobrevivido {time} horas ({date})",
                                                      Menu.DELETE)
                self.menu_options["w"] = ("Volver", Menu.LOAD_MENU)
                self.menu_options["q"] = ("Salir de DCCapitolio", Menu.EXIT)

            elif self.menu_state == Menu.DELETE:
                self.delete_save(int(user_input)-1, p.PATH_SAVES)
                self.load_list(p.PATH_SAVES)
                print("Partida borrada exitosamente")
                self.menu_state = Menu.LOAD_MENU
                continue

            elif self.menu_state == Menu.MAIN:
                print("Menu Principal")

                self.menu_options = {
                    "1": ("Simulación de hora", Menu.ACTIONS),
                    "2": ("Mostrar estado del tributo", Menu.STATUS),
                    "3": ("Utilizar objeto", Menu.INVENTORY),
                    "4": ("Resumen DCCapitolio", Menu.SUMMARY),
                    "w": ("Volver", Menu.START),
                    "q": ("Salir de DCCapitolio", Menu.EXIT)
                        }

            elif self.menu_state == Menu.ACTIONS:
                print(f"¿Que va a hacer {self.arena.player_tribute.name}?")

                self.menu_options = {
                    "1": ("Acción heroica", Menu.HEROIC),
                    "2": ("Atacar a un tributo", Menu.CHOOSE_TARGET),
                    "3": ("Pedir objeto a patrocinadores", Menu.BEG),
                    "4": ("Hacerse bolita", Menu.BALL_MODE),
                    "5": ("Rendirse", Menu.FORFEIT),
                    "w": ("Volver", Menu.MAIN),
                    "q": ("Salir de DCCapitolio", Menu.EXIT)
                        }

            elif self.menu_state == Menu.FORFEIT:
                print(f"{self.arena.player_tribute.name} ha decidido rendirse")
                self.arena.player_tribute.health = 0
                self.arena.closing_ceremony()
                self.delete_save(self.arena.save_id, p.PATH_SAVES)
                self.menu_state = Menu.START
                continue

            elif self.menu_state == Menu.HEROIC:
                if self.arena.player_tribute.heroic_action():
                    self.menu_state = Menu.SIMULATE
                else:
                    self.menu_state = Menu.ACTIONS
                continue

            elif self.menu_state == Menu.CHOOSE_TARGET:
                self.menu_options = {}
                for number, tribute in enumerate(self.arena.tributes_alive.values()):
                    if tribute.name != self.arena.player_tribute.name:
                        self.menu_options[str(number)] = (tribute.name, Menu.ATTACK)
                self.menu_options["w"] = ("Volver", Menu.MAIN)
                self.menu_options["q"] = ("Salir de DCCapitolio", Menu.EXIT)

            elif self.menu_state == Menu.ATTACK:
                print("Elija a su oponente:")
                target = self.arena.tributes[self.menu_options[user_input][0]]
                self.arena.player_tribute.attack(target)
                self.menu_state = Menu.SIMULATE
                continue

            elif self.menu_state == Menu.BEG:
                if self.arena.player_tribute.request_item():
                    self.menu_state = Menu.SIMULATE
                else:
                    self.menu_state = Menu.ACTIONS
                continue

            elif self.menu_state == Menu.BALL_MODE:
                self.arena.player_tribute.bakugan_mode()
                self.menu_state = Menu.SIMULATE
                continue

            elif self.menu_state == Menu.SIMULATE:
                print("")
                if self.arena.simulate():
                    print(f"\nHoras transcurridas: {self.arena.time}")
                    self.save(self.arena, p.PATH_SAVES)
                    print("La partida ha sido auto-guardada")
                    self.menu_state = Menu.MAIN
                    continue
                else:
                    self.delete_save(self.arena.save_id, p.PATH_SAVES)
                    self.menu_state = Menu.START
                    continue

            elif self.menu_state == Menu.STATUS:
                print(self.arena.player_tribute)
                self.menu_state = Menu.MAIN
                continue

            elif self.menu_state == Menu.INVENTORY:
                if self.arena.player_tribute.inventory:
                    print(f"Inventario de {self.arena.player_tribute.name}:")
                    self.menu_options = {}

                    iterator = enumerate(self.arena.player_tribute.inventory.values(), start=1)
                    for number, item in iterator:
                        self.menu_options[str(number)] = (item[0].name, Menu.USE_ITEM)
                    self.menu_options["w"] = ("Volver", Menu.MAIN)
                    self.menu_options["q"] = ("Salir de DCCapitolio", Menu.EXIT)
                else:
                    print(f"El inventario de {self.arena.player_tribute.name} esta vacio")
                    self.menu_state = Menu.MAIN
                    continue

            elif self.menu_state == Menu.USE_ITEM:
                item = self.arena.player_tribute.inventory[self.menu_options[user_input][0]]
                self.arena.player_tribute.use_item(item[0])
                self.menu_state = Menu.MAIN
                continue

            elif self.menu_state == Menu.SUMMARY:
                print(self.arena)
                self.menu_state = Menu.MAIN
                continue

            print("")
            for option, value in self.menu_options.items():
                print(f"[{option}] —", value[0])

            user_input = input()
            if user_input in self.menu_options:
                self.menu_state = self.menu_options[user_input][1]
            else:
                print(f"ERROR: {user_input} no es una opción valida")
            print("")

    def save(self, arena, path):
        data = arena.serialize()
        if arena.save_id >= len(self.saved_games):
            self.saved_games.append([datetime.now().strftime("%Y/%m/%d %H:%M:%S"), data])

        file = open(path, "w", encoding="utf-8")
        for number, save in enumerate(self.saved_games):
            if not save is None:
                if number == arena.save_id:
                    file.write(datetime.now().strftime("%Y/%m/%d %H:%M:%S") + "\n" + data + "\n")
                else:
                    file.write(save[0] + "\n" + save[1] + "\n")
        file.close()

    def load_list(self, path):
        saves = []
        save = []
        try:
            file = open(path, "r+", encoding="utf-8")
            for number, line in enumerate(file):
                if number % 2 == 0:
                    save.append(line.strip("\n"))
                else:
                    save.append(line.strip("\n"))
                    saves.append(save)
                    save = []
            file.close()
            saves.sort(key=lambda x: x[0], reverse=True)
            self.saved_games = saves
        except FileNotFoundError:
            print("INFO: creando archivo para guardar partidas...")
            self.saved_games = []

    def delete_save(self, save_id, path):
        self.saved_games[save_id] = None
        file = open(path, "w", encoding="utf8")
        for number, save in enumerate(self.saved_games):
            if not save is None:
                file.write(save[0] + "\n" + save[1] + "\n")
        file.close()

