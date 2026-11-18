from typing import List
from datetime import datetime
import uuid

from liquor_pos.core.ports.repositories import IProductRepository, IBatchRepository, IOrderRepository
from liquor_pos.core.domain.entities.order import Order, OrderItem
from liquor_pos.core.domain.exceptions.base import DomainException
from liquor_pos.application.dtos.sale_dto import CounterSaleDTO

class ProcessCounterSaleUseCase:
    def __init__(self, product_repo: IProductRepository, batch_repo: IBatchRepository, order_repo: IOrderRepository):
        self.product_repo = product_repo
        self.batch_repo = batch_repo
        self.order_repo = order_repo

    def execute(self, dto: CounterSaleDTO) -> Order:
        order_items = []
        
        for item_dto in dto.items:
            product = self.product_repo.get_by_barcode(item_dto.barcode)
            if not product:
                raise ValueError(f"Product with barcode {item_dto.barcode} not found")
                
            presentation = next((p for p in product.presentations if p.barcode.value == item_dto.barcode), None)
            if not presentation:
                raise ValueError(f"Presentation for barcode {item_dto.barcode} not found in product")

            # Descuento de inventario (Estrategia FIFO)
            units_to_deduct = item_dto.quantity * presentation.units_per_presentation
            batches = self.batch_repo.get_by_product_id(product.id)
            
            for batch in batches:
                if units_to_deduct == 0:
                    break
                    
                # Recargamos el batch con FOR UPDATE para evitar colisiones
                locked_batch = self.batch_repo.get_by_id(batch.id)
                if not locked_batch:
                    continue

                available = locked_batch.stock_base_units
                if available > 0:
                    deduct_amount = min(available, units_to_deduct)
                    locked_batch.deduct_stock(deduct_amount)
                    self.batch_repo.save(locked_batch)
                    units_to_deduct -= deduct_amount

            if units_to_deduct > 0:
                raise DomainException(f"Not enough stock for product {product.name}. Missing {units_to_deduct} base units.")

            order_items.append(
                OrderItem(
                    product_id=product.id,
                    presentation_id=presentation.id,
                    quantity=item_dto.quantity,
                    unit_price=presentation.retail_price
                )
            )

        order = Order(
            id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            items=order_items
        )
        
        self.order_repo.save(order)
        return order
