from PySide6.QtWidgets import QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from liquor_pos.presentation.views.pos_view import POSView

class MainWindow(QMainWindow):
    def __init__(self, pos_view: POSView):
        super().__init__()
        self.pos_view = pos_view
        self.setWindowTitle("Liquor POS - Punto de Venta & Gestión")
        self.resize(1280, 800)
        self.init_ui()

    def init_ui(self):
        self.tabs = QTabWidget()
        
        # Módulos core de la aplicación
        self.tabs.addTab(self.pos_view, "💰 Mostrador (POS)")
        self.tabs.addTab(self._create_dummy_tab("Módulo en construcción: Gestión de motorizados y cobros"), "🛵 Domicilios")
        self.tabs.addTab(self._create_dummy_tab("Módulo en construcción: CRUD de Botellas, Tragos y Cajas"), "📦 Catálogo")
        self.tabs.addTab(self._create_dummy_tab("Módulo en construcción: Arqueo ciego y mermas"), "📊 Caja / Turnos")

        self.setCentralWidget(self.tabs)

    def _create_dummy_tab(self, text):
        w = QWidget()
        l = QVBoxLayout(w)
        lbl = QLabel(text)
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl.setStyleSheet("font-size: 24px; color: #6c7086;")
        l.addWidget(lbl)
        return w
