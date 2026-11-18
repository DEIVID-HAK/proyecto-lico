from dataclasses import dataclass

@dataclass(frozen=True)
class VolumeML:
    ml: int

    def __post_init__(self):
        if self.ml <= 0:
            raise ValueError("Volume must be greater than 0 ml")
