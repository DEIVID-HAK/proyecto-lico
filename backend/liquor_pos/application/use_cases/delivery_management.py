from decimal import Decimal
from liquor_pos.core.ports.repositories import IOrderRepository
from liquor_pos.core.domain.entities.order import DeliveryStatus
from liquor_pos.core.domain.value_objects.money import Money
from liquor_pos.application.dtos.delivery_dto import DispatchDeliveryDTO, SettleDeliveryDTO

class DispatchDeliveryUseCase:
    def __init__(self, order_repo: IOrderRepository):
        self.order_repo = order_repo

    def execute(self, dto: DispatchDeliveryDTO) -> None:
        order = self.order_repo.get_by_id(dto.order_id)
        if not order or not order.delivery_details:
            raise ValueError("Delivery order not found")
            
        if order.delivery_details.status not in (DeliveryStatus.PREPARING, DeliveryStatus.PENDING):
            raise ValueError(f"Cannot dispatch order in status {order.delivery_details.status}")

        order.delivery_details.delivery_person_id = dto.delivery_person_id
        order.delivery_details.status = DeliveryStatus.IN_TRANSIT
        
        self.order_repo.save(order)

class SettleDeliveryUseCase:
    def __init__(self, order_repo: IOrderRepository):
        self.order_repo = order_repo

    def execute(self, dto: SettleDeliveryDTO) -> None:
        order = self.order_repo.get_by_id(dto.order_id)
        if not order or not order.delivery_details:
            raise ValueError("Delivery order not found")

        if order.delivery_details.status != DeliveryStatus.IN_TRANSIT:
            raise ValueError("Cannot settle an order that is not in transit")

        order.delivery_details.payment_method = dto.payment_method
        if dto.cash_tendered is not None:
            order.delivery_details.cash_tendered = Money(Decimal(str(dto.cash_tendered)))
            
        order.delivery_details.status = DeliveryStatus.SETTLED
        
        self.order_repo.save(order)
