from dataclasses import dataclass

@dataclass(frozen=True)
class Barcode:
    value: str

    def __post_init__(self):
        if not self.value:
            raise ValueError("Barcode cannot be empty")
        if not self.value.isalnum():
            raise ValueError("Barcode must be alphanumeric")
