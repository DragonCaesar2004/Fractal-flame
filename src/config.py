from frozendict import frozendict
from math import sin, cos, atan2, sqrt, pi
from enum import Enum

# минимальные и максимальные значения для длины / ширины изображения
min_width = 100
max_width = 5000
min_height = 100
max_height = 5000

# максимальное число итераций
max_iteration_num = 50_000_000

# кол-во аффинных преобразований, применяемых к точке на каждой итерации
affine_transformations_num = 3

# кол-во стартовых точек
count_start_points = 2

# левая и правая границы для коэфициентов аффиннго преобразования
left_bound_of_affine_coeffs = -1
right_bound_of_affine_coeffs = 1

# количество первых итераций, которые булут пропущены, для того чтобы
# убрать влияние начальной точки.
discarded_iteration_number = 50

# коэфф-т гамма коррекции
gamma_coeff = 3.5

# параметр симметрии
symmetry_axes_count = 1


# словарь вариаций frozendict[name]= function
transformer_functions = frozendict(
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


class FractalLimits(Enum):
    x_min: float = -1.0
    x_max: float = 1.0
    y_min: float = -1.0
    y_max: float = 1.0
