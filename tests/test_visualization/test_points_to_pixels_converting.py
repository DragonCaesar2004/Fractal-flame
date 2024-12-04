import pytest
from src.project_types import FractalLimits
from src.visualization.points_to_pixels_converting import convert_points_to_pixels

@pytest.fixture
def fractal_limits():
    return FractalLimits(x_min=-2.0, x_max=2.0, y_min=-2.0, y_max=2.0)

@pytest.fixture
def image_dimensions():
    return 800, 600

def test_convert_points_to_pixels_basic(fractal_limits, image_dimensions):
    points = {
        (-2.0, -2.0, 255, 0, 0),  # В нижнем левом углу
        (2.0, 2.0, 0, 255, 0),    # В верхнем правом углу
        (0.0, 0.0, 0, 0, 255),    # В центре
    }
    img_width, img_height = image_dimensions

    result = convert_points_to_pixels(points, img_width, img_height, fractal_limits)

    assert len(result) == 3
    assert result[(0, 0)].red == 255  # Левый нижний угол
    assert result[(799,599)].green == 255  # Правый верхний угол
    assert result[(399, 299)].blue == 255  # Центр


def test_convert_points_to_pixels_update_color(fractal_limits, image_dimensions):
    points = {
        (0.0, 0.0, 100, 100, 100),  # Центр
        (0.0, 0.0, 50, 50, 50),     # Тот же пиксель, добавляем цвет
    }
    img_width, img_height = image_dimensions

    result = convert_points_to_pixels(points, img_width, img_height, fractal_limits)

    assert len(result) == 1
    pixel = result[(399, 299)]
    assert pixel.red == 75
    assert pixel.green == 75
    assert pixel.blue == 75
    assert pixel.counter == 2

def test_convert_points_to_pixels_empty(fractal_limits, image_dimensions):
    points = set()
    img_width, img_height = image_dimensions

    result = convert_points_to_pixels(points, img_width, img_height, fractal_limits)

    assert result == {}

def test_convert_points_to_pixels_edge_case(fractal_limits, image_dimensions):
    points = {
        (2.0, 2.0, 0, 0, 255),    # Крайнее значение
        (-2.0, -2.0, 255, 0, 0),  # Крайнее значение
    }
    img_width, img_height = image_dimensions

    result = convert_points_to_pixels(points, img_width, img_height, fractal_limits)

    assert len(result) == 2
    assert (799, 599) in result
    assert (0, 0) in result
