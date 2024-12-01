from typing import NamedTuple
from dataclasses import dataclass

class UserData(NamedTuple):
    img_width_in_pixels: int
    img_height_in_pixels: int
    iterations_number: int
    transformer_function_set: set[int]


AffineCoefficients = tuple[float, float, float, float, float, float]

@dataclass(frozen= True)
class AffineTransformation:
    a: float
    b: float
    c: float
    d: float
    e: float
    f: float

    red: int
    green: int
    blue: int