from PyQt5.QtWidgets import QWidget, QLabel


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(200,200)
        QLabel("Esta es la ventana principal", self)