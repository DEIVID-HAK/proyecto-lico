from typing import List
import uuid
from decimal import Decimal

from liquor_pos.core.ports.repositories import IProductRepository
from liquor_pos.core.domain.entities.product import Product, Presentation
from liquor_pos.core.domain.value_objects.barcode import Barcode
from liquor_pos.core.domain.value_objects.money import Money
from liquor_pos.core.domain.value_objects.alcohol_grade import AlcoholGrade
from liquor_pos.core.domain.value_objects.volume import VolumeML
from liquor_pos.application.dtos.product_dto import RegisterProductDTO

class RegisterProductUseCase:
    def __init__(self, product_repo: IProductRepository):
        self.product_repo = product_repo

    def execute(self, dto: RegisterProductDTO) -> Product:
        # Check if product with SKU already exists
        if self.product_repo.get_by_sku(dto.sku):
            raise ValueError(f"Product with SKU {dto.sku} already exists")

        presentations = []
        for p_dto in dto.presentations:
            presentations.append(
                Presentation(
                    id=str(uuid.uuid4()),
                    name=p_dto.name,
                    barcode=Barcode(p_dto.barcode),
                    units_per_presentation=p_dto.units_per_presentation,
                    cost=Money(Decimal(str(p_dto.cost))),
                    retail_price=Money(Decimal(str(p_dto.retail_price))),
                    wholesale_price=Money(Decimal(str(p_dto.wholesale_price)))
                )
            )

        product = Product(
            id=str(uuid.uuid4()),
            sku=dto.sku,
            name=dto.name,
            category=dto.category,
            alcohol_grade=AlcoholGrade(dto.alcohol_grade_abv),
            volume=VolumeML(dto.volume_ml),
            invima_registration=dto.invima_registration,
            presentations=presentations
        )

        self.product_repo.save(product)
        return product
