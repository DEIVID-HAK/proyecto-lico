from typing import Optional, List
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import select

from liquor_pos.core.ports.repositories import (
    IProductRepository, IBatchRepository, IOrderRepository, IShiftRepository
)
from liquor_pos.core.domain.entities.product import Product, Presentation
from liquor_pos.core.domain.entities.batch import Batch
from liquor_pos.core.domain.entities.order import Order, OrderItem, DeliveryDetails
from liquor_pos.core.domain.entities.shift import CashShift
from liquor_pos.core.domain.value_objects.barcode import Barcode
from liquor_pos.core.domain.value_objects.money import Money
from liquor_pos.core.domain.value_objects.alcohol_grade import AlcoholGrade
from liquor_pos.core.domain.value_objects.volume import VolumeML

from liquor_pos.infrastructure.persistence.models import (
    ProductModel, PresentationModel, BatchModel, OrderModel, OrderItemModel, CashShiftModel
)

class SQLAlchemyProductRepository(IProductRepository):
    def __init__(self, session: Session):
        self.session = session

    def _to_domain(self, model: ProductModel) -> Product:
        presentations = [
            Presentation(
                id=p.id,
                name=p.name,
                barcode=Barcode(p.barcode),
                units_per_presentation=p.units_per_presentation,
                cost=Money(Decimal(str(p.cost_amount)), p.currency),
                retail_price=Money(Decimal(str(p.retail_price_amount)), p.currency),
                wholesale_price=Money(Decimal(str(p.wholesale_price_amount)), p.currency)
            ) for p in model.presentations
        ]
        
        return Product(
            id=model.id,
            sku=model.sku,
            name=model.name,
            category=model.category,
            alcohol_grade=AlcoholGrade(model.alcohol_grade_abv),
            volume=VolumeML(model.volume_ml),
            invima_registration=model.invima_registration,
            presentations=presentations
        )

    def get_by_id(self, product_id: str) -> Optional[Product]:
        stmt = select(ProductModel).where(ProductModel.id == product_id)
        model = self.session.execute(stmt).scalar_one_or_none()
        return self._to_domain(model) if model else None

    def get_all(self) -> List[Product]:
        stmt = select(ProductModel)
        models = self.session.execute(stmt).scalars().all()
        return [self._to_domain(m) for m in models]

    def get_by_sku(self, sku: str) -> Optional[Product]:
        stmt = select(ProductModel).where(ProductModel.sku == sku)
        model = self.session.execute(stmt).scalar_one_or_none()
        return self._to_domain(model) if model else None

    def get_by_barcode(self, barcode: str) -> Optional[Product]:
        stmt = select(ProductModel).join(ProductModel.presentations).where(PresentationModel.barcode == barcode)
        model = self.session.execute(stmt).scalar_one_or_none()
        return self._to_domain(model) if model else None

    def save(self, product: Product) -> None:
        model = self.session.execute(select(ProductModel).where(ProductModel.id == product.id)).scalar_one_or_none()
        if not model:
            model = ProductModel(id=product.id)
            self.session.add(model)
            
        model.sku = product.sku
        model.name = product.name
        model.category = product.category
        model.alcohol_grade_abv = product.alcohol_grade.abv
        model.volume_ml = product.volume.ml
        model.invima_registration = product.invima_registration
        
        existing_pres_map = {p.id: p for p in model.presentations}
        for pres in product.presentations:
            if pres.id in existing_pres_map:
                pm = existing_pres_map[pres.id]
                pm.name = pres.name
                pm.barcode = pres.barcode.value
                pm.units_per_presentation = pres.units_per_presentation
                pm.cost_amount = float(pres.cost.amount)
                pm.retail_price_amount = float(pres.retail_price.amount)
                pm.wholesale_price_amount = float(pres.wholesale_price.amount)
                pm.currency = pres.cost.currency
            else:
                pm = PresentationModel(
                    id=pres.id,
                    name=pres.name,
                    barcode=pres.barcode.value,
                    units_per_presentation=pres.units_per_presentation,
                    cost_amount=float(pres.cost.amount),
                    retail_price_amount=float(pres.retail_price.amount),
                    wholesale_price_amount=float(pres.wholesale_price.amount),
                    currency=pres.cost.currency
                )
                model.presentations.append(pm)

class SQLAlchemyBatchRepository(IBatchRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, batch_id: str) -> Optional[Batch]:
        # BLOQUEO PESIMISTA: SELECT ... FOR UPDATE
        stmt = select(BatchModel).where(BatchModel.id == batch_id).with_for_update()
        model = self.session.execute(stmt).scalar_one_or_none()
        
        if not model:
            return None
            
        return Batch(
            id=model.id,
            product_id=model.product_id,
            batch_number=model.batch_number,
            expiration_date=model.expiration_date,
            stock_base_units=model.stock_base_units
        )

    def get_by_product_id(self, product_id: str) -> List[Batch]:
        stmt = select(BatchModel).where(BatchModel.product_id == product_id).order_by(BatchModel.expiration_date)
        models = self.session.execute(stmt).scalars().all()
        return [
            Batch(
                id=m.id,
                product_id=m.product_id,
                batch_number=m.batch_number,
                expiration_date=m.expiration_date,
                stock_base_units=m.stock_base_units
            ) for m in models
        ]

    def save(self, batch: Batch) -> None:
        model = self.session.execute(select(BatchModel).where(BatchModel.id == batch.id)).scalar_one_or_none()
        if not model:
            model = BatchModel(id=batch.id)
            self.session.add(model)
            
        model.product_id = batch.product_id
        model.batch_number = batch.batch_number
        model.expiration_date = batch.expiration_date
        model.stock_base_units = batch.stock_base_units

class SQLAlchemyOrderRepository(IOrderRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, order_id: str) -> Optional[Order]:
        stmt = select(OrderModel).where(OrderModel.id == order_id)
        model = self.session.execute(stmt).scalar_one_or_none()
        if not model:
            return None
            
        items = [
            OrderItem(
                product_id=i.product_id,
                presentation_id=i.presentation_id,
                quantity=i.quantity,
                unit_price=Money(Decimal(str(i.unit_price_amount)), i.currency)
            ) for i in model.items
        ]
        
        delivery_details = None
        if model.is_delivery:
            delivery_details = DeliveryDetails(
                customer_name=model.customer_name or "",
                customer_phone=model.customer_phone or "",
                customer_address=model.customer_address or "",
                delivery_person_id=model.delivery_person_id,
                status=model.delivery_status,
                payment_method=model.payment_method,
                cash_tendered=Money(Decimal(str(model.cash_tendered_amount))) if model.cash_tendered_amount is not None else None
            )
            
        return Order(
            id=model.id,
            timestamp=model.timestamp,
            items=items,
            delivery_details=delivery_details
        )

    def save(self, order: Order) -> None:
        model = self.session.execute(select(OrderModel).where(OrderModel.id == order.id)).scalar_one_or_none()
        if not model:
            model = OrderModel(id=order.id)
            self.session.add(model)
            
        model.timestamp = order.timestamp
        
        if order.delivery_details:
            model.is_delivery = True
            model.customer_name = order.delivery_details.customer_name
            model.customer_phone = order.delivery_details.customer_phone
            model.customer_address = order.delivery_details.customer_address
            model.delivery_person_id = order.delivery_details.delivery_person_id
            model.delivery_status = order.delivery_details.status
            model.payment_method = order.delivery_details.payment_method
            model.cash_tendered_amount = float(order.delivery_details.cash_tendered.amount) if order.delivery_details.cash_tendered else None
        else:
            model.is_delivery = False
            
        for old_item in list(model.items):
            self.session.delete(old_item)
            
        for item in order.items:
            model.items.append(OrderItemModel(
                product_id=item.product_id,
                presentation_id=item.presentation_id,
                quantity=item.quantity,
                unit_price_amount=float(item.unit_price.amount),
                currency=item.unit_price.currency
            ))

class SQLAlchemyShiftRepository(IShiftRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_open_shift(self) -> Optional[CashShift]:
        stmt = select(CashShiftModel).where(CashShiftModel.end_time.is_(None))
        model = self.session.execute(stmt).scalar_one_or_none()
        if not model:
            return None
            
        return CashShift(
            id=model.id,
            cashier_id=model.cashier_id,
            start_time=model.start_time,
            base_amount=Money(Decimal(str(model.base_amount)), model.currency),
            end_time=model.end_time,
            declared_cash=Money(Decimal(str(model.declared_cash_amount)), model.currency) if model.declared_cash_amount is not None else None
        )

    def save(self, shift: CashShift) -> None:
        model = self.session.execute(select(CashShiftModel).where(CashShiftModel.id == shift.id)).scalar_one_or_none()
        if not model:
            model = CashShiftModel(id=shift.id)
            self.session.add(model)
            
        model.cashier_id = shift.cashier_id
        model.start_time = shift.start_time
        model.base_amount = float(shift.base_amount.amount)
        model.end_time = shift.end_time
        model.declared_cash_amount = float(shift.declared_cash.amount) if shift.declared_cash else None
        model.currency = shift.base_amount.currency

from liquor_pos.core.ports.repositories import IUserRepository, IAuditRepository
from liquor_pos.core.domain.entities.user import User
from liquor_pos.core.domain.entities.audit import AuditLog
from liquor_pos.infrastructure.persistence.models import UserModel, AuditLogModel

class SQLAlchemyUserRepository(IUserRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_by_username(self, username: str) -> Optional[User]:
        stmt = select(UserModel).where(UserModel.username == username)
        model = self.session.execute(stmt).scalar_one_or_none()
        if not model:
            return None
        return User(
            id=model.id,
            username=model.username,
            password_hash=model.password_hash,
            role=model.role,
            is_active=model.is_active
        )

    def save(self, user: User) -> None:
        model = self.session.execute(select(UserModel).where(UserModel.id == user.id)).scalar_one_or_none()
        if not model:
            model = UserModel(id=user.id)
            self.session.add(model)
        
        model.username = user.username
        model.password_hash = user.password_hash
        model.role = user.role
        model.is_active = user.is_active

class SQLAlchemyAuditRepository(IAuditRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, log: AuditLog) -> None:
        model = AuditLogModel(
            id=log.id,
            timestamp=log.timestamp,
            user_id=log.user_id,
            action=log.action,
            entity_id=log.entity_id,
            reason=log.reason,
            metadata_dump=log.metadata_dump
        )
        self.session.add(model)

