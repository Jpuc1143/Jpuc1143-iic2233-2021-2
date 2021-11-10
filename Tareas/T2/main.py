import sys
from PyQt5.QtWidgets import QApplication

from window_game import WindowGame
#from logic_game import LogicGame
from window_start import WindowStart
from logic_start import LogicStart
from window_ranking import WindowRanking


# Código de contenidos Semana 7.1
# https://github.com/IIC2233/contenidos/blob/main/semana-07/1-interfaces-gr%C3%A1ficas.ipynb
if __name__ == '__main__':
    def hook(type, value, traceback):
        print(type)
        print(traceback)
    sys.__excepthook__ = hook

    app = QApplication([])

    window_start = WindowStart()
    logic_start = LogicStart()

    window_ranking = WindowRanking()

    window_game = WindowGame()
    # logic_game = LogicGame()

    window_start.signal_submit_user.connect(
        logic_start.check_user
        )

    window_start.signal_show_ranking.connect(
        window_ranking.show
        )
    
    logic_start.signal_user_submit_reply.connect(
            window_start.submit_user_reply
        )

    #logic_start.signal_start_game.connect(
    # TODO       
    #    )

    window_ranking.signal_return_start.connect(
        window_start.show
        )

    window_start.show()

    app.exec()
