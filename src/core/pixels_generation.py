import random

from src.config import (
    COUNT_START_POINTS,
    DISCARDED_ITERATION_NUMBER,
    FRACTAL_LIMITS,
    SYMMETRY_AXES_COUNT,
)
from src.core.creating_pixel import create_pixel
from src.core.symmetry import apply_symmetry
from src.core.transformations import apply_variations
from src.project_types import ImageCoordsAlias, Pixel, UserData
from src.utils.random_element_selection import select_random_element_with_probabilities
from src.visualization.scaling import scale_to_image_coordinates


def process_single_start_point(
    args: tuple[UserData, list, list]
) -> dict[ImageCoordsAlias, Pixel]:
    """
    Функция-воркер для обработки одной стартовой точки и генерации пикселей.

    Аргументы:
        args: Кортеж, содержащий пользовательские данные, аффинные преобразования и их вероятности.

    Возвращает:
        Словарь пикселей, сгенерированных из этой стартовой точки.
    """
    user_data, affine_transformations, affine_probabilities = args
    pixels: dict[ImageCoordsAlias, Pixel] = {}

    # Инициализируем текущую позицию случайной стартовой точкой
    x_cur = random.uniform(FRACTAL_LIMITS.x_min, FRACTAL_LIMITS.x_max)
    y_cur = random.uniform(FRACTAL_LIMITS.y_min, FRACTAL_LIMITS.y_max)
    result_iter_num = user_data.iterations_number // COUNT_START_POINTS
    for iter_num in range(-DISCARDED_ITERATION_NUMBER, result_iter_num):
        # Выбираем случайное аффинное преобразование на основе вероятностей
        affine_transf = select_random_element_with_probabilities(
            affine_transformations, affine_probabilities
        )
        x_cur, y_cur = affine_transf.apply_affine_transformation(x_cur, y_cur)

        if iter_num > 0:
            # Применяем вариации к преобразованной точке
            x_cur, y_cur = apply_variations(
                user_data.transformer_function_set, x_cur, y_cur
            )
            # Применяем симметрию для генерации множества точек
            points = apply_symmetry(x_cur, y_cur, SYMMETRY_AXES_COUNT)

            for x, y in points:
                # Масштабируем точки в изображаемые координаты
                image_x, image_y = scale_to_image_coordinates(
                    x, y, user_data.img_width_in_pixels, user_data.img_height_in_pixels
                )
                # Создаем или обновляем пиксель в словаре
                create_pixel(pixels, affine_transf, image_x, image_y)

    return pixels
