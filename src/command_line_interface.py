from src.user_interface import UserInterface
from src.project_types import UserData
from src.custom_exception import CustomException
from src.config import (
    MIN_HEIGHT,
    MIN_WIDTH,
    MAX_HEIGHT,
    MAX_WIDTH,
    MAX_ITERATION_NUM,
    transformer_functions,
)


class CommandLineInterface(UserInterface):

    def get_user_data(self) -> UserData:
        img_width_in_pixels: int = self._get_size(
            self._get_width_input_message(), MIN_WIDTH, MAX_WIDTH
        )
        img_height_in_pixels: int = self._get_size(
            self._get_height_input_message(), MIN_HEIGHT, MAX_HEIGHT
        )
        iterations_number: int = self._get_iterations_number()
        transformer_function_set: set[int] = self._get_transformer_function_set()

        return UserData(
            img_width_in_pixels=img_width_in_pixels,
            img_height_in_pixels=img_height_in_pixels,
            iterations_number=iterations_number,
            transformer_function_set=transformer_function_set,
        )

    def _get_size(self, side: str, min_size: int, max_size: int) -> int:
        size_message = self._get_size_message(side)
        entered_size_str = input(size_message)

        if len(entered_size_str.split()) != 1:
            raise CustomException(self._get_only_one_arg_message())

        entered_size = self._int_validate(entered_size_str)

        if entered_size < min_size:
            raise CustomException(self._get_less_than_min_message() + str(min_size))

        if entered_size > max_size:
            raise CustomException(self._get_more_than_max_message() + str(max_size))
        return entered_size

    def _get_size_message(self, side) -> str:
        return f"Введите {side} изображения: "

    def _get_only_one_arg_message(self) -> str:
        return "Пожалуйста, введите только один аргумент."

    def _get_not_int_message(self) -> str:
        return "Ввод должен быть целым числом."

    def _get_less_than_min_message(self) -> str:
        return "Размер должен быть больше или равен "

    def _get_more_than_max_message(self) -> str:
        return "Размер должен быть меньше или равен "

    def _get_width_input_message(self) -> str:
        return "Введите ширину изображения."

    def _get_height_input_message(self) -> str:
        return "Введите высоту изображения."

    def _get_iterations_number(self) -> int:
        entered_iterations_number_str = input(self._get_iterations_number_message())
        entered_iterations_number = self._int_validate(entered_iterations_number_str)
        if entered_iterations_number <= 0:
            raise CustomException(self._get_more_than_zero_message())

        if entered_iterations_number > MAX_ITERATION_NUM:
            raise CustomException(self._get_iter_num_more_than_max())

        return entered_iterations_number

    def _get_iterations_number_message(self) -> str:
        return "Введите количество итераций: "

    def _get_more_than_zero_message(self) -> str:
        return "Ввод должен быть положительным числом."

    def _get_iter_num_more_than_max(self) -> str:
        return "Введеное число итераций превышает максимальное значение, программа будет слишком долго работать."

    def _get_transformer_function_set(self) -> set[int]:
        print(self._get_transformer_function_listing())
        entered_set = input(self._get_enter_func_set_message())
        if len(entered_set) == 0:
            raise CustomException(self._get_empty_input_message())

        max_num = len(transformer_functions)
        functions_num_set = set()
        for num_str in entered_set.split():
            num = self._int_validate(num_str)
            if not (1 <= num <= max_num):
                raise CustomException(self._get_not_in_range_message())
            if num in functions_num_set:
                raise CustomException(self._get_duplicate_input())
            functions_num_set.add(num)
        return functions_num_set

    def _get_duplicate_input(self):
        return "Вы ввели повторяющееся значение."

    def _get_not_in_range_message(self):
        return "Вы ввели число не из заданного диапазона."

    def _int_validate(self, number_str: str) -> int:
        try:
            number = int(number_str)
        except Exception as e:
            raise CustomException(self._get_not_int_message()) from e
        return number

    def _get_transformer_function_listing(self) -> str:
        result_message = """Выберите несколько трансфармирующих функций из списка.\n"""

        for ind, function in enumerate(transformer_functions):
            result_message += str(ind) + " " + function + "\n"
        return result_message

    def _get_enter_func_set_message(self) -> str:
        return "Введите только номера через пробел: "

    def _get_empty_input_message(self) -> str:
        return "Введите не пустую строку."
