from dataclasses import dataclass
from typing import List

@dataclass
class SaleItemDTO:
    barcode: str
    quantity: int

@dataclass
class CounterSaleDTO:
    items: List[SaleItemDTO]
