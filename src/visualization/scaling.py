from src.config import FRACTAL_LIMITS
from src.project_types import ImageCoordsAlias


def scale_to_image_coordinates(
    coord_x: float, coord_y: float, img_width: int, img_height: int
) -> ImageCoordsAlias:
    """
    Преобразует координаты в диапазоне (x_min, x_max, y_min, y_max) в пиксельные координаты.
    Масштабируем x и y в размеры изображения (с учётом диапазонов)
    """

    image_x = int(
        (coord_x - FRACTAL_LIMITS.x_min)
        / (FRACTAL_LIMITS.x_max - FRACTAL_LIMITS.x_min)
        * (img_width - 1)
    )
    image_y = int(
        (coord_y - FRACTAL_LIMITS.y_min)
        / (FRACTAL_LIMITS.y_max - FRACTAL_LIMITS.y_min)
        * (img_height - 1)
    )

    return image_x, image_y
