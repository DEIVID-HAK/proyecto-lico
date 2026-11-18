import pytest
from decimal import Decimal
from datetime import date

from liquor_pos.core.domain.entities.product import Product, Presentation
from liquor_pos.core.domain.entities.batch import Batch
from liquor_pos.core.domain.value_objects.barcode import Barcode
from liquor_pos.core.domain.value_objects.money import Money
from liquor_pos.core.domain.value_objects.alcohol_grade import AlcoholGrade
from liquor_pos.core.domain.value_objects.volume import VolumeML

from liquor_pos.infrastructure.persistence.repositories import (
    SQLAlchemyProductRepository, SQLAlchemyBatchRepository, SQLAlchemyOrderRepository
)
from liquor_pos.application.use_cases.sales_counter import ProcessCounterSaleUseCase
from liquor_pos.application.dtos.sale_dto import CounterSaleDTO, SaleItemDTO

def test_process_counter_sale_deducts_inventory_fifo(db_session):
    product_repo = SQLAlchemyProductRepository(db_session)
    batch_repo = SQLAlchemyBatchRepository(db_session)
    order_repo = SQLAlchemyOrderRepository(db_session)

    # 1. Setup Product and Presentation
    presentation = Presentation(
        id="pres-1",
        name="Caja x 12",
        barcode=Barcode("123456789"),
        units_per_presentation=12,
        cost=Money(Decimal("50000")),
        retail_price=Money(Decimal("70000")),
        wholesale_price=Money(Decimal("65000"))
    )

    product = Product(
        id="prod-1",
        sku="SKU-AGUAR-001",
        name="Aguardiente Blanco",
        category="Aguardiente",
        alcohol_grade=AlcoholGrade(29.0),
        volume=VolumeML(750),
        invima_registration="INV123",
        presentations=[presentation]
    )
    product_repo.save(product)

    # 2. Setup Batches (FIFO requires multiple batches)
    # Lote 1 vence antes, se consume primero
    batch1 = Batch(id="batch-1", product_id="prod-1", batch_number="L01", expiration_date=date(2025, 1, 1), stock_base_units=10)
    batch2 = Batch(id="batch-2", product_id="prod-1", batch_number="L02", expiration_date=date(2025, 12, 1), stock_base_units=20)
    batch_repo.save(batch1)
    batch_repo.save(batch2)
    
    db_session.commit()

    # 3. Process Sale: Vender 1 caja (12 unidades base)
    use_case = ProcessCounterSaleUseCase(product_repo, batch_repo, order_repo)
    dto = CounterSaleDTO(items=[SaleItemDTO(barcode="123456789", quantity=1)])
    
    order = use_case.execute(dto)
    db_session.commit()

    # 4. Assertions
    assert len(order.items) == 1
    
    # Check inventory deduction FIFO
    b1_after = batch_repo.get_by_id("batch-1")
    b2_after = batch_repo.get_by_id("batch-2")
    
    assert b1_after.stock_base_units == 0 # Debería agotar todo el lote 1
    assert b2_after.stock_base_units == 18 # Debería tomar las 2 unidades restantes del lote 2
