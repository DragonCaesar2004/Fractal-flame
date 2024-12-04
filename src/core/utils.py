import random
from src.project_types import AffineTransformation

# Выбор элемента на основе вероятностей
def select_random_element_with_probabilities(elements:list[AffineTransformation],probabilities:list[float] )-> AffineTransformation:
    return random.choices(elements, weights=probabilities, k=1)[0]