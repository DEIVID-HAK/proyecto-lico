from PySide6.QtCore import QObject, Signal, Slot
from liquor_pos.application.use_cases.sales_counter import ProcessCounterSaleUseCase
from liquor_pos.application.dtos.sale_dto import CounterSaleDTO, SaleItemDTO

class POSViewModel(QObject):
    # Señales para notificar a la vista (Event-Driven UI)
    item_added = Signal(dict)
    sale_completed = Signal(str)
    error_occurred = Signal(str)
    total_updated = Signal(str)

    def __init__(self, sale_use_case: ProcessCounterSaleUseCase):
        super().__init__()
        self.sale_use_case = sale_use_case
        self.cart_items = []

    @Slot(str)
    def add_barcode(self, barcode: str):
        # TODO: Consultar DTO o servicio de búsqueda de producto por código de barras.
        # Datos simulados temporalmente para la UI
        found = False
        for item in self.cart_items:
            if item['barcode'] == barcode:
                item['quantity'] += 1
                found = True
                break
        
        if not found:
            self.cart_items.append({'barcode': barcode, 'quantity': 1, 'name': f"Producto {barcode}", 'price': 15000})
        
        added_item = next(i for i in self.cart_items if i['barcode'] == barcode)
        self.item_added.emit(added_item)
        
        # Recalcular total
        total = sum(i['price'] * i['quantity'] for i in self.cart_items)
        self.total_updated.emit(f"$ {total:,.2f}")

    @Slot()
    def checkout(self):
        if not self.cart_items:
            self.error_occurred.emit("El carrito está vacío.")
            return
            
        try:
            dto_items = [SaleItemDTO(barcode=i['barcode'], quantity=i['quantity']) for i in self.cart_items]
            dto = CounterSaleDTO(items=dto_items)
            
            if self.sale_use_case:
                order = self.sale_use_case.execute(dto)
                order_id = order.id
            else:
                # Fallback para pruebas de UI puras
                order_id = "TEST-ORDER-123"
            
            # Limpiar estado tras éxito
            self.cart_items.clear()
            self.sale_completed.emit(f"Venta registrada. Orden ID: {order_id}")
            self.total_updated.emit("$ 0.00")
            
        except Exception as e:
            self.error_occurred.emit(str(e))
