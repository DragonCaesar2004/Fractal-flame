from typing import NamedTuple


class UserData(NamedTuple):
    img_width_in_pixels: int
    img_height_in_pixels: int
    iterations_number: int
    transformer_function_set: set[int]
