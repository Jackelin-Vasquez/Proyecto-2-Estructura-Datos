import sys
from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QPushButton,QLabel, QFrame, QLineEdit, QStackedWidget, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class MenuPrincipal(QWidget):
    def __init__(self, usuario, raw, conv):
        super().__init__()
        # Recibimos los motores de lógica y guardado
        self.usuario = usuario
        self.raw = raw
        self.conv = conv

        self.setWindowTitle("Tree System - Panel de Control")
        self.setMinimumSize(1100, 700)
        self.setStyleSheet("background-color: #f0f0f0;")

        self.setup_ui()

    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- SIDEBAR (Panel Izquierdo Verde) ---
        sidebar = QFrame()
        sidebar.setFixedWidth(240)
        sidebar.setStyleSheet("background-color: #1a8a42; border: none;")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        lbl_logo = QLabel("Tree\nSystem")
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_logo.setStyleSheet("color: white; font-size: 28px; font-weight: bold; margin: 20px;")
        sidebar_layout.addWidget(lbl_logo)

        # Botones del Menú Lateral
        self.btn_binario = self.crear_boton_menu("Árbol binario")
        self.btn_bst = self.crear_boton_menu("Árbol BST")
        self.btn_avl = self.crear_boton_menu("Árbol AVL")

        # Conectar navegación del StackedWidget
        self.btn_binario.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.btn_bst.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.btn_avl.clicked.connect(lambda: self.stack.setCurrentIndex(2))

        sidebar_layout.addWidget(self.btn_binario)
        sidebar_layout.addWidget(self.btn_bst)
        sidebar_layout.addWidget(self.btn_avl)
        sidebar_layout.addStretch()

        # --- ÁREA DE CONTENIDO (Derecha) ---
        self.stack = QStackedWidget()

        # Creamos las 3 páginas
        self.pag_simple = self.crear_pagina_arbol("Árbol binario", "simple")
        self.pag_busqueda = self.crear_pagina_arbol("Árbol BST", "busqueda")
        self.pag_avl = self.crear_pagina_arbol("Árbol AVL", "avl")

        self.stack.addWidget(self.pag_simple)
        self.stack.addWidget(self.pag_busqueda)
        self.stack.addWidget(self.pag_avl)

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.stack)

    def crear_boton_menu(self, texto):
        btn = QPushButton(texto)
        btn.setFixedHeight(50)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                font-size: 16px;
                text-align: left;
                padding-left: 20px;
                border-bottom: 1px solid #28a745;
            }
            QPushButton:hover { background-color: #28a745; }
        """)
        return btn

    def crear_pagina_arbol(self, titulo_texto, tipo_arbol):
        pagina = QWidget()
        layout = QVBoxLayout(pagina)
        layout.setContentsMargins(40, 20, 40, 20)

        titulo = QLabel(titulo_texto)
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 36px; font-weight: bold; color: black;")
        layout.addWidget(titulo)

        # Controles
        controles_layout = QHBoxLayout()
        input_val = QLineEdit()
        input_val.setPlaceholderText("Buscar")
        input_val.setFixedWidth(120)
        input_val.setStyleSheet("border-radius: 10px; border: 1px solid gray; padding: 5px; background: white; color: black;")

        btn_insertar = self.crear_boton_accion("Insertar")
        btn_buscar = self.crear_boton_accion("Buscar")
        btn_eliminar = self.crear_boton_accion("Eliminar")

        # Conectar acciones pasando el input y el tipo
        btn_insertar.clicked.connect(lambda: self.accion_insertar(input_val, tipo_arbol))
        btn_buscar.clicked.connect(lambda: self.accion_buscar(input_val, tipo_arbol))
        btn_eliminar.clicked.connect(lambda: self.accion_eliminar(input_val, tipo_arbol))

        controles_layout.addWidget(input_val)
        controles_layout.addWidget(btn_insertar)
        controles_layout.addWidget(btn_buscar)
        controles_layout.addWidget(btn_eliminar)
        controles_layout.addStretch()

        btn_pre = self.crear_boton_accion("Preorden")
        btn_in = self.crear_boton_accion("Inorden")
        btn_post = self.crear_boton_accion("Postorden")

        controles_layout.addWidget(btn_pre)
        controles_layout.addWidget(btn_in)
        controles_layout.addWidget(btn_post)

        layout.addLayout(controles_layout)

        # Canvas (DOnde se va a dibjar los arboles)
        canvas = QFrame()
        canvas.setStyleSheet("background-color: white; border: 1px solid #ccc; border-radius: 10px; margin-top: 10px;")
        layout.addWidget(canvas, 1)

        return pagina

    def crear_boton_accion(self, texto):
        btn = QPushButton(texto)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border-radius: 15px;
                padding: 8px 15px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #218838; }
        """)
        return btn

    # conexción con clases

    def accion_insertar(self, line_edit, tipo):
        try:
            val = int(line_edit.text().strip())
            nombre_it = f"Tree_{self.usuario}"

            if tipo == "simple":
                arbol = self.conv.bn_search(nombre_it)
                if not arbol:
                    from Arboles.binario_simple import ArbolSimple
                    arbol = ArbolSimple(nombre_it)
                    self.conv.binario_n[nombre_it] = arbol
                arbol.agregar(val)
                self.raw.bn_save()

            elif tipo == "busqueda":
                arbol = self.conv.bABB_search(nombre_it)
                if not arbol:
                    from Arboles.binario_busqueda import ArbolBusqueda
                    arbol = ArbolBusqueda(nombre_it)
                    self.conv.binario_ABB[nombre_it] = arbol
                arbol.agregar(val)
                self.raw.bABB_save()

            elif tipo == "avl":
                arbol = self.conv.bAVB_search(nombre_it)
                if not arbol:
                    from Arboles.binario_balanceado import ArbolAVL
                    arbol = ArbolAVL(nombre_it)
                    self.conv.binario_AVB[nombre_it] = arbol
                arbol.insertar(val)
                self.raw.bAVB_save()

            print(f"Insertado {val} en {tipo}")
            line_edit.clear()

        except ValueError:
            QMessageBox.warning(self, "Error", "Ingresa un número entero.")

    def accion_buscar(self, line_edit, tipo):
        # Aun falta conexión con el metodo de buscar xd
        QMessageBox.information(self, "Info", f"Buscando en {tipo}...")

    def accion_eliminar(self, line_edit, tipo):
        #Falta conexión con metod de eliminar xd
        QMessageBox.information(self, "Info", f"Eliminando en {tipo}...")