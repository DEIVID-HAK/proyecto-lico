from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional
from liquor_pos.core.domain.value_objects.money import Money

class DeliveryStatus(Enum):
    PENDING = "PENDING"
    PREPARING = "PREPARING"
    IN_TRANSIT = "IN_TRANSIT"
    DELIVERED = "DELIVERED"
    SETTLED = "SETTLED"

class PaymentMethod(Enum):
    CASH = "CASH"
    NEQUI = "NEQUI"
    DAVIPLATA = "DAVIPLATA"
    DATAPHONE = "DATAPHONE"

@dataclass
class OrderItem:
    product_id: str
    presentation_id: str
    quantity: int
    unit_price: Money

    @property
    def subtotal(self) -> Money:
        from decimal import Decimal
        return self.unit_price * Decimal(self.quantity)

@dataclass
class DeliveryDetails:
    customer_name: str
    customer_phone: str
    customer_address: str
    delivery_person_id: Optional[str] = None
    status: DeliveryStatus = DeliveryStatus.PENDING
    payment_method: Optional[PaymentMethod] = None
    cash_tendered: Optional[Money] = None

@dataclass
class Order:
    id: str
    timestamp: datetime
    items: List[OrderItem] = field(default_factory=list)
    delivery_details: Optional[DeliveryDetails] = None
    
    @property
    def total(self) -> Money:
        from decimal import Decimal
        if not self.items:
            return Money(Decimal('0'))
        total_amount = sum(item.subtotal.amount for item in self.items)
        return Money(total_amount, self.items[0].subtotal.currency)
