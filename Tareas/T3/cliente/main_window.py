from PyQt5.QtWidgets import QWidget, QLabel


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        QLabel("Esta es la ventana principal", self)
