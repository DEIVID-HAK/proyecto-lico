class DomainException(Exception):
    """Base exception for all domain errors"""
    pass

class NegativeStockError(DomainException):
    """Raised when an operation would result in negative stock"""
    pass

class RaceConditionError(DomainException):
    """Raised when an optimistic lock fails or a concurrency issue is detected"""
    pass
