from dataclasses import dataclass
from math import log10
from typing import NamedTuple

ImageCoordsAlias = tuple[int, int]
PointCoordsAlias = tuple[float, float]


class UserData(NamedTuple):
    """
    Класс для хранения пользовательских данных для обработки изображений.

    Атрибуты:
        img_width_in_pixels: Ширина изображения в пикселях.
        img_height_in_pixels: Высота изображения в пикселях.
        iterations_number: Число итераций, которые нужно выполнить в процессе обработки.
        transformer_function_set: Множество функций преобразования, представленных целыми числами.
    """

    img_width_in_pixels: int
    img_height_in_pixels: int
    iterations_number: int
    transformer_function_set: set[int]


@dataclass
class Pixel:
    """
    Класс для представления пикселя в изображении с цветами RGB.

    Атрибуты:
        red: Красный компонент пикселя.
        green: Зеленый компонент пикселя.
        blue: Синий компонент пикселя.
        counter: Счетчик для отслеживания обновлений этого пикселя.
        normal: Число с плавающей запятой, представляющее нормализованное значение на основе счетчика.
    """

    red: int = 0
    green: int = 0
    blue: int = 0
    counter: int = 0
    normal: float = 1.0

    def increment_counter(self) -> None:
        """
        Увеличить счетчик пикселя на один.

        Этот метод используется для отслеживания того, сколько раз пиксель был обновлён.
        """
        self.counter += 1

    def update_color(self, new_red: int, new_green: int, new_blue: int) -> None:
        """
        Обновить цвет пикселя, усреднив текущий цвет с новым цветом.

        Аргументы:
            new_red: Новое значение красного цвета.
            new_green: Новое значение зеленого цвета.
            new_blue: Новое значение синего цвета.
        """
        self.red = (self.red + new_red) // 2
        self.green = (self.green + new_green) // 2
        self.blue = (self.blue + new_blue) // 2

    def update_normal(self) -> None:
        """
        Обновить нормализованное значение пикселя на основе счетчика.

        Нормализованное значение вычисляется с использованием логарифма (по основанию 10) от счетчика.
        Если счетчик равен нулю, нормализованное значение остается без изменений.
        """
        if self.counter:
            self.normal = log10(self.counter)


@dataclass(frozen=True)
class AffineTransformation:
    """
    Класс для представления аффинного преобразования в 2D пространстве.

    Атрибуты:
        a: Коэффициент для оси x в преобразовании.
        b: Коэффициент для оси y в преобразовании.
        c: Сдвиг вдоль оси x.
        d: Коэффициент для оси x во втором преобразовании.
        e: Коэффициент для оси y во втором преобразовании.
        f: Сдвиг вдоль оси y.
        red: Красный цветовой компонент, связанный с преобразованием.
        green: Зеленый цветовой компонент, связанный с преобразованием.
        blue: Синий цветовой компонент, связанный с преобразованием.
    """

    a: float
    b: float
    c: float
    d: float
    e: float
    f: float

    red: int
    green: int
    blue: int

    def apply_affine_transformation(self, x: float, y: float) -> tuple[float, float]:
        """
        Применить аффинное преобразование к точке в 2D пространстве.

        Аргументы:
            x: Координата x точки.
            y: Координата y точки.

        Возвращает:
            Кортеж, содержащий преобразованные координаты x и y в результате аффинного преобразования.
        """
        return self.a * x + self.b * y + self.c, self.d * x + self.e * y + self.f
