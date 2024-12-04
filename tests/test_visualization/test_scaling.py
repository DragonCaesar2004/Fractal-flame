import pytest

from src.visualization.scaling import scale_to_image_coordinates


@pytest.fixture(scope='session')
def fractal_limits():
    """Фикстура для границ фрактала."""
    class FractalLimits:
        x_min = -2.0
        x_max = 2.0
        y_min = -2.0
        y_max = 2.0
    
    return FractalLimits()

def test_scale_to_image_coordinates_center(fractal_limits):
    """Тест центра изображения."""
    coord_x, coord_y = 0.0, 0.0
    img_width, img_height = 100, 100

    result = scale_to_image_coordinates(coord_x, coord_y, img_width, img_height, fractal_limits)
    expected = (49, 49)  # Центр изображения
    assert result == expected

def test_scale_to_image_coordinates_bottom_left(fractal_limits):
    """Тест левого нижнего угла."""
    coord_x, coord_y = -2.0, -2.0
    img_width, img_height = 100, 100

    result = scale_to_image_coordinates(coord_x, coord_y, img_width, img_height, fractal_limits)
    expected = (0, 0)  # Левый нижний угол
    assert result == expected

def test_scale_to_image_coordinates_top_right(fractal_limits):
    """Тест верхнего правого угла."""
    coord_x, coord_y = 2.0, 2.0
    img_width, img_height = 100, 100

    result = scale_to_image_coordinates(coord_x, coord_y, img_width, img_height, fractal_limits)
    expected = (99, 99)  # Правый верхний угол
    assert result == expected

def test_scale_to_image_coordinates_out_of_bounds(fractal_limits):
    """Проверка координат за пределами диапазона границ."""
    coord_x, coord_y = 3.0, 3.0
    img_width, img_height = 100, 100

    result = scale_to_image_coordinates(coord_x, coord_y, img_width, img_height, fractal_limits)
    expected = (123, 123)  # Проверяем, что значения корректно вылезают за пределы
    assert result == expected

def test_scale_to_image_coordinates_edge_case(fractal_limits):
    """Тест граничного случая."""
    coord_x, coord_y = -1.0, 1.0
    img_width, img_height = 100, 100

    result = scale_to_image_coordinates(coord_x, coord_y, img_width, img_height, fractal_limits)
    expected = (24, 74)  # Проверяем, что с половинными значениями всё корректно
    assert result == expected
