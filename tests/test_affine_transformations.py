import pytest
import random
from src.config import affine_transformations_number
from frozendict import frozendict
from src.affine_transformations import generate_valid_affine_coefficients, generate_probabilities
from src.project_types import AffineCoefficients 

# Фиксируем seed для тестирования случайности
random.seed(1)


@pytest.fixture
def affine_coefficients():
    # Генерация аффинных коэффициентов для будущих тестов
    return [generate_valid_affine_coefficients() for _ in range(affine_transformations_number)]


@pytest.fixture
def affine_probabilities():
    # Генерация вероятностей
    return generate_probabilities(affine_transformations_number)


def test_generate_valid_affine_coefficients():
    """Тест генерации корректных коэффициентов."""
    coefficients = generate_valid_affine_coefficients()
    assert len(coefficients) == 6, "Коэффициенты должны состоять из шести элементов."
    
    a, b, c, d, e, f = coefficients  # Распаковываем для проверки
    assert -1 <= a <= 1, "Коэффициент 'a' должен лежать в диапазоне [-1, 1]."
    assert -1 <= b <= 1, "Коэффициент 'b' должен лежать в диапазоне [-1, 1]."
    assert -1 <= d <= 1, "Коэффициент 'd' должен лежать в диапазоне [-1, 1]."
    assert -1 <= e <= 1, "Коэффициент 'e' должен лежать в диапазоне [-1, 1]."
    assert -1 <= c <= 1, "Коэффициент 'c' должен лежать в диапазоне [-1, 1]."
    assert -1 <= f <= 1, "Коэффициент 'f' должен лежать в диапазоне [-1, 1]."
    
    # Проверка условий (из вашего алгоритма)
    assert a**2 + d**2 < 1
    assert b**2 + e**2 < 1
    assert a**2 + b**2 + d**2 + e**2 < 1 + (a * e - b * d)**2


def test_generate_probabilities():
    """Тест корректности генерации вероятностей."""
    n = 5
    probabilities = generate_probabilities(n)
    
    # Проверка длины списка
    assert len(probabilities) == n, f"Длина списка вероятностей должна быть {n}."
    
    # Проверка, что все вероятности больше 0 и меньше 1
    assert all(0 <= p <= 1 for p in probabilities), "Все вероятности должны быть в диапазоне [0, 1]."
    
    # Проверка, что сумма вероятностей равна 1
    assert abs(sum(probabilities) - 1) < 1e-9, "Сумма всех вероятностей должна быть равна 1."


def test_affine_conversion_coefficients(affine_coefficients:list[AffineCoefficients], affine_probabilities:list[float]):
    """Тест создания словаря коэффициентов и вероятностей."""
    # Создаем словарь
    affine_conversion_coefficients = frozendict({
        tuple(coefficients): probability
        for coefficients, probability in zip(affine_coefficients, affine_probabilities)
    })
    
    # Проверка длины словаря
    assert len(affine_conversion_coefficients) == len(affine_coefficients), (
        "Длина словаря должна совпадать с количеством коэффициентов."
    )
    
    # Проверка, что ключи в словаре являются кортежами (неизменяемыми)
    for key in affine_conversion_coefficients.keys():
        assert isinstance(key, tuple), "Ключи словаря должны быть кортежами."
        
    # Проверка, что значения ключей совпадают с вероятностями и их сумма равна 1
    assert abs(sum(affine_conversion_coefficients.values()) - 1) < 1e-9, "Сумма всех значений вероятностей должна быть равна 1."
