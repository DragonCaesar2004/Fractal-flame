from frozendict import frozendict
from math import sin, cos

MIN_WIDTH = 376
MAX_WIDTH = 2000

MIN_HEIGHT = 256
MAX_HEIGHT = 2000

MAX_ITERATION_NUM = 10_000_000

transformer_functions = frozendict(
    {
        "linear": lambda x, y: (x, y),
        "sinusoidal": lambda x, y: (sin(x), sin(y)),
        "spherical": lambda x, y: (x / (x**2 + y**2), y / (x**2 + y**2)),
        "swirl": lambda x, y: (
            x * sin(x**2 + y**2) - y * cos(x**2 + y**2),
            x * cos(x**2 + y**2) + y * sin(x**2 + y**2),
        ),
        "horseshoe": lambda x, y: (
            (x - y) * (x + y) / (x**2 + y**2)**0.5,
            2 * x * y / (x**2 + y**2)**0.5,
        ),
    }
)

affine_transformations_number = 3

start_point = (0, 0)  # x,y


left_bound_of_affine_coeffs = -1
right_bound_of_affine_coeffs = 1

# количество первых итераций, которые булут пропущены, для того чтобы 
# убрать влияние начальной точки.
discarded_iterations = 50