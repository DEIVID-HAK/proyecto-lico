import uuid
import json
from datetime import datetime
from liquor_pos.core.domain.entities.audit import AuditLog, AuditAction
from liquor_pos.core.ports.repositories import IAuditRepository

class AuditService:
    def __init__(self, audit_repo: IAuditRepository):
        self.audit_repo = audit_repo

    def log_action(self, user_id: str, action: AuditAction, entity_id: str, reason: str, old_state: dict, new_state: dict):
        if not reason or len(reason.strip()) < 5:
            raise ValueError("Se requiere una justificación válida para esta operación sensible.")
            
        metadata = json.dumps({"old": old_state, "new": new_state})
        
        log = AuditLog(
            id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            user_id=user_id,
            action=action,
            entity_id=entity_id,
            reason=reason,
            metadata_dump=metadata
        )
        
        self.audit_repo.save(log)
