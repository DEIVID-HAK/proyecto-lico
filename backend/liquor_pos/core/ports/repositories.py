from typing import Protocol, Optional, List
from liquor_pos.core.domain.entities.product import Product
from liquor_pos.core.domain.entities.batch import Batch
from liquor_pos.core.domain.entities.order import Order
from liquor_pos.core.domain.entities.shift import CashShift

class IProductRepository(Protocol):
    def get_by_id(self, product_id: str) -> Optional[Product]:
        ...
        
    def get_all(self) -> List[Product]:
        ...
        
    def get_by_sku(self, sku: str) -> Optional[Product]:
        ...

    def get_by_barcode(self, barcode: str) -> Optional[Product]:
        ...
        
    def save(self, product: Product) -> None:
        ...

class IBatchRepository(Protocol):
    def get_by_id(self, batch_id: str) -> Optional[Batch]:
        ...
        
    def get_by_product_id(self, product_id: str) -> List[Batch]:
        ...
        
    def save(self, batch: Batch) -> None:
        ...

class IOrderRepository(Protocol):
    def get_by_id(self, order_id: str) -> Optional[Order]:
        ...
        
    def save(self, order: Order) -> None:
        ...

class IShiftRepository(Protocol):
    def get_open_shift(self) -> Optional[CashShift]:
        ...
        
    def save(self, shift: CashShift) -> None:
        ...

from liquor_pos.core.domain.entities.user import User
class IUserRepository(Protocol):
    def get_by_username(self, username: str) -> Optional[User]:
        ...
    def save(self, user: User) -> None:
        ...

from liquor_pos.core.domain.entities.audit import AuditLog
class IAuditRepository(Protocol):
    def save(self, log: AuditLog) -> None:
        ...

