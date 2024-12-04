from typing import NamedTuple
from dataclasses import dataclass

ImageCoordsAlias =  tuple[int, int]
PointAlias = tuple[float, float, int,int,int] 

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

    def increment_counter(self)->None:
        self.counter+=1

    def update_color(self,new_red:int, new_green: int, new_blue: int)-> None:
        self.red = (self.red+ new_red)//2
        self.green = (self.green+ new_green)//2
        self.blue = (self.blue+ new_blue)//2



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

    def apply_affine_transformation(self, x:float, y: float)->tuple[float, float]:
        return self.a *x  +self.b *y + self.c, self.d *x +self.e *y + self.f
    

@dataclass
class FractalLimits:
    x_min: float = float('inf')
    x_max: float = -float('inf')
    y_min: float = float('inf')
    y_max: float = -float('inf')

    def update(self,x_cur,y_cur):
        self.x_min = min(self.x_min, x_cur)
        self.x_max = max(self.x_max, x_cur)
        self.y_min = min(self.y_min, y_cur)
        self.y_max = max(self.y_max, y_cur)