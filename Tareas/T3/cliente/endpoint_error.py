from PyQt5.QtWidgets import QMessageBox


class EndpointError(Exception):
    def __init__(self, reason=None):
        super().__init__()

        if reason is None:
            self.reason = "Ha ocurrido un error menor. El programa continuara"
        else:
            self.reason = reason

        self.dialog = QMessageBox() # TODO set parent as current window
        self.dialog.setText(self.reason)
        self.dialog.setIcon(QMessageBox.Warning)

    def show_error(self):
        self.dialog.exec_()

class FatalEndpointError(EndpointError):
    def __init__(self):
        super().__init__("Se ha perdido la conexión al servidor. Cerrando programa.")

        self.dialog.setIcon(QMessageBox.Critical)
