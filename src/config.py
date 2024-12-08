from frozendict import frozendict
from math import sin, cos, atan2, sqrt, pi
from typing import NamedTuple

# минимальные и максимальные значения для длины / ширины изображения
MIN_WIDTH = 100
MAX_WIDTH = 5000
MIN_HEIGHT = 100
MAX_HEIGHT = 5000

# максимальное число итераций
MAX_ITERATION_NUM = 50_000_000

# кол-во аффинных преобразований, применяемых к точке на каждой итерации
AFFINE_TRANSFORMATIONS_NUM = 3

# кол-во стартовых точек
COUNT_START_POINTS = 4

# левая и правая границы для коэфициентов аффиннго преобразования
LEFT_BOUND_OF_AFFINE_COEFFS = -1
RIGHT_BOUND_OF_AFFINE_COEFFS = 1

# количество первых итераций, которые булут пропущены, для того чтобы
# убрать влияние начальной точки.
DISCARDED_ITERATION_NUMBER = 50

# коэфф-т гамма коррекции
GAMMA_COEFF = 2.4

# параметр симметрии
SYMMETRY_AXES_COUNT = 3


# словарь вариаций frozendict[name]= function
TRANSFORMER_FUNCTIONS = frozendict(
    {
        "linear": lambda x, y: (x, y),
        "sinusoidal": lambda x, y: (sin(x), sin(y)),
        "spherical": lambda x, y: (
            x / (x**2 + y**2) if (x**2 + y**2) != 0 else 0,
            y / (x**2 + y**2) if (x**2 + y**2) != 0 else 0,
        ),
        "swirl": lambda x, y: (
            x * sin(x**2 + y**2) - y * cos(x**2 + y**2),
            x * cos(x**2 + y**2) + y * sin(x**2 + y**2),
        ),
        "horseshoe": lambda x, y: (
            (x - y) * (x + y) / sqrt(x**2 + y**2) if sqrt(x**2 + y**2) != 0 else 0,
            2 * x * y / sqrt(x**2 + y**2) if sqrt(x**2 + y**2) != 0 else 0,
        ),
        "polar": lambda x, y: (
            atan2(y, x) / pi,
            sqrt(x**2 + y**2) - 1,
        ),
        "handkerchief": lambda x, y: (
            sqrt(x**2 + y**2) * sin(atan2(y, x) + sqrt(x**2 + y**2)),
            sqrt(x**2 + y**2) * cos(atan2(y, x) - sqrt(x**2 + y**2)),
        ),
        "heart": lambda x, y: (
            sqrt(x**2 + y**2) * sin(atan2(y, x) * sqrt(x**2 + y**2)),
            -sqrt(x**2 + y**2) * cos(atan2(y, x) * sqrt(x**2 + y**2)),
        ),
        "disc": lambda x, y: (
            atan2(y, x) / pi * sin(pi * sqrt(x**2 + y**2)),
            atan2(y, x) / pi * cos(pi * sqrt(x**2 + y**2)),
        ),
        "spiral": lambda x, y: (
            1 / sqrt(x**2 + y**2) * (cos(atan2(y, x) + sqrt(x**2 + y**2))),
            1 / sqrt(x**2 + y**2) * (sin(atan2(y, x) - sqrt(x**2 + y**2))),
        ),
        "hyperbolic": lambda x, y: (
            sin(atan2(y, x)) / sqrt(x**2 + y**2),
            cos(atan2(y, x)) * sqrt(x**2 + y**2),
        ),
        "diamond": lambda x, y: (
            sin(atan2(y, x)) * cos(sqrt(x**2 + y**2)),
            cos(atan2(y, x)) * sin(sqrt(x**2 + y**2)),
        ),
    }
)


class FractalLimits(NamedTuple):
    x_min: float = -1.0
    x_max: float = 1.0
    y_min: float = -1.0
    y_max: float = 1.0


FRACTAL_LIMITS = FractalLimits()

OUTPUT_ADDRESS = "fractal_flame.png"
