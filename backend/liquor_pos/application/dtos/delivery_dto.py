from dataclasses import dataclass
from typing import Optional
from liquor_pos.core.domain.entities.order import PaymentMethod

@dataclass
class DispatchDeliveryDTO:
    order_id: str
    delivery_person_id: str

@dataclass
class SettleDeliveryDTO:
    order_id: str
    payment_method: PaymentMethod
    cash_tendered: Optional[float] = None
