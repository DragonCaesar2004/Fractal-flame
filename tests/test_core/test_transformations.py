import pytest
import random
from src.config import (
    AFFINE_TRANSFORMATIONS_NUM,
    LEFT_BOUND_OF_AFFINE_COEFFS,
    RIGHT_BOUND_OF_AFFINE_COEFFS,
)
from src.core.transformations import (
    generate_valid_affine_transformation,
    generate_probabilities,
    apply_variations,
)
from math import sin, cos, sqrt, atan2, pi

# Фиксируем seed для тестирования случайности
random.seed(1)


@pytest.fixture
def affine_coefficients():
    # Генерация аффинных коэффициентов для будущих тестов
    return [
        generate_valid_affine_transformation()
        for _ in range(AFFINE_TRANSFORMATIONS_NUM)
    ]


@pytest.fixture
def affine_probabilities():
    # Генерация вероятностей
    return generate_probabilities(AFFINE_TRANSFORMATIONS_NUM)


def test_generate_valid_affine_coefficients():
    """Тест генерации корректных коэффициентов."""
    affine_trans = generate_valid_affine_transformation()

    assert LEFT_BOUND_OF_AFFINE_COEFFS <= affine_trans.a <= RIGHT_BOUND_OF_AFFINE_COEFFS
    assert LEFT_BOUND_OF_AFFINE_COEFFS <= affine_trans.b <= RIGHT_BOUND_OF_AFFINE_COEFFS
    assert LEFT_BOUND_OF_AFFINE_COEFFS <= affine_trans.d <= RIGHT_BOUND_OF_AFFINE_COEFFS
    assert LEFT_BOUND_OF_AFFINE_COEFFS <= affine_trans.e <= RIGHT_BOUND_OF_AFFINE_COEFFS
    assert LEFT_BOUND_OF_AFFINE_COEFFS <= affine_trans.c <= RIGHT_BOUND_OF_AFFINE_COEFFS
    assert LEFT_BOUND_OF_AFFINE_COEFFS <= affine_trans.f <= RIGHT_BOUND_OF_AFFINE_COEFFS

    assert 0 <= affine_trans.red <= 255
    assert 0 <= affine_trans.blue <= 255
    assert 0 <= affine_trans.green <= 255
    # Проверка условий (из вашего алгоритма)
    assert affine_trans.a**2 + affine_trans.d**2 < 1
    assert affine_trans.b**2 + affine_trans.e**2 < 1
    assert (
        affine_trans.a**2 + affine_trans.b**2 + affine_trans.d**2 + affine_trans.e**2
        < 1 + (affine_trans.a * affine_trans.e - affine_trans.b * affine_trans.d) ** 2
    )


def test_generate_probabilities():
    """Тест корректности генерации вероятностей."""
    n = 5
    probabilities = generate_probabilities(n)

    # Проверка длины списка
    assert len(probabilities) == n, f"Длина списка вероятностей должна быть {n}."

    # Проверка, что все вероятности больше 0 и меньше 1
    assert all(
        0 <= p <= 1 for p in probabilities
    ), "Все вероятности должны быть в диапазоне [0, 1]."

    # Проверка, что сумма вероятностей равна 1
    assert (
        abs(sum(probabilities) - 1) < 1e-9
    ), "Сумма всех вероятностей должна быть равна 1."


def test_apply_variations_linear_function():
    # Проверка применения одного преобразования
    transformer_function_set = {0}  # Включаем только mock_transform_1
    x_cur, y_cur = 1, 1
    x_var, y_var = apply_variations(transformer_function_set, x_cur, y_cur)
    assert (x_var, y_var) == (1, 1)


def test_apply_variations_multiple_functions():
    # Проверка применения нескольких преобразований
    transformer_function_set = {0, 1}  # Включаем mock_transform_1 и mock_transform_2
    x_cur, y_cur = 1, 1
    x_var, y_var = apply_variations(transformer_function_set, x_cur, y_cur)
    assert (x_var, y_var) == (1 + sin(1), 1 + sin(1))


def test_apply_variations_no_functions():
    # Проверка работы с пустым набором функций
    transformer_function_set: set[int] = set()  # Никакие функции не применяются
    x_cur, y_cur = 1, 1
    x_var, y_var = apply_variations(transformer_function_set, x_cur, y_cur)
    assert (x_var, y_var) == (0, 0)  # Без трансформаций результат должен быть (0, 0)


def test_apply_variations_sinusoidal_function():
    transformer_function_set = {1}
    x_cur, y_cur = 1, -1
    x_var, y_var = apply_variations(transformer_function_set, x_cur, y_cur)
    assert (x_var, y_var) == (sin(x_cur), sin(y_cur))


def test_apply_variations_spherical_function():
    transformer_function_set = {2}
    x_cur, y_cur = 1, -1
    x_var, y_var = apply_variations(transformer_function_set, x_cur, y_cur)
    assert (x_var, y_var) == (
        x_cur / (x_cur**2 + y_cur**2),
        y_cur / (x_cur**2 + y_cur**2),
    )


def test_apply_variations_swirl_function():
    transformer_function_set = {3}
    x_cur, y_cur = 2, -2
    x_var, y_var = apply_variations(transformer_function_set, x_cur, y_cur)
    assert (x_var, y_var) == (
        x_cur * sin(x_cur**2 + y_cur**2) - y_cur * cos(x_cur**2 + y_cur**2),
        x_cur * cos(x_cur**2 + y_cur**2) + y_cur * sin(x_cur**2 + y_cur**2),
    )


def test_apply_variations_horseshoe_function():
    transformer_function_set = {4}
    x_cur, y_cur = 2, -2
    x_var, y_var = apply_variations(transformer_function_set, x_cur, y_cur)
    assert (x_var, y_var) == (
        (x_cur - y_cur) * (x_cur + y_cur) / (x_cur**2 + y_cur**2) ** 0.5,
        2 * x_cur * y_cur / (x_cur**2 + y_cur**2) ** 0.5,
    )


def test_apply_variations_polar_function():
    transformer_function_set = {5}
    x_cur, y_cur = 3, 4
    x_var, y_var = apply_variations(transformer_function_set, x_cur, y_cur)
    assert (x_var, y_var) == (
        atan2(y_cur, x_cur) / pi,
        sqrt(x_cur**2 + y_cur**2) - 1,
    )

def test_apply_variations_handkerchief_function():
    transformer_function_set = {6}
    x_cur, y_cur = 3, 4
    x_var, y_var = apply_variations(transformer_function_set, x_cur, y_cur)
    assert (x_var, y_var) == (
        sqrt(x_cur**2 + y_cur**2) * sin(atan2(y_cur, x_cur) + sqrt(x_cur**2 + y_cur**2)),
        sqrt(x_cur**2 + y_cur**2) * cos(atan2(y_cur, x_cur) - sqrt(x_cur**2 + y_cur**2)),
    )

def test_apply_variations_heart_function():
    transformer_function_set = {7}
    x_cur, y_cur = -3, 4
    x_var, y_var = apply_variations(transformer_function_set, x_cur, y_cur)
    assert (x_var, y_var) == (
        sqrt(x_cur**2 + y_cur**2) * sin(atan2(y_cur, x_cur) * sqrt(x_cur**2 + y_cur**2)),
        -sqrt(x_cur**2 + y_cur**2) * cos(atan2(y_cur, x_cur) * sqrt(x_cur**2 + y_cur**2)),
    )

def test_apply_variations_disc_function():
    transformer_function_set = {8}
    x_cur, y_cur = -3, 4
    x_var, y_var = apply_variations(transformer_function_set, x_cur, y_cur)
    assert (x_var, y_var) == (
        atan2(y_cur, x_cur) / pi * sin(pi * sqrt(x_cur**2 + y_cur**2)),
        atan2(y_cur, x_cur) / pi * cos(pi * sqrt(x_cur**2 + y_cur**2)),
    )

def test_apply_variations_spiral_function():
    transformer_function_set = {9}
    x_cur, y_cur = 1, 2
    x_var, y_var = apply_variations(transformer_function_set, x_cur, y_cur)
    norm = sqrt(x_cur**2 + y_cur**2)
    assert (x_var, y_var) == (
        1 / norm * (cos(atan2(y_cur, x_cur) + norm)),
        1 / norm * (sin(atan2(y_cur, x_cur) - norm)),
    )

def test_apply_variations_hyperbolic_function():
    transformer_function_set = {10}
    x_cur, y_cur = 2, 1
    x_var, y_var = apply_variations(transformer_function_set, x_cur, y_cur)
    norm = sqrt(x_cur**2 + y_cur**2)
    assert (x_var, y_var) == (
        sin(atan2(y_cur, x_cur)) / norm,
        cos(atan2(y_cur, x_cur)) * norm,
    )

def test_apply_variations_diamond_function():
    transformer_function_set = {11}
    x_cur, y_cur = 4, -3
    x_var, y_var = apply_variations(transformer_function_set, x_cur, y_cur)
    norm = sqrt(x_cur**2 + y_cur**2)
    assert (x_var, y_var) == (
        sin(atan2(y_cur, x_cur)) * cos(norm),
        cos(atan2(y_cur, x_cur)) * sin(norm),
    )