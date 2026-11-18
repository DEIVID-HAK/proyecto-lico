from dataclasses import dataclass

@dataclass(frozen=True)
class AlcoholGrade:
    abv: float

    def __post_init__(self):
        if self.abv < 0.0 or self.abv > 100.0:
            raise ValueError("ABV must be between 0 and 100")
