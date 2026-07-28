import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QFrame, QMessageBox
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPalette, QBrush, QPixmap

from Interfaz.estilos import (
    ESTILO_BOTON_PRINCIPAL,
    ESTILO_INPUT_OSCURO,
    crear_boton,
    crear_input,
    crear_label,
    escalar_imagen,
)

try:
    from ventana_principal import MenuPrincipal
except ImportError:
    MenuPrincipal = None

class ArbolesLogin(QWidget):
    def __init__(self, auth, on_login_exitoso):
        super().__init__()
        self.auth = auth
        self.on_login_exitoso = on_login_exitoso

        self.setWindowTitle("Login de Arboles")

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
        fondo = escalar_imagen(
            os.path.join(self.carpeta_recursos, "fono.png"), self.size(), expandir=True
        )
        if fondo is None:
            # Color de respaldo si no hay imagen
            self.setStyleSheet("background-color: #121212;")
            return

        palette = QPalette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(fondo))
        self.setPalette(palette)

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
        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setStyleSheet("border: none; background: transparent;")

        logo = escalar_imagen(
            os.path.join(self.carpeta_recursos, "icono2.png"), QSize(120, 120)
        )
        if logo is None:
            logo_label.setText("LOGO") # Texto provisional
        else:
            logo_label.setPixmap(QPixmap.fromImage(logo))

        container_layout.addWidget(logo_label)

        container_layout.addWidget(crear_label(
            "ARBOLES",
            "font-size: 28px; font-weight: bold; border: none; background: transparent;",
            centrado=True,
        ))
        container_layout.addWidget(crear_label(
            "- BIENVENIDO! -",
            "color: #888; border: none; font-size: 13px; background: transparent;",
            centrado=True,
        ))

        container_layout.addSpacing(20)

        # Inputs
        self.user_input = crear_input("USUARIO", ESTILO_INPUT_OSCURO, alto=48)
        container_layout.addWidget(self.user_input)

        self.pass_input = crear_input("CONTRASEÑA", ESTILO_INPUT_OSCURO, alto=48)
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        container_layout.addWidget(self.pass_input)

        container_layout.addSpacing(20)

        # Botón
        btn_entrar = crear_boton("ENTRAR", ESTILO_BOTON_PRINCIPAL, alto=55)
        btn_entrar.clicked.connect(self.intentar_login)
        container_layout.addWidget(btn_entrar)

        container_layout.addWidget(crear_label(
            "¿Olvidó su contraseña?",
            "background: transparent; border: none; color: #666; font-size: 11px; margin-top: 10px;",
            centrado=True,
        ))

        main_layout.addWidget(container)

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

    try:
        from Datos.Guardado_arboles import ArbolesRaw, ArbolesConv

        # Eaqui es donde llamamos a las clases
        raw_engine = ArbolesRaw()
        conv_engine = ArbolesConv()

        raw_engine.conv_origin = conv_engine
        conv_engine.raw_origin = raw_engine

        try:
            raw_engine.load()
            conv_engine.full_dump()
        except FileNotFoundError:
            print("No hay archivos previos, iniciando limpio.")

    except ImportError as e:
        print(f"Error: No se encontradon datos {e}")
        sys.exit(1)

    def abrir_menu(usuario):
        global win_principal
        try:
            win_principal = MenuPrincipal(usuario, raw_engine, conv_engine)
            win_principal.show()
            login_win.close()
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(None, "Error", f"No se pudo cargar el menú: {e}")

    login_win = ArbolesLogin(auth=None, on_login_exitoso=abrir_menu)
    login_win.show()
    sys.exit(app.exec())