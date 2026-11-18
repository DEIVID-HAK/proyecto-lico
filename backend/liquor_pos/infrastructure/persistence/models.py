from datetime import datetime, date
from typing import List, Optional
from sqlalchemy import String, Integer, Numeric, ForeignKey, DateTime, Date, Enum as SQLEnum, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from liquor_pos.infrastructure.persistence.database import Base
from liquor_pos.core.domain.entities.order import DeliveryStatus, PaymentMethod
from liquor_pos.core.domain.entities.inventory import MovementType

class ProductModel(Base):
    __tablename__ = "products"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    sku: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(200))
    category: Mapped[str] = mapped_column(String(100))
    alcohol_grade_abv: Mapped[float] = mapped_column(Float)
    volume_ml: Mapped[int] = mapped_column(Integer)
    invima_registration: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    presentations: Mapped[List["PresentationModel"]] = relationship(back_populates="product", cascade="all, delete-orphan")
    batches: Mapped[List["BatchModel"]] = relationship(back_populates="product", cascade="all, delete-orphan")

class PresentationModel(Base):
    __tablename__ = "presentations"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    product_id: Mapped[str] = mapped_column(ForeignKey("products.id"), index=True)
    name: Mapped[str] = mapped_column(String(100))
    barcode: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    units_per_presentation: Mapped[int] = mapped_column(Integer)
    cost_amount: Mapped[float] = mapped_column(Numeric(15, 2))
    retail_price_amount: Mapped[float] = mapped_column(Numeric(15, 2))
    wholesale_price_amount: Mapped[float] = mapped_column(Numeric(15, 2))
    currency: Mapped[str] = mapped_column(String(3), default="COP")

    product: Mapped["ProductModel"] = relationship(back_populates="presentations")

class BatchModel(Base):
    __tablename__ = "batches"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    product_id: Mapped[str] = mapped_column(ForeignKey("products.id"), index=True)
    batch_number: Mapped[str] = mapped_column(String(100))
    expiration_date: Mapped[date] = mapped_column(Date)
    stock_base_units: Mapped[int] = mapped_column(Integer)

    product: Mapped["ProductModel"] = relationship(back_populates="batches")

class InventoryMovementModel(Base):
    __tablename__ = "inventory_movements"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    product_id: Mapped[str] = mapped_column(ForeignKey("products.id"))
    batch_id: Mapped[str] = mapped_column(ForeignKey("batches.id"))
    movement_type: Mapped[MovementType] = mapped_column(SQLEnum(MovementType))
    quantity_base_units: Mapped[int] = mapped_column(Integer)
    timestamp: Mapped[datetime] = mapped_column(DateTime)
    notes: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

class OrderModel(Base):
    __tablename__ = "orders"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime)
    
    # Delivery details (nullable, only if order is a delivery)
    is_delivery: Mapped[bool] = mapped_column(default=False)
    customer_name: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    customer_phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    customer_address: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    delivery_person_id: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    delivery_status: Mapped[Optional[DeliveryStatus]] = mapped_column(SQLEnum(DeliveryStatus), nullable=True)
    payment_method: Mapped[Optional[PaymentMethod]] = mapped_column(SQLEnum(PaymentMethod), nullable=True)
    cash_tendered_amount: Mapped[Optional[float]] = mapped_column(Numeric(15, 2), nullable=True)

    items: Mapped[List["OrderItemModel"]] = relationship(back_populates="order", cascade="all, delete-orphan")

class OrderItemModel(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[str] = mapped_column(ForeignKey("orders.id"), index=True)
    product_id: Mapped[str] = mapped_column(String(50))
    presentation_id: Mapped[str] = mapped_column(String(50))
    quantity: Mapped[int] = mapped_column(Integer)
    unit_price_amount: Mapped[float] = mapped_column(Numeric(15, 2))
    currency: Mapped[str] = mapped_column(String(3), default="COP")

    order: Mapped["OrderModel"] = relationship(back_populates="items")

class CashShiftModel(Base):
    __tablename__ = "cash_shifts"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    cashier_id: Mapped[str] = mapped_column(String(50), index=True)
    start_time: Mapped[datetime] = mapped_column(DateTime)
    base_amount: Mapped[float] = mapped_column(Numeric(15, 2))
    end_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    declared_cash_amount: Mapped[Optional[float]] = mapped_column(Numeric(15, 2), nullable=True)
    currency: Mapped[str] = mapped_column(String(3), default="COP")

from liquor_pos.core.domain.entities.user import Role
from liquor_pos.core.domain.entities.audit import AuditAction
from sqlalchemy import Boolean, Text

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[Role] = mapped_column(SQLEnum(Role))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

class AuditLogModel(Base):
    __tablename__ = "audit_logs"

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, index=True)
    user_id: Mapped[str] = mapped_column(String(50), index=True)
    action: Mapped[AuditAction] = mapped_column(SQLEnum(AuditAction))
    entity_id: Mapped[str] = mapped_column(String(100), index=True)
    reason: Mapped[str] = mapped_column(String(500))
    metadata_dump: Mapped[str] = mapped_column(Text)

