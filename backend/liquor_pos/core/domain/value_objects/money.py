from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str = "COP"

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Money amount cannot be negative")

    def __add__(self, other: 'Money') -> 'Money':
        if not isinstance(other, Money):
            return NotImplemented
        if self.currency != other.currency:
            raise ValueError("Currencies do not match")
        return Money(self.amount + other.amount, self.currency)

    def __sub__(self, other: 'Money') -> 'Money':
        if not isinstance(other, Money):
            return NotImplemented
        if self.currency != other.currency:
            raise ValueError("Currencies do not match")
        if self.amount < other.amount:
            raise ValueError("Subtraction results in negative money")
        return Money(self.amount - other.amount, self.currency)

    def __mul__(self, multiplier: int | Decimal) -> 'Money':
        if not isinstance(multiplier, (int, Decimal)):
            return NotImplemented
        return Money(self.amount * Decimal(multiplier), self.currency)
