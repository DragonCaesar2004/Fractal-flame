import math
from src.core.symmetry import apply_symmetry


def test_point_on_single_axis():
    """Тестируем точку на четной оси симметрии."""
    result = apply_symmetry(1.0, 0.0, 4)
    expected_result = [(1.0, 0.0), (0.0, 1.0), (-1.0, 0.0), (0.0, -1.0)]

    # Округляем координаты результата до 5 знаков для корректного сравнения.
    result_rounded = [(round(x, 5), round(y, 5)) for x, y in result]
    expected_result_rounded = [(round(x, 5), round(y, 5)) for x, y in expected_result]

    assert result_rounded == expected_result_rounded


def test_general_point():
    """Тестируем точку в общем случае."""
    x, y = math.sqrt(2) / 2, math.sqrt(2) / 2
    result = apply_symmetry(x, y, 4)
    expected_result = [(x, y), (-y, x), (-x, -y), (y, -x)]

    result_rounded = [(round(x, 5), round(y, 5)) for x, y in result]
    expected_result_rounded = [(round(x, 5), round(y, 5)) for x, y in expected_result]

    print("Result:", result_rounded)
    assert result_rounded == expected_result_rounded


def test_custom_symmetry_axes_count():
    """Тестируем с изменением количества осей симметрии."""

    symmetry_axes_count = 6  # Устанавливаем 6 осей симметрии
    result = apply_symmetry(1, 1, symmetry_axes_count)
    assert len(result) == symmetry_axes_count


def test_negative_coordinates():
    """Тестируем, что функция корректно работает с отрицательными координатами."""
    result = apply_symmetry(-1, -1, 4)
    expected_result = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
    assert [(round(x, 5), round(y, 5)) for x, y in result] == expected_result
