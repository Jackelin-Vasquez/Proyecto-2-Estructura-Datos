"""Estilos y fábricas de widgets compartidos por las ventanas del sistema."""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage
from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton

VERDE = "#28a745"
VERDE_OSCURO = "#1a8a42"
VERDE_CLARO = "#48c774"

ESTILO_BOTON_PRINCIPAL = """
    QPushButton {
        background-color: #28a745;
        color: white;
        border-radius: 27px;
        font-size: 18px;
        font-weight: bold;
        border: none;
    }
    QPushButton:hover { background-color: #48c774; }
"""

ESTILO_BOTON_ACCION = """
    QPushButton {
        background-color: #28a745;
        color: white;
        border-radius: 12px;
        padding: 8px 15px;
        font-weight: bold;
    }
    QPushButton:hover { background-color: #218838; }
"""

ESTILO_BOTON_MENU = """
    QPushButton {
        background-color: transparent;
        color: white;
        font-size: 16px;
        text-align: left;
        padding-left: 20px;
        border-bottom: 1px solid #28a745;
    }
    QPushButton:hover { background-color: #28a745; }
"""

ESTILO_INPUT_OSCURO = """
    QLineEdit {
        background-color: #2a2a2a;
        border: 1px solid #444;
        border-radius: 12px;
        padding-left: 15px;
        color: white;
        font-size: 14px;
    }
    QLineEdit:focus { border: 1px solid #28a745; }
"""

ESTILO_INPUT_CLARO = (
    "border-radius: 10px; border: 1px solid #999; padding: 5px; background: white; color: black;"
)

ESTILO_TITULO_INFO = "font-weight: bold; color: #555555; font-size: 13px;"
ESTILO_VALOR_INFO = "color: #1a8a42; font-weight: bold; font-size: 13px;"


def crear_boton(texto, estilo, alto=None):
    btn = QPushButton(texto)
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    btn.setStyleSheet(estilo)
    if alto is not None:
        btn.setFixedHeight(alto)
    return btn


def crear_input(placeholder, estilo, ancho=None, alto=None):
    campo = QLineEdit()
    campo.setPlaceholderText(placeholder)
    campo.setStyleSheet(estilo)
    if ancho is not None:
        campo.setFixedWidth(ancho)
    if alto is not None:
        campo.setMinimumHeight(alto)
    return campo


def crear_label(texto, estilo, centrado=False):
    label = QLabel(texto)
    label.setStyleSheet(estilo)
    if centrado:
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    return label


def escalar_imagen(ruta, tamano, expandir=False):
    """Carga y escala una imagen; devuelve ``None`` si la ruta no sirve."""
    imagen = QImage(ruta)
    if imagen.isNull():
        return None
    modo = (
        Qt.AspectRatioMode.KeepAspectRatioByExpanding
        if expandir
        else Qt.AspectRatioMode.KeepAspectRatio
    )
    return imagen.scaled(tamano, modo, Qt.TransformationMode.SmoothTransformation)
