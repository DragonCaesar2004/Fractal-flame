import pytest
from typing import NamedTuple
from src.visualization.scaling import scale_to_image_coordinates


@pytest.fixture(scope="session")
def FRACTAL_LIMITS():
    """Фикстура для границ фрактала."""

    class FractalLimits(NamedTuple):
        x_min: float = -2.0
        x_max: float = 2.0
        y_min: float = -2.0
        y_max: float = 2.0

    return FractalLimits()


def test_scale_to_image_coordinates_center():
    """Тест центра изображения."""
    coord_x, coord_y = 0.0, 0.0
    img_width, img_height = 100, 100

    result = scale_to_image_coordinates(coord_x, coord_y, img_width, img_height)
    expected = (49, 49)  # Центр изображения
    assert result == expected


def test_scale_to_image_coordinates_bottom_left():
    """Тест левого нижнего угла."""
    coord_x, coord_y = -1.0, -1.0
    img_width, img_height = 0, 0

    result = scale_to_image_coordinates(coord_x, coord_y, img_width, img_height)
    expected = (0, 0)  # Левый нижний угол
    assert result == expected


def test_scale_to_image_coordinates_top_right():
    """Тест верхнего правого угла."""
    coord_x, coord_y = 1.0, 1.0
    img_width, img_height = 100, 100

    result = scale_to_image_coordinates(coord_x, coord_y, img_width, img_height)
    expected = (99, 99)  # Правый верхний угол
    assert result == expected


def test_scale_to_image_coordinates_out_of_bounds():
    """Проверка координат за пределами диапазона границ."""
    coord_x, coord_y = 3.0, 3.0
    img_width, img_height = 100, 100

    result = scale_to_image_coordinates(coord_x, coord_y, img_width, img_height)
    expected = (198, 198)  # Проверяем, что значения корректно вылезают за пределы
    assert result == expected


def test_scale_to_image_coordinates_edge_case():
    """Тест граничного случая."""
    coord_x, coord_y = -1.0, 1.0
    img_width, img_height = 100, 100

    result = scale_to_image_coordinates(coord_x, coord_y, img_width, img_height)
    expected = (0, 99)  # Проверяем, что с половинными значениями всё корректно
    assert result == expected
