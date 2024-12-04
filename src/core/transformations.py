import random

from src.config import  left_bound_of_affine_coeffs,right_bound_of_affine_coeffs,transformer_functions
from src.project_types import AffineTransformation

"""
Необходимо подобрать такие коэффициенты, чтобы полученное преобразование было сжимающим,
то есть таким, что его коэффициент масштабирования меньше единицы. 
Этих преобразований должно быть несколько, и если выбирать случайным образом одно из них,
чтобы вычислить новые координаты точки и отобразить ее на экране, 
мы получим аттрактор — множество точек, из которых и будет состоять изображение.

x′ = ax + by + c
y′ = dx + ey + f
"""

 
def generate_valid_affine_transformation() -> AffineTransformation:
    while True:
        
        a = random.uniform(left_bound_of_affine_coeffs, right_bound_of_affine_coeffs)
        b = random.uniform(left_bound_of_affine_coeffs, right_bound_of_affine_coeffs)
        d = random.uniform(left_bound_of_affine_coeffs, right_bound_of_affine_coeffs)
        e = random.uniform(left_bound_of_affine_coeffs, right_bound_of_affine_coeffs)

        # Проверка указанных условий
        if (
            (a**2 + d**2 < 1)
            and (b**2 + e**2 < 1)
            and (a**2 + b**2 + d**2 + e**2 < 1 + (a * e - b * d) ** 2)
        ):
            # Генерация оставшихся коэффициентов c и f
            c = random.uniform(left_bound_of_affine_coeffs, right_bound_of_affine_coeffs)
            f = random.uniform(left_bound_of_affine_coeffs, right_bound_of_affine_coeffs)

            # Генерация яркости каждого цвета в диапозоне от 0 до 255
            red = random.randint(0,255)
            green = random.randint(0,255)
            blue = random.randint(0,255)
            return AffineTransformation(a=a, b=b, c=c, d=d, e=e, f=f, red=red,green=green, blue=blue)


# Функция для генерации случайных вероятностей, сумма которых равна 1
def generate_probabilities(n:int ) -> list[float]:
    probabilities = [random.random() for _ in range(n)]
    total = sum(probabilities)
    return [p / total for p in probabilities]




def apply_variations(transformer_function_set:set[int] ,x_cur: float,y_cur: float)-> tuple[float, float]:
    
    x_var,y_var = 0,0
    
    for ind, variation in enumerate(transformer_functions):
        if ind in transformer_function_set:
            x_v, y_v = transformer_functions[variation](x_cur,y_cur)
            x_var += x_v
            y_var += y_v
    return x_var, y_var