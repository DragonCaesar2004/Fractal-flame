import pytest
from src.project_types import Pixel
from src.visualization.gamma_correction import gamma_correction


# Фикстура для создания примера с тестовыми пикселями
@pytest.fixture
def sample_pixels():
    return {
        (0, 0): Pixel(100, 150, 200, 0),
        (1, 1): Pixel(50, 75, 100, 0),
        (2, 2): Pixel(25, 50, 75, 0),
    }


@pytest.fixture
def gamma_coeff():
    return 2.2


# Тест нормализации нормаль
def test_normalization(sample_pixels, gamma_coeff):
    # Выполняем gamma_correction
    gamma_correction(sample_pixels, gamma_coeff)

    normals = [pixel.normal for pixel in sample_pixels.values()]
    max_normal = max(normals)

    # Все нормали после нормализации должны быть <= 1
    assert all(0.0 <= normal <= 1.0 for normal in normals)
    # Максимальная нормаль должна быть равна 1
    assert pytest.approx(max_normal, rel=1e-5) == 1.0


# Тест преобразования цветов
def test_color_correction(sample_pixels, gamma_coeff):
    gamma_correction(sample_pixels, gamma_coeff)
    for coord, pixel in sample_pixels.items():
        original_red = pixel.red
        original_green = pixel.green
        original_blue = pixel.blue

        normalized_normal = pixel.normal

        expected_red = int(original_red * (normalized_normal ** (1.0 / gamma_coeff)))
        expected_green = int(
            original_green * (normalized_normal ** (1.0 / gamma_coeff))
        )
        expected_blue = int(original_blue * (normalized_normal ** (1.0 / gamma_coeff)))

        assert pixel.red == expected_red
        assert pixel.green == expected_green
        assert pixel.blue == expected_blue


# Тест работы функции при пустом вводе
def test_empty_pixels():
    pixels = {}
    gamma_correction(pixels, gamma_coeff=2.2)  # Без ошибок
    assert len(pixels) == 0  # Пустой ввод = пустой результат


# Тест работы при нуле в нормали
def test_zero_normal():
    pixels = {
        (0, 0): Pixel(0, 0, 0, 0),
    }
    gamma_correction(pixels, gamma_coeff=2.2)

    pixel = pixels[(0, 0)]

    # Должно обработать пиксель с нормалью 0, без деления на 0
    assert pixel.normal == 1
    assert pixel.red == 0
    assert pixel.green == 0
    assert pixel.blue == 0


# Тест на большие значения gamma_coeff
@pytest.mark.parametrize("gamma_coeff", [0.1, 1.0, 2.2, 10.0])
def test_gamma_coeff_range(sample_pixels, gamma_coeff):
    gamma_correction(sample_pixels, gamma_coeff)

    for pixel in sample_pixels.values():
        # Проверка: цвета остаются корректными (в диапазоне 0-255)
        assert 0 <= pixel.red <= 255
        assert 0 <= pixel.green <= 255
        assert 0 <= pixel.blue <= 255
