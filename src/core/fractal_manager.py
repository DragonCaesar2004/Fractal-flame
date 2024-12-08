from multiprocessing import Pool, cpu_count

from src.project_types import UserData
from src.config import (
    COUNT_START_POINTS,
    AFFINE_TRANSFORMATIONS_NUM,
    GAMMA_COEFF,
    OUTPUT_ADDRESS
)
from src.core.pixels_generation import process_single_start_point
from src.core.creating_pixel import  combine_pixels
from src.core.transformations import (
    generate_valid_affine_transformation,
    generate_probabilities,
    )

from src.visualization.image_renderer import create_fractal_image
from src.visualization.gamma_correction import gamma_correction

from src.timing_decorator import timing_decorator


class Manager:
    """ Класс, отвечающий за создание фрактальных изображений с использованием аффинных трансформаций."""
    def __init__(self, user_data: UserData)->None:
        """Инициализация менеджера."""
        self.user_data = user_data

        # Генерация всех аффинных трансформаций
        self.affine_transformations = [
            generate_valid_affine_transformation()
            for _ in range(AFFINE_TRANSFORMATIONS_NUM)
        ]
        # Генерация соответствующих вероятностей для трансформаций
        self.affine_probabilities = generate_probabilities(AFFINE_TRANSFORMATIONS_NUM)

    @timing_decorator
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
            for _ in range(COUNT_START_POINTS)
        ]

        # Создаем пул процессов
        with Pool(processes=num_processes) as pool:
            # Распределяем работу между процессами
            results = pool.map(process_single_start_point, args)

        # Объединяем словари пикселей от всех процессов
        combined_pixels = combine_pixels(results)

        # Применяем гамма-коррекцию для всех пикселей
        gamma_correction(combined_pixels, GAMMA_COEFF)
        # Генерируем и сохраняем фрактальное изображение
        create_fractal_image(
            self.user_data.img_width_in_pixels,
            self.user_data.img_height_in_pixels,
            combined_pixels, OUTPUT_ADDRESS
        )
