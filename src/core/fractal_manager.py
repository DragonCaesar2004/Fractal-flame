import random
from multiprocessing import Pool, cpu_count

from src.project_types import UserData, Pixel, ImageCoordsAlias
from src.config import discarded_iteration_number, count_start_points,affine_transformations_num,symmetry_axes_count,gamma_coeff, FractalLimits

from src.core.utils import select_random_element_with_probabilities
from src.core.transformations import generate_valid_affine_transformation,generate_probabilities, apply_variations
from src.core.symmetry import apply_symmetry

from src.visualization.image_renderer import create_fractal_image
from src.visualization.gamma_correction import gamma_correction
from src.visualization.scaling import scale_to_image_coordinates
from src.core.creating_pixel import create_pixel, combine_pixels



def process_single_start_point(args: tuple[UserData, list, list]) -> dict[ImageCoordsAlias, Pixel]:
    """
    Функция-воркер для обработки одной стартовой точки и генерации пикселей.

    Аргументы:
        args: Кортеж, содержащий пользовательские данные, аффинные преобразования и их вероятности.
    
    Возвращает:
        Словарь пикселей, сгенерированных из этой стартовой точки.
    """
    user_data, affine_transformations, affine_probabilities = args
    pixels: dict[ImageCoordsAlias, Pixel] = {}

    # Инициализируем текущую позицию случайной стартовой точкой
    x_cur = random.uniform(FractalLimits.x_min.value, FractalLimits.x_max.value)
    y_cur = random.uniform(FractalLimits.y_min.value, FractalLimits.y_max.value)

    # Выполняем заданное количество итераций
    for iter_num in range(-discarded_iteration_number, user_data.iterations_number):
        # Выбираем случайное аффинное преобразование на основе вероятностей
        affine_transf = select_random_element_with_probabilities(
            affine_transformations, affine_probabilities
        )
        x_cur, y_cur = affine_transf.apply_affine_transformation(x_cur, y_cur)

        if iter_num > 0:
            # Применяем вариации к преобразованной точке
            x_cur, y_cur = apply_variations(
                user_data.transformer_function_set, x_cur, y_cur
            )
            # Применяем симметрию для генерации множества точек
            points = apply_symmetry(x_cur, y_cur, symmetry_axes_count)

            for x, y in points:
                # Масштабируем точки в изображаемые координаты
                image_x, image_y = scale_to_image_coordinates(
                    x, y,
                    user_data.img_width_in_pixels,
                    user_data.img_height_in_pixels
                )
                # Создаем или обновляем пиксель в словаре
                create_pixel(pixels, affine_transf, image_x, image_y)

    return pixels


class Manager:
    def __init__(self, user_data: UserData):
        """
        Инициализация менеджера.
        """
        self.user_data = user_data

        # Генерация всех аффинных трансформаций
        self.affine_transformations = [
            generate_valid_affine_transformation() for _ in range(affine_transformations_num)
        ]
        # Генерация соответствующих вероятностей для трансформаций
        self.affine_probabilities = generate_probabilities(affine_transformations_num)

    def create_fractal_flame(self, multistream: bool = False) -> None:
        """
        Создание фрактального изображения, с возможной параллелизацией процессов.

        Аргументы:
            multistream (bool): Если True, используется многопроцессорность для обработки стартовых точек.
        """
        num_processes = cpu_count() if multistream else 1

        # Подготавливаем аргументы для каждой стартовой точки
        args = [
            (self.user_data, self.affine_transformations, self.affine_probabilities)
            for _ in range(count_start_points)
        ]

        # Создаем пул процессов
        with Pool(processes=num_processes) as pool:
            # Распределяем работу между процессами
            results = pool.map(process_single_start_point, args)
        
        # Объединяем словари пикселей от всех процессов
        combined_pixels = combine_pixels(results)
               

        # Применяем гамма-коррекцию для всех пикселей
        gamma_correction(combined_pixels, gamma_coeff)
        # Генерируем и сохраняем фрактальное изображение
        create_fractal_image(
            self.user_data.img_width_in_pixels,
            self.user_data.img_height_in_pixels,
            combined_pixels
        )
