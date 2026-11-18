from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, 
    QTableWidget, QTableWidgetItem, QLabel, QMessageBox, QHeaderView
)
from PySide6.QtCore import Qt
from liquor_pos.presentation.viewmodels.pos_viewmodel import POSViewModel

class POSView(QWidget):
    def __init__(self, viewmodel: POSViewModel):
        super().__init__()
        self.viewmodel = viewmodel
        self.init_ui()
        self.connect_signals()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Panel izquierdo (Lista de productos)
        left_panel = QVBoxLayout()
        
        self.barcode_input = QLineEdit()
        self.barcode_input.setPlaceholderText("Escanear Código de Barras (El cursor siempre regresa aquí)")
        self.barcode_input.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.barcode_input.setFixedHeight(60)
        
        self.cart_table = QTableWidget(0, 4)
        self.cart_table.setHorizontalHeaderLabels(["Código", "Producto", "Cant.", "Subtotal"])
        self.cart_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.cart_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.cart_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        left_panel.addWidget(self.barcode_input)
        left_panel.addWidget(self.cart_table)
        
        # Panel derecho (Cobro y botones táctiles)
        right_panel = QVBoxLayout()
        right_panel.setSpacing(15)
        
        self.lbl_total = QLabel("$ 0.00")
        self.lbl_total.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_total.setStyleSheet("font-size: 64px; font-weight: bold; color: #a6da95; padding: 30px; background-color: #363a4f; border-radius: 12px;")
        
        self.btn_checkout = QPushButton("COBRAR")
        self.btn_checkout.setFixedHeight(80)
        self.btn_checkout.setStyleSheet("background-color: #a6da95; color: #181926; font-size: 24px;")
        
        self.btn_clear = QPushButton("LIMPIAR (Esc)")
        self.btn_clear.setFixedHeight(60)
        self.btn_clear.setStyleSheet("background-color: #ed8796; color: #181926;")

        right_panel.addWidget(self.lbl_total)
        right_panel.addStretch()
        right_panel.addWidget(self.btn_checkout)
        right_panel.addWidget(self.btn_clear)

        main_layout.addLayout(left_panel, stretch=7)
        main_layout.addLayout(right_panel, stretch=3)

    def connect_signals(self):
        # UI -> ViewModel
        self.barcode_input.returnPressed.connect(self._on_barcode_scanned)
        self.btn_checkout.clicked.connect(self.viewmodel.checkout)
        
        # ViewModel -> UI
        self.viewmodel.item_added.connect(self._update_cart_display)
        self.viewmodel.error_occurred.connect(self._show_error)
        self.viewmodel.sale_completed.connect(self._show_success)
        self.viewmodel.total_updated.connect(self.lbl_total.setText)

    def _on_barcode_scanned(self):
        barcode = self.barcode_input.text().strip()
        if barcode:
            self.viewmodel.add_barcode(barcode)
        self.barcode_input.clear()
        self.barcode_input.setFocus() # Re-enfocar para el siguiente escaneo

    def _update_cart_display(self, item_data):
        # Buscar si ya existe la fila
        for row in range(self.cart_table.rowCount()):
            if self.cart_table.item(row, 0).text() == item_data['barcode']:
                self.cart_table.setItem(row, 2, QTableWidgetItem(str(item_data['quantity'])))
                self.cart_table.setItem(row, 3, QTableWidgetItem(f"$ {item_data['quantity']*item_data['price']:,.2f}"))
                return
                
        # Si no existe, agregar fila
        row = self.cart_table.rowCount()
        self.cart_table.insertRow(row)
        self.cart_table.setItem(row, 0, QTableWidgetItem(item_data['barcode']))
        self.cart_table.setItem(row, 1, QTableWidgetItem(item_data['name']))
        self.cart_table.setItem(row, 2, QTableWidgetItem(str(item_data['quantity'])))
        self.cart_table.setItem(row, 3, QTableWidgetItem(f"$ {item_data['quantity']*item_data['price']:,.2f}"))
        self.cart_table.scrollToBottom()

    def _show_error(self, msg):
        QMessageBox.critical(self, "Error", msg)
        self.barcode_input.setFocus()

    def _show_success(self, msg):
        QMessageBox.information(self, "Venta Exitosa", msg)
        self.cart_table.setRowCount(0)
        self.barcode_input.setFocus()
