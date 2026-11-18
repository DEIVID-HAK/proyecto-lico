from dataclasses import dataclass
from typing import List, Optional

@dataclass
class PresentationDTO:
    name: str
    barcode: str
    units_per_presentation: int
    cost: float
    retail_price: float
    wholesale_price: float

@dataclass
class RegisterProductDTO:
    sku: str
    name: str
    category: str
    alcohol_grade_abv: float
    volume_ml: int
    invima_registration: Optional[str]
    presentations: List[PresentationDTO]
