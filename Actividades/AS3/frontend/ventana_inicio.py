from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout,
)

import parametros as p


class VentanaInicio(QWidget):

    senal_enviar_login = pyqtSignal(tuple)

    def __init__(self, tamano_ventana):
        super().__init__()
        self.init_gui(tamano_ventana)

    def init_gui(self, tamano_ventana):
        self.setWindowIcon(QIcon(p.RUTA_ICONO))
        self.setGeometry(tamano_ventana)

        self.logo = QLabel(self)
        self.logo.setPixmap(QPixmap(p.RUTA_LOGO))
        self.logo.setMaximumSize(400, 400)
        self.logo.setScaledContents(True)

        self.usuario_form = QLineEdit(self)
        self.usuario_form_label = QLabel("Usuario:", self)

        self.usuario_form_box = QHBoxLayout()
        self.usuario_form_box.addWidget(self.usuario_form_label)
        self.usuario_form_box.addWidget(self.usuario_form)

        self.clave_form = QLineEdit(self)
        self.clave_form.setEchoMode(QLineEdit.Password)
        self.clave_form_label = QLabel("Contraseña:", self)

        self.clave_form_box = QHBoxLayout()
        self.clave_form_box.addWidget(self.clave_form_label)
        self.clave_form_box.addWidget(self.clave_form)

        self.ingresar_button = QPushButton("Log In", self)
        self.ingresar_button.clicked.connect(self.enviar_login)

        vbox = QVBoxLayout()
        vbox.addWidget(self.logo)
        vbox.addLayout(self.usuario_form_box)
        vbox.addLayout(self.clave_form_box)
        vbox.addWidget(self.ingresar_button)
        self.setLayout(vbox)

        self.agregar_estilo()
        self.show()

    def enviar_login(self):
        self.senal_enviar_login.emit((self.usuario_form.text(), self.clave_form.text()))

    def agregar_estilo(self):
        # Acciones y señales
        self.clave_form.returnPressed.connect(
            lambda: self.ingresar_button.click()
        )  # Permite usar "ENTER" para iniciar sesión

        # Estilo extra
        self.setStyleSheet("background-color: #fdf600")
        self.usuario_form.setStyleSheet("background-color: #000000;"
                                        "border-radius: 5px;"
                                        "color: white")
        self.clave_form.setStyleSheet("background-color: #000000;"
                                      "border-radius: 5px;"
                                      "color: white")
        self.ingresar_button.setStyleSheet(p.stylesheet_boton)

    def recibir_validacion(self, tupla_respuesta):
        if tupla_respuesta[1]:
            self.ocultar()
        else:
            self.clave_form.setText("")
            self.clave_form.setPlaceholderText("Contraseña inválida!")

    def mostrar(self):
        self.show()

    def ocultar(self):
        self.hide()
