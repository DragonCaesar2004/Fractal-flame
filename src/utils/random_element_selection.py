import random

from src.project_types import AffineTransformation


def select_random_element_with_probabilities(
    elements: list[AffineTransformation], probabilities: list[float]
) -> AffineTransformation:
    """
    Выбирает случайный элемент из списка на основе заданных вероятностей.

    Эта функция принимает список элементов и соответствующий список вероятностей,
    возвращая один элемент, выбранный с учетом указанных вероятностей.
    """
    return random.choices(elements, weights=probabilities, k=1)[0]
