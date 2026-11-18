from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from liquor_pos.core.domain.value_objects.money import Money

@dataclass
class CashShift:
    id: str
    cashier_id: str
    start_time: datetime
    base_amount: Money
    end_time: Optional[datetime] = None
    declared_cash: Optional[Money] = None
    
    def close_shift(self, declared_cash: Money, end_time: datetime):
        self.declared_cash = declared_cash
        self.end_time = end_time

    @property
    def is_open(self) -> bool:
        return self.end_time is None
