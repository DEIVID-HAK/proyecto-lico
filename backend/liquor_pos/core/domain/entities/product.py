from dataclasses import dataclass, field
from typing import List, Optional
from liquor_pos.core.domain.value_objects.barcode import Barcode
from liquor_pos.core.domain.value_objects.money import Money
from liquor_pos.core.domain.value_objects.alcohol_grade import AlcoholGrade
from liquor_pos.core.domain.value_objects.volume import VolumeML

@dataclass
class Presentation:
    id: str
    name: str  # e.g., "Botella individual", "Six-pack"
    barcode: Barcode
    units_per_presentation: int
    cost: Money
    retail_price: Money
    wholesale_price: Money

    def __post_init__(self):
        if self.units_per_presentation <= 0:
            raise ValueError("Units per presentation must be greater than 0")

@dataclass
class Product:
    id: str
    sku: str
    name: str
    category: str
    alcohol_grade: AlcoholGrade
    volume: VolumeML
    invima_registration: Optional[str]
    presentations: List[Presentation] = field(default_factory=list)

    def __post_init__(self):
        if self.alcohol_grade.abv > 0 and not self.invima_registration:
            raise ValueError("INVIMA registration is mandatory for alcoholic beverages")
