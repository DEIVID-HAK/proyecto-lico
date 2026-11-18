from dataclasses import dataclass
from enum import Enum

class Role(Enum):
    ADMIN = "ADMIN"          # Puede anular facturas, ver arqueos completos, ajustar kardex
    CASHIER = "CASHIER"      # Solo puede vender y hacer arqueo ciego
    MANAGER = "MANAGER"      # Puede abrir/cerrar turnos, cuadrar domiciliarios

@dataclass
class User:
    id: str
    username: str
    password_hash: str
    role: Role
    is_active: bool = True
