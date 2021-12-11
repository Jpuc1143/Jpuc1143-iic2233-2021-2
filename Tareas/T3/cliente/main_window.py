from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QTableWidget, QPushButton, QScrollArea, QVBoxLayout, QButtonGroup, QMessageBox, QProgressDialog, QDialog


class MainWindow(QWidget):
    signal_invite_player = pyqtSignal(str)
    signal_prompt_invite_reply = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.resize(200,200)
        self.setWindowTitle("DCCalamar — Sala de Espera")

        self.lobby_data = []
        self.lobby_scroll = QScrollArea(self)
        self.lobby_scroll.setWidget(QLabel("Loading..."))
        self.lobby_buttons = QButtonGroup(self)
        self.lobby_buttons.buttonClicked.connect(self.lobby_button_clicked)

        self.invite_dialog = QMessageBox(self)
        self.invite_dialog.setStandardButtons(QMessageBox.Cancel)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Bienvenidos a DCCalamar"))
        layout.addWidget(self.lobby_scroll)

    def update_lobby(self, lobby_data):
        self.lobby_data = lobby_data
        for button in self.lobby_buttons.buttons():
            self.lobby_buttons.removeButton(button)

        scroll_widget = QWidget(self)
        #scroll_widget.resize(self.lobby_scroll.size().width(), scroll_widget.size().height())
        lobby_layout = QGridLayout(scroll_widget)
        for index, data in enumerate(lobby_data):
            lobby_layout.addWidget(QLabel(data[0]), index, 0)
            button = QPushButton("Invitar")
            button.setEnabled(data[1])
            lobby_layout.addWidget(button, index, 1)
            self.lobby_buttons.addButton(button, index)

        self.lobby_scroll.setWidget(scroll_widget)

    def lobby_button_clicked(self, button):
        # TODO thread safety???
        button_id = self.lobby_buttons.id(button)
        invited_player = self.lobby_data[button_id][0]

        self.invite_dialog.setText(f"Esperando a que {invited_player} acepte.")
        self.invite_dialog.open()
        self.signal_invite_player.emit(invited_player)

    def invite_player_reply(self, success):
        self.invite_dialog.close()

    def prompt_invite(self, inviter):
        invited_prompt = QMessageBox(self)
        invited_prompt.setText(f"{inviter} te ha invitado a una partida")
        invited_prompt.setInformativeText("¿Aceptar invitación?")

        invited_prompt.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        invited_prompt.accepted.connect(self.prompt_invite_accept)
        invited_prompt.rejected.connect(self.prompt_invite_reject)

        invited_prompt.open()

    def prompt_invite_accept(self):
        self.signal_prompt_invite_reply.emit(True)

    def prompt_invite_reject(self):
        self.signal_prompt_invite_reply.emit(False)
