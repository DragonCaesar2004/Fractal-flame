from src.command_line_interface import CommandLineInterface
from src.affine_transformations import  generate_probabilities
from src.config import affine_transformations_number
from src.project_types import UserData

class Manager:

    def __init__(self, user_data: UserData,  cli: CommandLineInterface):
        self.cli = cli
        self.user_data = user_data

    def create_fractal_flame(self, multistream=False):
        pass
        # Генерация коэффициентов для всех преобразований
        # affine_coefficients = [
        #     generate_valid_affine_coefficients() for _ in range(affine_transformations_number)
        # ]

        # # Генерация вероятностей для аффинных преобразований
        # affine_probabilities = generate_probabilities(affine_transformations_number)
