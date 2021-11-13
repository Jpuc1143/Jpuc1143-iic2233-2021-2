import sys
from PyQt5.QtWidgets import QApplication

from window_game import WindowGame
from logic_game import LogicGame
from window_start import WindowStart
from logic_start import LogicStart
from window_ranking import WindowRanking
from logic_ranking import LogicRanking
from window_post_game import WindowPostGame
from logic_post_game import LogicPostGame


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
    logic_ranking = LogicRanking()

    window_game = WindowGame()
    logic_game = LogicGame()

    window_post_game = WindowPostGame()
    logic_post_game = LogicPostGame()

    window_start.signal_submit_user.connect(
        logic_start.check_user
        )

    window_start.signal_show_ranking.connect(
        window_ranking.show_scores
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

    window_ranking.signal_load_scores.connect(
            logic_ranking.load_scores
            )

    logic_ranking.signal_set_scores.connect(
            window_ranking.set_scores
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

    window_game.signal_quit_game.connect(
            logic_game.lose_game
            )

    logic_game.signal_render_level.connect(
            window_game.render_level
        )

    logic_game.signal_render.connect(
            window_game.render
            )

    logic_game.signal_go_post_game.connect(
            window_post_game.show_results
            )

    logic_game.signal_go_post_game.connect(
            window_game.hide
            )

    window_post_game.signal_next_level.connect(
            logic_game.next_level
            )

    window_post_game.signal_save_score.connect(
            logic_post_game.save_score
            )

    window_post_game.signal_go_start.connect(
            window_start.show
            )

    window_start.show()

    app.exec()
