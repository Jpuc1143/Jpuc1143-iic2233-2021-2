from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QLabel, QPushButton

from endpoint_error import EndpointError, FatalEndpointError


class StartWindow(QWidget):
    signal_verify_user = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.edit_user = QLineEdit()
        self.edit_birthday = QLineEdit()
        self.button_enter = QPushButton("Firmar")
        self.button_enter.clicked.connect(self.verify_user)

        layout.addWidget(QLabel("LOGO"))
        form = QFormLayout()
        layout.addLayout(form)
        form.addRow(QLabel("Usuario:"), self.edit_user)
        form.addRow(QLabel("Cumpleaños:"), self.edit_birthday)
        form.addRow(self.button_enter)

    def verify_user(self):
        raise FatalEndpointError
        self.edit_user.setEnabled(False)
        self.edit_birthday.setEnabled(False)
        self.button_enter.setEnabled(False)
        self.signal_verify_user.emit(self.edit_user.text(), self.edit_birthday.text())

    def verify_user_reply(self, success):
        self.edit_user.setEnabled(True)
        self.edit_birthday.setEnabled(True)
        self.button_enter.setEnabled(True)

        if success:
            self.hide()
