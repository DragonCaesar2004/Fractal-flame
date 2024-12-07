from src.config import FractalLimits
from src.project_types import ImageCoordsAlias


def scale_to_image_coordinates(
    coord_x: float, coord_y: float, img_width: int, img_height: int
) -> ImageCoordsAlias:
    """
    Преобразует координаты в диапазоне (x_min, x_max, y_min, y_max) в пиксельные координаты.
    Масштабируем x и y в размеры изображения (с учётом диапазонов)
    """

    image_x = int(
        (coord_x - FractalLimits.x_min.value)
        / (FractalLimits.x_max.value - FractalLimits.x_min.value)
        * (img_width - 1)
    )
    image_y = int(
        (coord_y - FractalLimits.y_min.value)
        / (FractalLimits.y_max.value - FractalLimits.y_min.value)
        * (img_height - 1)
    )

    return image_x, image_y
