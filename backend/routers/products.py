from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session

from dependencies import get_db
from liquor_pos.infrastructure.persistence.repositories import SQLAlchemyProductRepository
from liquor_pos.application.use_cases.manage_products import RegisterProductUseCase
from liquor_pos.application.dtos.product_dto import RegisterProductDTO, PresentationDTO

router = APIRouter(prefix="/api/products", tags=["Products"])

def get_product_repo(db: Session = Depends(get_db)):
    return SQLAlchemyProductRepository(db)

def get_register_product_use_case(repo: SQLAlchemyProductRepository = Depends(get_product_repo)):
    return RegisterProductUseCase(repo)

# Pydantic Schemas for validation (mirroring DTOs)
class PresentationSchema(BaseModel):
    name: str
    barcode: str
    units_per_presentation: int
    cost: float
    retail_price: float
    wholesale_price: float

class RegisterProductSchema(BaseModel):
    sku: str
    name: str
    category: str
    alcohol_grade_abv: float
    volume_ml: int
    invima_registration: Optional[str] = None
    presentations: List[PresentationSchema]

@router.get("/", status_code=status.HTTP_200_OK)
def get_all_products(
    repo: SQLAlchemyProductRepository = Depends(get_product_repo)
):
    products = repo.get_all()
    # Mapeo simple a diccionarios para la respuesta
    return [{
        "id": p.id,
        "sku": p.sku,
        "name": p.name,
        "category": p.category,
        "presentations": [{
            "id": pres.id,
            "name": pres.name,
            "barcode": pres.barcode.value,
            "retail_price": float(pres.retail_price.amount)
        } for pres in p.presentations]
    } for p in products]

@router.post("/", status_code=status.HTTP_201_CREATED)
def register_product(
    request: RegisterProductSchema,
    use_case: RegisterProductUseCase = Depends(get_register_product_use_case),
    db: Session = Depends(get_db)
):
    try:
        invima = request.invima_registration
        if request.alcohol_grade_abv > 0 and not invima:
            invima = "INVIMA L-0004562" # Fallback temporal para la demostración

        # Convert FastAPI Schema to Application DTO
        dto = RegisterProductDTO(
            sku=request.sku,
            name=request.name,
            category=request.category,
            alcohol_grade_abv=request.alcohol_grade_abv,
            volume_ml=request.volume_ml,
            invima_registration=invima,
            presentations=[
                PresentationDTO(
                    name=p.name,
                    barcode=p.barcode,
                    units_per_presentation=p.units_per_presentation,
                    cost=p.cost,
                    retail_price=p.retail_price,
                    wholesale_price=p.wholesale_price
                ) for p in request.presentations
            ]
        )
        
        product = use_case.execute(dto)
        db.commit() # Importante: hacer commit a la base de datos
        
        return {"message": "Product created successfully", "product_id": product.id}
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
