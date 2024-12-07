from src.project_types import Pixel, ImageCoordsAlias


def gamma_correction(pixels: dict[ImageCoordsAlias, Pixel], gamma_coeff: float) -> None:
    """
    Применяет гамма-коррекцию к пикселям изображения.

    Эта функция обновляет цвета пикселей на основе их нормалей с использованием
    заданного коэффициента гаммы. Нормали нормализуются, и RGB значения
    умножаются на результат гамма-коррекции.
    """
    max_log: float = 0.0
    for pixel in pixels.values():
        pixel.update_normal()
        max_log = max(max_log, pixel.normal)
    # Защита от деления на 0
    if max_log == 0:
        return  # Все нормали - ноль, изменений быть не должно
    for pixel in pixels.values():
        pixel.normal /= max_log
        pixel.red = int(pixel.red * pixel.normal ** (1.0 / gamma_coeff))
        pixel.green = int(pixel.green * pixel.normal ** (1.0 / gamma_coeff))
        pixel.blue = int(pixel.blue * pixel.normal ** (1.0 / gamma_coeff))
