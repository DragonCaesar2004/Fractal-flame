import pytest
import random
from src.config import affine_transformations_number, left_bound_of_affine_coeffs, right_bound_of_affine_coeffs
from frozendict import frozendict
from src.affine_transformations import (
    generate_valid_affine_transformation,
    generate_probabilities,
)
from src.project_types import AffineCoefficients

# Фиксируем seed для тестирования случайности
random.seed(1)


@pytest.fixture
def affine_coefficients():
    # Генерация аффинных коэффициентов для будущих тестов
    return [
        generate_valid_affine_transformation()
        for _ in range(affine_transformations_number)
    ]


@pytest.fixture
def affine_probabilities():
    # Генерация вероятностей
    return generate_probabilities(affine_transformations_number)


def test_generate_valid_affine_coefficients():
    """Тест генерации корректных коэффициентов."""
    affine_trans= generate_valid_affine_transformation()

    assert left_bound_of_affine_coeffs <= affine_trans.a <= right_bound_of_affine_coeffs
    assert left_bound_of_affine_coeffs <= affine_trans.b <= right_bound_of_affine_coeffs
    assert left_bound_of_affine_coeffs <= affine_trans.d <= right_bound_of_affine_coeffs
    assert left_bound_of_affine_coeffs <= affine_trans.e <= right_bound_of_affine_coeffs
    assert left_bound_of_affine_coeffs <= affine_trans.c <= right_bound_of_affine_coeffs
    assert left_bound_of_affine_coeffs <= affine_trans.f <= right_bound_of_affine_coeffs

    assert 0<=affine_trans.red<=255
    assert 0<=affine_trans.blue<=255
    assert 0<=affine_trans.green<=255
    # Проверка условий (из вашего алгоритма)
    assert affine_trans.a**2 + affine_trans.d**2 < 1
    assert affine_trans.b**2 + affine_trans.e**2 < 1
    assert affine_trans.a**2 + affine_trans.b**2 + affine_trans.d**2 + affine_trans.e**2 < 1 + (affine_trans.a * affine_trans.e - affine_trans.b * affine_trans.d) ** 2


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


