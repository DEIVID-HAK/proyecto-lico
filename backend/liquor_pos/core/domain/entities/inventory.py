from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class MovementType(Enum):
    PURCHASE = "PURCHASE"
    SALE = "SALE"
    WASTE_BREAKAGE = "WASTE_BREAKAGE"
    ADJUSTMENT = "ADJUSTMENT"

@dataclass
class InventoryMovement:
    id: str
    product_id: str
    batch_id: str
    movement_type: MovementType
    quantity_base_units: int
    timestamp: datetime
    notes: str = ""
