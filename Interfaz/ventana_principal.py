import sys
from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QFrame, QStackedWidget, QMessageBox, QScrollArea)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPainter, QPen, QColor, QFont
from io import StringIO
from contextlib import contextmanager
from PyQt6.QtCore import QTimer

from Datos.tipos_arbol import SIMPLE, TIPOS
from Interfaz.estilos import (
    ESTILO_BOTON_ACCION,
    ESTILO_BOTON_MENU,
    ESTILO_INPUT_CLARO,
    ESTILO_TITULO_INFO,
    ESTILO_VALOR_INFO,
    crear_boton,
    crear_input,
    crear_label,
)
from Recorridos import recorridos

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
        # Tamaño inicial para que la area del scroll no lo oculte
        self.setMinimumSize(800, 500)
        #Se fuarda el valor del nodo que se está visitando actualmente :D
        self.nodo_actual_animado = None

    def actualizar_tamano(self):
        arbol = self.obtener_arbol()
        if not arbol or not arbol.raiz:
            self.setFixedSize(800, 500)
            return

        profundidad = self._obtener_profundidad(arbol.raiz)

        # usemos un ancho base, para que crezca de forma normal xd.
        ancho_necesario = max(1000, profundidad * 250)
        alto_necesario = max(600, (profundidad + 1) * 100)

        self.setFixedSize(ancho_necesario, alto_necesario)

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
        return recorridos.profundidad(nodo)

    def _dibujar_fondo_niveles(self, painter, niveles):
        painter.setFont(QFont("Arial", 12, QFont.Weight.Bold))

        # Título Nivel
        painter.setPen(QColor("#888888"))
        painter.drawText(20, 40, "Nivel")

        for i in range(1, niveles + 1):
            y = i * 80
            # Línea horizontal gris
            painter.setPen(QPen(QColor("#cccccc"), 1))
            painter.drawLine(150, y, self.width() - 50, y)

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

        #Se pinta el nodo de color naranja
        if self.nodo_actual_animado is not None and nodo.val == self.nodo_actual_animado:
            color = QColor("#ff9100")  # Naranja :D
            painter.setBrush(color)
            painter.setPen(QPen(QColor("#cc5200"), 2))
        else:
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

        self.lbls_raiz = {}
        self.lbls_altura = {}
        self.lbls_nodos = {}
        self.canvas_por_tipo = {}

        #Variables para la animación secuencial
        self.timer_animacion = QTimer()
        self.timer_animacion.timeout.connect(self._procesar_siguiente_nodo_animacion)
        self.lista_nodos_animacion = []
        self.indice_animacion = 0
        self.tipo_arbol_actual_animando = ""
        self.prefijo_modo_actual = ""
        self.acumulado_texto_recorrido = []

        self.es_modo_buscar = False
        self.resultado_busqueda_final = None

        self.setWindowTitle("Tree System - Panel de Control")
        self.setMinimumSize(1100, 700)
        self.setStyleSheet("background-color: #f0f0f0;")

        self.setup_ui()
        #iniciaizar infromacion de arbol
        for tipo in TIPOS:
            self._actualizar_informacion_arbol(tipo)

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

        sidebar_layout.addWidget(crear_label(
            "Tree\nSystem",
            "color: white; font-size: 28px; font-weight: bold; margin: 20px;",
            centrado=True,
        ))

        # --- CONTENIDO ---
        self.stack = QStackedWidget()

        for indice, (tipo, spec) in enumerate(TIPOS.items()):
            btn = crear_boton(spec.etiqueta, ESTILO_BOTON_MENU, alto=50)
            btn.clicked.connect(lambda _, i=indice: self.stack.setCurrentIndex(i))
            sidebar_layout.addWidget(btn)
            self.stack.addWidget(self.crear_pagina_arbol(spec.etiqueta, tipo))

        sidebar_layout.addStretch()

        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.stack)

    def crear_pagina_arbol(self, titulo_texto, tipo_arbol):
        pagina = QWidget()
        layout = QVBoxLayout(pagina)
        layout.setContentsMargins(40, 20, 40, 20)

        layout.addWidget(crear_label(
            titulo_texto, "font-size: 36px; font-weight: bold; color: #333333;", centrado=True))

        controles_layout = QHBoxLayout()
        input_val = crear_input("Valor...", ESTILO_INPUT_CLARO, ancho=120)
        controles_layout.addWidget(input_val)

        acciones = [
            ("Insertar", lambda: self.accion_insertar(input_val, tipo_arbol)),
            ("Buscar", lambda: self.accion_buscar(input_val, tipo_arbol)),
            ("Eliminar", lambda: self.accion_eliminar(input_val, tipo_arbol)),
        ]
        for texto, callback in acciones:
            btn = crear_boton(texto, ESTILO_BOTON_ACCION)
            btn.clicked.connect(callback)
            controles_layout.addWidget(btn)

        controles_layout.addStretch()

        for texto, modo in (("Preorden", "pre"), ("Inorden", "in"), ("Postorden", "post")):
            btn = crear_boton(texto, ESTILO_BOTON_ACCION)
            btn.clicked.connect(lambda _, m=modo: self.accion_recorrido(tipo_arbol, m))
            controles_layout.addWidget(btn)

        layout.addLayout(controles_layout)

        #Barra de información del arbol
        info_layout = QHBoxLayout()
        info_layout.setContentsMargins(10, 5, 10, 5)

        self.lbls_raiz[tipo_arbol] = self._agregar_dato_info(info_layout, "Valor Raíz: ", "Ninguno")
        self.lbls_altura[tipo_arbol] = self._agregar_dato_info(info_layout, "Altura total: ", "0")
        self.lbls_nodos[tipo_arbol] = self._agregar_dato_info(
            info_layout, "Cantidad Nodos: ", "0", ultimo=True)

        info_layout.addStretch()
        layout.addLayout(info_layout)

        # seccion de recorrido
        recorrido_container = QHBoxLayout()
        recorrido_container.addStretch()

        lbl_resultado = crear_label(
            "",
            "font-size: 14px; color: #333; font-weight: bold; margin-top: 10px; margin-bottom: 10px;")

        self.labels_recorrido[tipo_arbol] = lbl_resultado
        recorrido_container.addWidget(lbl_resultado)

        layout.addLayout(recorrido_container)

        # --- ARREGLO DEL SCROLL AREA ---
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(False)  # Dsto para que respete el tamaño del cava
        scroll_area.setStyleSheet("background-color: white; border: 1px solid #ccc; border-radius: 10px;")

        # CAPA DE DIBUJO
        capa = CapaDibujo(lambda: self._obtener_arbol(tipo_arbol, self._nombre_arbol()))
        scroll_area.setWidget(capa)
        layout.addWidget(scroll_area, 1)

        self.canvas_por_tipo[tipo_arbol] = capa

        return pagina

    def _agregar_dato_info(self, info_layout, titulo, valor_inicial, ultimo=False):
        info_layout.addWidget(crear_label(titulo, ESTILO_TITULO_INFO))
        estilo = ESTILO_VALOR_INFO if ultimo else ESTILO_VALOR_INFO + " margin-right: 20px;"
        lbl_valor = crear_label(valor_inicial, estilo)
        info_layout.addWidget(lbl_valor)
        return lbl_valor

    def _nombre_arbol(self):
        return f"Tree_{self.usuario}"

    def _obtener_arbol(self, tipo, nombre):
        return self.conv.search(tipo, nombre)

    def _canvas(self, tipo):
        return self.canvas_por_tipo.get(tipo)

    def _refrescar_canvas(self, tipo):
        canvas = self._canvas(tipo)
        if canvas:
            canvas.actualizar_tamano()  # Primero ajustamos el widget
            canvas.update()  # Luego se pinta :D
            self._actualizar_informacion_arbol(tipo)

    def accion_insertar(self, line_edit, tipo):
        texto = line_edit.text().strip()
        if not texto:
            return

        try:
            val = int(texto)
            nombre_it = self._nombre_arbol()
            arbol = self._obtener_arbol(tipo, nombre_it)

            if not arbol:
                arbol = self.conv.registrar(tipo, TIPOS[tipo].arbol_clase(nombre_it))

            arbol.agregar(val)
            self.raw.guardar(tipo)

            line_edit.clear()
            self._refrescar_canvas(tipo)
        except ValueError:
            QMessageBox.warning(self, "Error", "Ingrese un número entero.")

    def accion_recorrido(self, tipo, modo):
        self.timer_animacion.stop()
        arbol = self._obtener_arbol(tipo, self._nombre_arbol())
        canvas = self._canvas(tipo)
        if arbol and arbol.raiz and canvas:
            nombres_modo = {"pre": "Preorden", "in": "Inorden", "post": "Postorden"}

            metodos = {
                "pre": arbol.preorden,
                "in": arbol.inorden,
                "post": arbol.postorden}

            _, texto_recorrido = ejecutar_con_captura(metodos[modo])
            nodos_encontrados = [int(x) for x in texto_recorrido.strip().split('\n') if x.strip()]

            if not nodos_encontrados:
                return

            self.es_modo_buscar = False
            self.tipo_arbol_actual_animando = tipo
            self.prefijo_modo_actual = nombres_modo[modo]
            self.lista_nodos_animacion = nodos_encontrados
            self.indice_animacion = 0
            self.acumulado_texto_recorrido = []

            self.timer_animacion.start(600)
        else:
            self.labels_recorrido[tipo].setText("Árbol vacío")

    def accion_buscar(self, line_edit, tipo):
        self.timer_animacion.stop()  # Frenar cualquier animación corriendo
        texto = line_edit.text().strip()
        if not texto:
            return

        try:
            val = int(texto)
            arbol = self._obtener_arbol(tipo, self._nombre_arbol())
            if not arbol or not arbol.raiz:
                return
            resultado = arbol.buscar(val)

            # El camino depende de si el árbol está ordenado o no
            if tipo == SIMPLE:
                camino = recorridos.camino_por_niveles(arbol.raiz, val)
            else:
                camino = recorridos.camino_ordenado(arbol.raiz, val)

            self.es_modo_buscar = True  #para saber que es una búsqueda
            self.resultado_busqueda_final = resultado
            self.tipo_arbol_actual_animando = tipo
            self.prefijo_modo_actual = "Camino de Búsqueda"
            self.lista_nodos_animacion = camino
            self.indice_animacion = 0
            self.acumulado_texto_recorrido = []

            self.timer_animacion.start(500)
            line_edit.clear()

        except ValueError:
            QMessageBox.critical(self, "Error", "Por favor, ingrese un número entero.")

    def accion_eliminar(self, line_edit, tipo):
        texto = line_edit.text().strip()
        if not texto:
            return
        try:
            val = int(texto)
            arbol = self._obtener_arbol(tipo, self._nombre_arbol())

            if arbol:
                arbol.eliminar(val)
                self.raw.guardar(tipo)

                #Se actualiza interfaz
                self._refrescar_canvas(tipo)
                line_edit.clear()
            else:
                QMessageBox.warning(self, "Aviso", "El árbol no existe.")

        except ValueError:
            QMessageBox.warning(self, "Error", "Por favor, ingrese un número válido.")
        except Exception as e:
            QMessageBox.critical(self, "Error en Eliminación",f"El motor del árbol falló:\n{str(e)}\n.")

    """Función para actualizar los labels de consultar_metadata consultando al árbol y a la interfaz"""
    def _actualizar_informacion_arbol(self, tipo):
        arbol = self._obtener_arbol(tipo, self._nombre_arbol()) #Obteien la info desde las funciones de arriba xd
        canvas = self._canvas(tipo)

        if arbol and arbol.raiz and canvas:
            # Métodos lógicos del backend de los árboles
            val_raiz = str(arbol.obtener_valor_raiz())
            total_nodos = str(arbol.contar_nodos())

            # Altura tomada directamente de inferfaz obtener_produnidad (arriba :D)
            altura = str(canvas._obtener_profundidad(arbol.raiz))

            self.lbls_raiz[tipo].setText(val_raiz)
            self.lbls_altura[tipo].setText(altura)
            self.lbls_nodos[tipo].setText(total_nodos)
        else:
            self.lbls_raiz[tipo].setText("Ninguno")
            self.lbls_altura[tipo].setText("0")
            self.lbls_nodos[tipo].setText("0")

    def _procesar_siguiente_nodo_animacion(self):
        tipo = self.tipo_arbol_actual_animando
        canvas = self._canvas(tipo)

        if self.indice_animacion >= len(self.lista_nodos_animacion):
            self.timer_animacion.stop()
            if canvas:
                canvas.nodo_actual_animado = None
                canvas.update()

            # Si estábamos en el metodo busqueda, al terminar la animación lanzamos el mensjae ---
            if self.es_modo_buscar:
                if self.resultado_busqueda_final:
                    res_val = self.resultado_busqueda_final[0]
                    res_alt = self.resultado_busqueda_final[1]
                    QMessageBox.information(self, "Nodo Encontrado",f"¡Éxito!\nValor: {res_val}\nAltura en el árbol: {res_alt}")
                else:
                    QMessageBox.warning(self, "No encontrado", "El valor no existe en la estructura jerárquica.")

                # Limpieza de banderas de búsqueda
                self.es_modo_buscar = False
                self.resultado_busqueda_final = None
            return

        nodo_valor = self.lista_nodos_animacion[self.indice_animacion]

        if canvas:
            canvas.nodo_actual_animado = nodo_valor
            canvas.update()

        self.acumulado_texto_recorrido.append(str(nodo_valor))
        formato_texto = f"{self.prefijo_modo_actual}: {' ➔ '.join(self.acumulado_texto_recorrido)}"
        self.labels_recorrido[tipo].setText(formato_texto)

        self.indice_animacion += 1