import sys
from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QPushButton,QLabel, QFrame, QLineEdit, QStackedWidget, QMessageBox)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPainter, QPen, QColor, QFont
from io import StringIO
from contextlib import contextmanager

@contextmanager
def capturar_print():
    """Esto ayuda a capturar los print, nos va a servir par amostrar los reccorrido ya que los metodos
    soo muestran print :("""
    old_stdout = sys.stdout
    captured_output = StringIO()
    sys.stdout = captured_output
    try:
        yield captured_output
    finally:
        sys.stdout = old_stdout

def ejecutar_con_captura(funcion, *args, **kwargs):
    """Ejecuta la funcion anterior y captura todos sus prints"""
    with capturar_print() as output:
        resultado = funcion(*args, **kwargs)
        texto_capturado = output.getvalue()
    return resultado, texto_capturado

class CapaDibujo(QWidget):
    def __init__(self, obtener_arbol_callback):
        super().__init__()
        self.obtener_arbol = obtener_arbol_callback

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        arbol = self.obtener_arbol()
        if not arbol or not arbol.raiz:
            return

        profundidad_max = self._obtener_profundidad(arbol.raiz)

        #Fondo
        self._dibujar_fondo_niveles(painter, profundidad_max)

        # Aqui se dibuja el arbol
        ancho_disponible = self.width() - 200
        self._dibujar_nodo(painter, arbol.raiz, self.width() // 2 + 50, 80, ancho_disponible // 4, 1)

    def _obtener_profundidad(self, nodo):
        if not nodo: return 0
        return 1 + max(self._obtener_profundidad(nodo.izq), self._obtener_profundidad(nodo.der))

    def _dibujar_fondo_niveles(self, painter, niveles):
        painter.setFont(QFont("Arial", 12, QFont.Weight.Bold))

        # Título Nivel
        painter.setPen(QColor("#888888"))
        painter.drawText(20, 40, "Nivel")

        for i in range(1, niveles + 1):
            y = i * 80
            # Línea horizontal gris
            painter.setPen(QPen(QColor("#cccccc"), 1))
            painter.drawLine(250, y, self.width() - 50, y)

            # Etiquetas de nivel
            texto_nivel = "Raíz - 1" if i == 1 else str(i)
            painter.setPen(QColor("#333333"))
            painter.drawText(50, y + 5, texto_nivel)

    def _dibujar_nodo(self, painter, nodo, x, y, espacio_h, nivel):
        if not nodo: return

        distancia_y = 80
        proximo_y = y + distancia_y
        painter.setPen(QPen(Qt.GlobalColor.black, 2))

        if nodo.izq:
            painter.drawLine(int(x), int(y), int(x - espacio_h), int(proximo_y))
            self._dibujar_nodo(painter, nodo.izq, x - espacio_h, proximo_y, espacio_h // 2, nivel + 1)

        painter.setPen(QPen(Qt.GlobalColor.black, 2))
        if nodo.der:
            painter.drawLine(int(x), int(y), int(x + espacio_h), int(proximo_y))
            self._dibujar_nodo(painter, nodo.der, x + espacio_h, proximo_y, espacio_h // 2, nivel + 1)

        # Círculo del nodo
        colores = ["#00c853", "#4caf50", "#8bc34a", "#cddc39", "#d4e157"]
        color = QColor(colores[min(nivel - 1, len(colores) - 1)])

        painter.setBrush(color)
        painter.setPen(QPen(QColor("#1a6332"), 1))
        painter.drawEllipse(QPoint(int(x), int(y)), 28, 28)

        # Texto blanco centrado
        painter.setPen(Qt.GlobalColor.white)
        painter.setFont(QFont("Arial", 9, QFont.Weight.Bold))
        # ajuste del rectanglo del texto
        painter.drawText(int(x - 28), int(y - 28), 56, 56, Qt.AlignmentFlag.AlignCenter, str(nodo.val))

class MenuPrincipal(QWidget):
    def __init__(self, usuario, raw, conv):
        super().__init__()
        self.usuario = usuario
        self.raw = raw
        self.conv = conv
        self.labels_recorrido = {}

        self.setWindowTitle("Tree System - Panel de Control")
        self.setMinimumSize(1100, 700)
        self.setStyleSheet("background-color: #f0f0f0;")

        self.setup_ui()

    def setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- SIDEBAR ---
        sidebar = QFrame()
        sidebar.setFixedWidth(240)
        sidebar.setStyleSheet("background-color: #1a8a42; border: none;")
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        lbl_logo = QLabel("Tree\nSystem")
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_logo.setStyleSheet("color: white; font-size: 28px; font-weight: bold; margin: 20px;")
        sidebar_layout.addWidget(lbl_logo)

        self.btn_binario = self.crear_boton_menu("Árbol binario")
        self.btn_bst = self.crear_boton_menu("Árbol BST")
        self.btn_avl = self.crear_boton_menu("Árbol AVL")

        sidebar_layout.addWidget(self.btn_binario)
        sidebar_layout.addWidget(self.btn_bst)
        sidebar_layout.addWidget(self.btn_avl)
        sidebar_layout.addStretch()

        # --- CONTENIDO ---
        self.stack = QStackedWidget()
        self.pag_simple = self.crear_pagina_arbol("Árbol binario", "simple")
        self.pag_busqueda = self.crear_pagina_arbol("Árbol BST", "busqueda")
        self.pag_avl = self.crear_pagina_arbol("Árbol AVL", "avl")

        self.stack.addWidget(self.pag_simple)
        self.stack.addWidget(self.pag_busqueda)
        self.stack.addWidget(self.pag_avl)

        self.btn_binario.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.btn_bst.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.btn_avl.clicked.connect(lambda: self.stack.setCurrentIndex(2))

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
        titulo.setStyleSheet("font-size: 36px; font-weight: bold; color: #333333;")
        layout.addWidget(titulo)

        controles_layout = QHBoxLayout()
        input_val = QLineEdit()
        input_val.setPlaceholderText("Valor...")
        input_val.setFixedWidth(120)
        # IMPORTANTE: Forzamos color negro para que el texto sea visible
        input_val.setStyleSheet(
            "border-radius: 10px; border: 1px solid #999; padding: 5px; background: white; color: black;")

        btn_insertar = self.crear_boton_accion("Insertar")
        btn_buscar = self.crear_boton_accion("Buscar")
        btn_eliminar = self.crear_boton_accion("Eliminar")

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

        btn_pre.clicked.connect(lambda: self.accion_recorrido(tipo_arbol, "pre"))
        btn_in.clicked.connect(lambda: self.accion_recorrido(tipo_arbol, "in"))
        btn_post.clicked.connect(lambda: self.accion_recorrido(tipo_arbol, "post"))

        controles_layout.addWidget(btn_pre)
        controles_layout.addWidget(btn_in)
        controles_layout.addWidget(btn_post)

        layout.addLayout(controles_layout)

        # seccion de recorrido
        recorrido_container = QHBoxLayout()
        recorrido_container.addStretch()

        lbl_resultado = QLabel("")
        lbl_resultado.setStyleSheet(
            "font-size: 14px; color: #333; font-weight: bold; margin-top: 10px; margin-bottom: 10px;")

        self.labels_recorrido[tipo_arbol] = lbl_resultado
        recorrido_container.addWidget(lbl_resultado)

        layout.addLayout(recorrido_container)

        # CAPA DE DIBUJO
        capa = CapaDibujo(lambda: self._obtener_arbol(tipo_arbol, f"Tree_{self.usuario}"))
        layout.addWidget(capa, 1)

        if tipo_arbol == "simple":
            self.canvas_simple = capa
        elif tipo_arbol == "busqueda":
            self.canvas_busqueda = capa
        elif tipo_arbol == "avl":
            self.canvas_avl = capa

        return pagina

    def crear_boton_accion(self, texto):
        btn = QPushButton(texto)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                border-radius: 12px;
                padding: 8px 15px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #218838; }
        """)
        return btn

    def _obtener_arbol(self, tipo, nombre):
        if tipo == "simple": return self.conv.bn_search(nombre)
        if tipo == "busqueda": return self.conv.bABB_search(nombre)
        if tipo == "avl": return self.conv.bAVB_search(nombre)
        return None

    def accion_insertar(self, line_edit, tipo):
        texto = line_edit.text().strip()
        if not texto:
            return

        try:
            val = int(texto)
            nombre_it = f"Tree_{self.usuario}"
            arbol = self._obtener_arbol(tipo, nombre_it)

            if not arbol:
                if tipo == "simple":
                    from Arboles.binario_simple import ArbolSimple
                    arbol = ArbolSimple(nombre_it)
                    self.conv.binario_n[nombre_it] = arbol
                elif tipo == "busqueda":
                    from Arboles.binario_busqueda import ArbolBusqueda
                    arbol = ArbolBusqueda(nombre_it)
                    self.conv.binario_ABB[nombre_it] = arbol
                elif tipo == "avl":
                    from Arboles.binario_balanceado import ArbolAVL
                    arbol = ArbolAVL(nombre_it)
                    self.conv.binario_AVB[nombre_it] = arbol

            if tipo == "avl":
                arbol.insertar(val)
            else:
                arbol.agregar(val)

            # GUARDAR EN JSON SEGÚN MOTOR
            if tipo == "simple":
                self.raw.bn_save()
            elif tipo == "busqueda":
                self.raw.bABB_save()
            elif tipo == "avl":
                self.raw.bAVB_save()

            line_edit.clear()
            self._refrescar_canvas(tipo)
        except ValueError:
            QMessageBox.warning(self, "Error", "Ingrese un número entero.")

    def _refrescar_canvas(self, tipo):
        if tipo == "simple":
            self.canvas_simple.update()
        elif tipo == "busqueda":
            self.canvas_busqueda.update()
        elif tipo == "avl":
            self.canvas_avl.update()

    def accion_recorrido(self, tipo, modo):
        arbol = self._obtener_arbol(tipo, f"Tree_{self.usuario}")
        if arbol and arbol.raiz:
            # Mapeo de nombres para el prefijo
            nombres_modo = {"pre": "Preorden", "in": "Inorden", "post": "Postorden"}

            metodos = {
                "pre": arbol.preorden,
                "in": arbol.inorden,
                "post": arbol.postorden}

            # Capturamos la salida
            _, texto_recorrido = ejecutar_con_captura(metodos[modo])

            texto_limpio = texto_recorrido.strip().replace("\n", " > ")
            formato_final = f"{nombres_modo[modo]}: {texto_limpio}"

            # Actualizamos el Label de la página actual
            self.labels_recorrido[tipo].setText(formato_final)

        else:
            self.labels_recorrido[tipo].setText("Árbol vacío")

    def accion_buscar(self, line_edit, tipo):
        texto = line_edit.text().strip()
        if not texto:
            return

        try:
            val = int(texto)
            arbol = self._obtener_arbol(tipo, f"Tree_{self.usuario}")
            resultado = arbol.buscar(val)

            if resultado:
                # aquie es donde se recibe lo de valor y alturam :D
                valor_enc, altura_enc = resultado
                QMessageBox.information(
                    self,
                    "Nodo Encontrado",
                    f"Valor: {valor_enc}\nAltura en el árbol: {altura_enc}")
            else:
                QMessageBox.warning(self, "No encontrado", f"El valor {val} no existe en el árbol.")

        except ValueError:
            QMessageBox.critical(self, "Error", "Por favor, ingrese un número entero.")

    def accion_eliminar(self, line_edit, tipo):
        texto = line_edit.text().strip()
        if not texto:
            return
        try:
            val = int(texto)
            arbol = self._obtener_arbol(tipo, f"Tree_{self.usuario}")

            if arbol:
                arbol.eliminar(val)
                #Guardar cambios
                if tipo == "simple":
                    self.raw.bn_save()
                elif tipo == "busqueda":
                    self.raw.bABB_save()
                elif tipo == "avl":
                    self.raw.bAVB_save()

                #Se actualiza interfaz
                self._refrescar_canvas(tipo)
                line_edit.clear()
            else:
                QMessageBox.warning(self, "Aviso", "El árbol no existe.")

        except ValueError:
            QMessageBox.warning(self, "Error", "Por favor, ingrese un número válido.")
        except Exception as e:
            QMessageBox.critical(self, "Error en Eliminación",f"El motor del árbol falló:\n{str(e)}\n.")