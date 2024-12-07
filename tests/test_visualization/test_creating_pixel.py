from src.core.creating_pixel import create_pixel, combine_pixels
from src.project_types import AffineTransformation,Pixel


def test_create_new_pixel():
    pixels = {}
    affine_transf = AffineTransformation(
        a=0.5, b=0.5, c=0.5, d=0.5, e=0.5, f=0.5, red=10, green=20, blue=30
    )
    image_x, image_y = 100, 200

    create_pixel(pixels, affine_transf, image_x, image_y)

    assert (image_x, image_y) in pixels
    assert pixels[(image_x, image_y)].red == 10
    assert pixels[(image_x, image_y)].green == 20
    assert pixels[(image_x, image_y)].blue == 30
    assert pixels[(image_x, image_y)].counter == 1


def test_create_pixel_existing_pixel():
    pixels = {}
    affine_transf_1 = AffineTransformation(
        a=0.5, b=0.5, c=0.5, d=0.5, e=0.5, f=0.5, red=10, green=20, blue=30
    )
    affine_transf_2 = AffineTransformation(
        a=0.5, b=0.5, c=0.5, d=0.5, e=0.5, f=0.5, red=90, green=80, blue=70
    )
    image_x, image_y = 100, 200

    create_pixel(pixels, affine_transf_1, image_x, image_y)
    create_pixel(pixels, affine_transf_2, image_x, image_y)

    assert (image_x, image_y) in pixels
    assert pixels[(image_x, image_y)].red == 50
    assert pixels[(image_x, image_y)].green == 50
    assert pixels[(image_x, image_y)].blue == 50
    assert pixels[(image_x, image_y)].counter == 2  # Было 1, стало 2



# Вспомогательная функция для проверки пикселей
def pixel_equals(pixel: Pixel, counter: int, red: int, green: int, blue: int) -> bool:
    return (
        pixel.counter == counter
        and pixel.red == red
        and pixel.green == green
        and pixel.blue == blue
    )

def test_combine_pixels():
    # Создаем тестовые данные
    input_data = [
        {
            (0, 0): Pixel(counter=1, red=100, green=150, blue=200),
            (1, 0): Pixel(counter=2, red=50, green=75, blue=250),
        },
        {
            (0, 0): Pixel(counter=2, red=200, green=100, blue=50),
            (1, 1): Pixel(counter=1, red=25, green=50, blue=75),
        },
    ]

    # Ожидаемый результат
    expected_output = {
        (0, 0): Pixel(counter=3, red=150, green=125, blue=125),
        (1, 0): Pixel(counter=2, red=50, green=75, blue=250),
        (1, 1): Pixel(counter=1, red=25, green=50, blue=75),
    }
 
    result = combine_pixels(input_data)

     
    assert len(result) == len(expected_output), "Должно сохраняться количество уникальных координат"

    for coord, pixel in result.items():
        assert coord in expected_output, f"Координата {coord} не найдена в ожидаемом результате"
        expected_pixel = expected_output[coord]
        assert pixel_equals(
            pixel,
            expected_pixel.counter,
            expected_pixel.red,
            expected_pixel.green,
            expected_pixel.blue,
        ), f"Пиксель {coord} не совпадает с ожидаемым значением"

def test_empty_input():
    # Пустой вход
    input_data = []
    result = combine_pixels(input_data)
    assert result == {}, "Результат для пустого входа должен быть пустым словарем"

def test_non_overlapping_pixels():
    # Данные без пересекающихся координат
    input_data = [
        {(0, 0): Pixel(counter=1, red=100, green=150, blue=200)},
        {(1, 1): Pixel(counter=2, red=50, green=75, blue=125)},
    ]

    expected_output = {
        (0, 0): Pixel(counter=1, red=100, green=150, blue=200),
        (1, 1): Pixel(counter=2, red=50, green=75, blue=125),
    }

    result = combine_pixels(input_data)

    assert len(result) == len(expected_output), "Длина результата не совпадает с ожидаемым"
    
    for coord, pixel in result.items():
        assert coord in expected_output, f"Координата {coord} не найдена в ожидаемом результате"
        expected_pixel = expected_output[coord]
        assert pixel_equals(
            pixel,
            expected_pixel.counter,
            expected_pixel.red,
            expected_pixel.green,
            expected_pixel.blue,
        ), f"Пиксель {coord} не совпадает с ожидаемым значением"

