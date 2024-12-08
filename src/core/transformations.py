import random

from src.config import (
    LEFT_BOUND_OF_AFFINE_COEFFS,
    RIGHT_BOUND_OF_AFFINE_COEFFS,
    TRANSFORMER_FUNCTIONS,
)
from src.project_types import AffineTransformation, PointCoordsAlias

"""
Необходимо подобрать такие коэффициенты, чтобы полученное преобразование было сжимающим,
то есть таким, что его коэффициент масштабирования меньше единицы. 
Этих преобразований должно быть несколько, и если выбирать случайным образом одно из них,
чтобы вычислить новые координаты точки и отобразить ее на экране, 
мы получим аттрактор — множество точек, из которых и будет состоять изображение.

x′ = ax + by + c
y′ = dx + ey + f
"""


def generate_valid_affine_transformation() -> AffineTransformation:
    while True:
        a = random.uniform(LEFT_BOUND_OF_AFFINE_COEFFS, RIGHT_BOUND_OF_AFFINE_COEFFS)
        b = random.uniform(LEFT_BOUND_OF_AFFINE_COEFFS, RIGHT_BOUND_OF_AFFINE_COEFFS)
        d = random.uniform(LEFT_BOUND_OF_AFFINE_COEFFS, RIGHT_BOUND_OF_AFFINE_COEFFS)
        e = random.uniform(LEFT_BOUND_OF_AFFINE_COEFFS, RIGHT_BOUND_OF_AFFINE_COEFFS)

        # Проверка указанных условий
        if (
            (a**2 + d**2 < 1)
            and (b**2 + e**2 < 1)
            and (a**2 + b**2 + d**2 + e**2 < 1 + (a * e - b * d) ** 2)
        ):
            # Генерация оставшихся коэффициентов c и f
            c = random.uniform(
                LEFT_BOUND_OF_AFFINE_COEFFS, RIGHT_BOUND_OF_AFFINE_COEFFS
            )
            f = random.uniform(
                LEFT_BOUND_OF_AFFINE_COEFFS, RIGHT_BOUND_OF_AFFINE_COEFFS
            )

            # Генерация яркости каждого цвета в диапозоне от 0 до 255. 8 бит. предствление цвета
            red = random.randint(0, 255)
            green = random.randint(0, 255)
            blue = random.randint(0, 255)
            return AffineTransformation(
                a=a, b=b, c=c, d=d, e=e, f=f, red=red, green=green, blue=blue
            )


# Функция для генерации случайных вероятностей, сумма которых равна 1
def generate_probabilities(n: int) -> list[float]:
    probabilities = [random.random() for _ in range(n)]
    total = sum(probabilities)
    return [p / total for p in probabilities]


def apply_variations(
    transformer_function_set: set[int], x_cur: float, y_cur: float
) -> PointCoordsAlias:
    """
    Применяет набор функций преобразования к заданным координатам.

    Эта функция принимает множество индексов, представляющих функции преобразования,
    применяет эти преобразования к текущим координатам (x_cur, y_cur) и возвращает
    суммарные изменения в координатах x и y.
    """
    x_var, y_var = 0, 0

    for ind, variation in enumerate(TRANSFORMER_FUNCTIONS):
        if ind in transformer_function_set:
            x_v, y_v = TRANSFORMER_FUNCTIONS[variation](x_cur, y_cur)
            x_var += x_v
            y_var += y_v
    return x_var, y_var
