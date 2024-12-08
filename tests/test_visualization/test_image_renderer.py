import pytest
from PIL import Image

from src.project_types import Pixel
from src.visualization.image_renderer import create_fractal_image


@pytest.fixture
def sample_pixels():
    """Пример данных для тестирования."""
    return {
        (0, 0): Pixel(red=255, green=0, blue=0),  # Красный пиксель
        (1, 1): Pixel(red=0, green=255, blue=0),  # Зеленый пиксель
        (2, 2): Pixel(red=0, green=0, blue=255),  # Синий пиксель
    }


@pytest.fixture
def image_size():
    """Размер тестового изображения."""
    return 3, 3


def test_create_fractal_image_creates_file(image_size, sample_pixels, tmp_path):
    """Проверка, что изображение создается и сохраняется."""
    img_width, img_height = image_size
    output_path = tmp_path / "fractal_flame.png"

    create_fractal_image(img_width, img_height, sample_pixels, output_path=output_path)

    # Проверяем, что файл существует
    assert output_path.exists()

    # Проверяем размер изображения
    img = Image.open(output_path)
    assert img.size == (img_width, img_height)


def test_create_fractal_image_pixel_colors(image_size, sample_pixels, tmp_path):
    """Проверка установки правильных цветов пикселей."""
    img_width, img_height = image_size
    output_path = tmp_path / "fractal_flame.png"

    create_fractal_image(img_width, img_height, sample_pixels, output_path=output_path)

    img = Image.open(output_path)

    for coords, pixel in sample_pixels.items():
        assert img.getpixel(coords) == (pixel.red, pixel.green, pixel.blue)


def test_create_fractal_image_ignores_out_of_bounds(
    image_size, sample_pixels, tmp_path
):
    """Проверка, что пиксели за пределами изображения игнорируются."""
    img_width, img_height = image_size
    output_path = tmp_path / "fractal_flame.png"

    # Добавляем пиксель за пределами изображения
    sample_pixels[(5, 5)] = Pixel(red=255, green=255, blue=255)

    create_fractal_image(img_width, img_height, sample_pixels, output_path=output_path)

    img = Image.open(output_path)

    # Проверяем, что пиксель за пределами не был добавлен
    with pytest.raises(IndexError):
        img.getpixel((5, 5))

    # Проверяем, что остальные пиксели корректны
    for coords, pixel in sample_pixels.items():
        if coords[0] < img_width and coords[1] < img_height:
            assert img.getpixel(coords) == (pixel.red, pixel.green, pixel.blue)
