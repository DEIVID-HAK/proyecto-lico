import pytest
from datetime import datetime
from decimal import Decimal

from liquor_pos.core.domain.entities.order import Order, OrderItem, DeliveryDetails, DeliveryStatus, PaymentMethod
from liquor_pos.core.domain.value_objects.money import Money
from liquor_pos.infrastructure.persistence.repositories import SQLAlchemyOrderRepository
from liquor_pos.application.use_cases.delivery_management import SettleDeliveryUseCase
from liquor_pos.application.dtos.delivery_dto import SettleDeliveryDTO

def test_settle_delivery_updates_status_and_payment(db_session):
    order_repo = SQLAlchemyOrderRepository(db_session)
    
    delivery_details = DeliveryDetails(
        customer_name="Juan Perez",
        customer_phone="555-1234",
        customer_address="Calle Falsa 123",
        delivery_person_id="rider-1",
        status=DeliveryStatus.IN_TRANSIT
    )
    
    item = OrderItem(
        product_id="prod-1",
        presentation_id="pres-1",
        quantity=2,
        unit_price=Money(Decimal("10000"))
    )

    order = Order(
        id="order-1",
        timestamp=datetime.now(),
        items=[item],
        delivery_details=delivery_details
    )
    
    order_repo.save(order)
    db_session.commit()
    
    use_case = SettleDeliveryUseCase(order_repo)
    dto = SettleDeliveryDTO(
        order_id="order-1",
        payment_method=PaymentMethod.CASH,
        cash_tendered=50000.0
    )
    
    use_case.execute(dto)
    db_session.commit()
    
    updated_order = order_repo.get_by_id("order-1")
    assert updated_order.delivery_details.status == DeliveryStatus.SETTLED
    assert updated_order.delivery_details.payment_method == PaymentMethod.CASH
    assert updated_order.delivery_details.cash_tendered.amount == Decimal("50000.0")
