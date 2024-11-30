import random
from frozendict import frozendict

from src.config import affine_transformations_number
from src.project_types import AffineCoefficients 
'''
Необходимо подобрать такие коэффициенты, чтобы полученное преобразование было сжимающим,
то есть таким, что его коэффициент масштабирования меньше единицы. 
Этих преобразований должно быть несколько, и если выбирать случайным образом одно из них,
чтобы вычислить новые координаты точки и отобразить ее на экране, 
мы получим аттрактор — множество точек, из которых и будет состоять изображение.

x′ = ax + by + c
y′ = dx + ey + f
'''
def generate_valid_affine_coefficients()-> AffineCoefficients:
    while True:
        # Генерация коэффициентов a, b, d, e на отрезке [-1, 1]
        a = random.uniform(-1, 1)
        b = random.uniform(-1, 1)
        d = random.uniform(-1, 1)
        e = random.uniform(-1, 1)
        
        # Проверка указанных условий
        if (a**2 + d**2 < 1) and (b**2 + e**2 < 1) and (a**2 + b**2 + d**2 + e**2 < 1 + (a*e - b*d)**2):
            # Генерация оставшихся коэффициентов c и f
            c = random.uniform(-1, 1)
            f = random.uniform(-1, 1)
            return (a, b, c, d, e, f)
        
# Функция для генерации случайных вероятностей, сумма которых равна 1
def generate_probabilities(n)->list[float]:
    probabilities = [random.random() for _ in range(n)]
    total = sum(probabilities)
    return [p / total for p in probabilities]

# Генерация коэффициентов для всех преобразований
affine_coefficients = [generate_valid_affine_coefficients() for _ in range(affine_transformations_number)]

# Генерация вероятностей для аффинных преобразований
affine_probabilities = generate_probabilities(affine_transformations_number)

# Создание словаря, где коэффициенты — ключи, а вероятности — значения
affine_conversion_coefficients = frozendict(
    {coefficients: probability for coefficients, probability in zip(affine_coefficients, affine_probabilities)}
)
