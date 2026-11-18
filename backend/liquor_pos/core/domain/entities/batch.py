from dataclasses import dataclass
from datetime import date
from liquor_pos.core.domain.exceptions.base import NegativeStockError

@dataclass
class Batch:
    id: str
    product_id: str
    batch_number: str
    expiration_date: date
    stock_base_units: int

    def __post_init__(self):
        if self.stock_base_units < 0:
            raise NegativeStockError("Stock cannot be negative")

    def deduct_stock(self, quantity: int):
        if quantity < 0:
            raise ValueError("Quantity to deduct must be positive")
        if self.stock_base_units < quantity:
            raise NegativeStockError(f"Cannot deduct {quantity} units. Only {self.stock_base_units} available.")
        self.stock_base_units -= quantity

    def add_stock(self, quantity: int):
        if quantity < 0:
            raise ValueError("Quantity to add must be positive")
        self.stock_base_units += quantity
