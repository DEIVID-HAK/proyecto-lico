from dataclasses import dataclass
from datetime import datetime
from enum import Enum

class AuditAction(Enum):
    VOID_TICKET = "VOID_TICKET"
    REOPEN_SHIFT = "REOPEN_SHIFT"
    MANUAL_STOCK_ADJUSTMENT = "MANUAL_STOCK_ADJUSTMENT"
    CASH_DRAWER_OPENED = "CASH_DRAWER_OPENED"

@dataclass
class AuditLog:
    id: str
    timestamp: datetime
    user_id: str
    action: AuditAction
    entity_id: str  # ID de la orden, turno o producto afectado
    reason: str     # Justificación obligatoria
    metadata_dump: str # JSON con el estado anterior y nuevo
