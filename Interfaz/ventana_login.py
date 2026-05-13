import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFrame, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QBrush, QImage, QPixmap

try:
    from ventana_principal import MenuPrincipal
except ImportError:
    MenuPrincipal = None

class ArbolesLogin(QWidget):
    def __init__(self, auth, on_login_exitoso):
        super().__init__()
        self.auth = auth
        self.on_login_exitoso = on_login_exitoso

        self.setWindowTitle("Mundo Comic - Catálogo Virtual")

        # Configuración de rutas de Recursos
        self.ruta_script = os.path.dirname(os.path.abspath(__file__))
        self.carpeta_recursos = os.path.join(self.ruta_script, "Recursos")

        self.setMinimumSize(1000, 700)
        self.showMaximized()
        self.setup_ui()

    def resizeEvent(self, event):
        self.actualizar_fondo()
        super().resizeEvent(event)

    def actualizar_fondo(self):
        ruta_fondo = os.path.join(self.carpeta_recursos, "fono.png")
        if os.path.exists(ruta_fondo):
            oImage = QImage(ruta_fondo)
            sImage = oImage.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation,
            )
            palette = QPalette()
            palette.setBrush(QPalette.ColorRole.Window, QBrush(sImage))
            self.setPalette(palette)
        else:
            # Color de respaldo si no hay imagen
            self.setStyleSheet("background-color: #121212;")

    def setup_ui(self):
        self.setStyleSheet("color: white; font-family: 'Segoe UI', Arial;")
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        container = QFrame()
        container.setFixedSize(400, 580)
        container.setStyleSheet("""
                    QFrame {
                        background-color: rgba(20, 20, 20, 180);
                        border: 2px solid #28a745;
                        border-radius: 30px;
                    }
                """)

        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(40, 30, 40, 30)
        container_layout.setSpacing(10)

        # Logo
        ruta_logo = os.path.join(self.carpeta_recursos, "icono2.png")
        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setStyleSheet("border: none; background: transparent;")

        if os.path.exists(ruta_logo):
            img_logo = QImage(ruta_logo)
            scaled_logo = img_logo.scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(QPixmap.fromImage(scaled_logo))
        else:
            logo_label.setText("LOGO") # Texto provisional

        container_layout.addWidget(logo_label)

        titulo = QLabel("ARBOLES")
        titulo.setStyleSheet("font-size: 28px; font-weight: bold; border: none; background: transparent;")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(titulo)

        sub_titulo = QLabel("- BIENVENIDO! -")
        sub_titulo.setStyleSheet("color: #888; border: none; font-size: 13px; background: transparent;")
        sub_titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        container_layout.addWidget(sub_titulo)

        container_layout.addSpacing(20)

        # Inputs
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("USUARIO")
        self.apply_input_style(self.user_input)
        container_layout.addWidget(self.user_input)

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("CONTRASEÑA")
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.apply_input_style(self.pass_input)
        container_layout.addWidget(self.pass_input)

        container_layout.addSpacing(20)

        # Botón
        btn_entrar = QPushButton("ENTRAR")
        btn_entrar.setMinimumHeight(55)
        btn_entrar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_entrar.setStyleSheet("""
                    QPushButton {
                        background-color: #28a745;
                        color: white;
                        border-radius: 27px;
                        font-size: 18px;
                        font-weight: bold;
                        border: none;
                    }
                    QPushButton:hover { background-color: #48c774; }
                """)
        btn_entrar.clicked.connect(self.intentar_login)
        container_layout.addWidget(btn_entrar)

        links = QLabel("¿Olvidó su contraseña?")
        links.setAlignment(Qt.AlignmentFlag.AlignCenter)
        links.setStyleSheet("background: transparent; border: none; color: #666; font-size: 11px; margin-top: 10px;")
        container_layout.addWidget(links)

        main_layout.addWidget(container)

    def apply_input_style(self, widget):
        widget.setMinimumHeight(48)
        widget.setStyleSheet("""
                    QLineEdit {
                        background-color: #2a2a2a;
                        border: 1px solid #444;
                        border-radius: 12px;
                        padding-left: 15px;
                        color: white;
                        font-size: 14px;
                    }
                    QLineEdit:focus { border: 1px solid #28a745; }
                """)

    def intentar_login(self):
        usuario = self.user_input.text().strip()
        contra = self.pass_input.text()
        # CREDENCIALES QUEMADAS
        if usuario == "admin" and contra == "1234":
            QMessageBox.information(self, "Éxito", f"Acceso concedido. ¡Bienvenido {usuario}!")
            self.on_login_exitoso(usuario)
        else:
            QMessageBox.critical(self, "Error", "Usuario o contraseña incorrectos.\n")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    def ejecutar_redireccion(nombre_usuario):
        if MenuPrincipal:
            global main_win
            main_win.show()
            login_win.close()
        else:
            print("Error: No se encontró la clase MenuPrincipal en ventana_principal.py")


    login_win = ArbolesLogin(auth=None, on_login_exitoso=ejecutar_redireccion)
    login_win.show()
    sys.exit(app.exec())