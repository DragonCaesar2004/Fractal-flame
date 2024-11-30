from frozendict import frozendict

MIN_WIDTH = 376
MAX_WIDTH = 2000

MIN_HEIGHT = 256
MAX_HEIGHT = 2000

MAX_ITERATION_NUM = 10_000_000

transformer_functions = frozendict(
    {
        1: "linear",
        2: "sinusoidal",
        3: "spherical",
        4: "swirl",
        5: "horseshoe",
    }
)
