from typing import NamedTuple
from dataclasses import dataclass
from math import log10

ImageCoordsAlias =  tuple[int, int]
PointCoordsAlias = tuple[float, float]

class UserData(NamedTuple):
    img_width_in_pixels: int
    img_height_in_pixels: int
    iterations_number: int
    transformer_function_set: set[int]


@dataclass
class Pixel:
    red: int = 0
    green: int = 0
    blue: int = 0
    counter: int = 0
    normal: float = 1.0

    def increment_counter(self)->None:
        self.counter+=1

    def update_color(self,new_red:int, new_green: int, new_blue: int)-> None:
        self.red = (self.red+ new_red)//2
        self.green = (self.green+ new_green)//2
        self.blue = (self.blue+ new_blue)//2

    def update_normal(self):
        if self.counter:
            self.normal: float = log10(self.counter)



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
    
    def apply_affine_transformation(self, x:float, y: float)->PointCoordsAlias:
        return self.a *x  +self.b *y + self.c, self.d *x +self.e *y + self.f
    

