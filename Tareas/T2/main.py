import sys
from PyQt5.QtWidgets import QApplication

from window_game import WindowGame
from logic_game import LogicGame
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
    logic_game = LogicGame()

    window_start.signal_submit_user.connect(
        logic_start.check_user
        )

    window_start.signal_show_ranking.connect(
        window_ranking.show
        )
    
    logic_start.signal_user_submit_reply.connect(
            window_start.submit_user_reply
        )

    logic_start.signal_start_game.connect(
            logic_game.start_game
        )

    window_ranking.signal_return_start.connect(
        window_start.show
        )

    window_game.signal_game_key_down.connect(
            logic_game.key_down
            )

    window_game.signal_game_key_up.connect(
            logic_game.key_up
            )

    window_game.signal_pause_game.connect(
            logic_game.pause_game
            )

    window_game.signal_resume_game.connect(
            logic_game.resume_game
            )

    logic_game.signal_render_level.connect(
            window_game.render_level
        )

    logic_game.signal_render.connect(
            window_game.render
            )

    window_start.show()

    app.exec()
