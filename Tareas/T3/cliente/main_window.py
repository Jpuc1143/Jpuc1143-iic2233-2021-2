from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QTableWidget, QPushButton


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(200,200)

        self.lobby_widget = QTableWidget(self)
        self.lobby_widget.setCellWidget(0, 0, QLabel("Loading..."))
        #self.lobby.addWidget(QLabel("Esta es la ventana principal", self), 0, 0, 2, 1)

    def update_lobby(self, lobby_data):
        print("rendering", lobby_data)

        self.lobby_widget.setRowCount(len(lobby_data))
        self.lobby_widget.setColumnCount(2)
        for index, data in enumerate(lobby_data):
            self.lobby_widget.setCellWidget(index, 0, QLabel(data[0]))
            self.lobby_widget.setCellWidget(index, 1, QPushButton(str(data[1])))
