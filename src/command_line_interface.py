from src.config import (
    MAX_HEIGHT,
    MAX_ITERATION_NUM,
    MAX_WIDTH,
    MIN_HEIGHT,
    MIN_WIDTH,
    TRANSFORMER_FUNCTIONS,
)
from src.custom_exception import CustomError
from src.project_types import UserData
from src.user_interface import UserInterface


class CommandLineInterface(UserInterface):
    """
    Командный интерфейс пользователя для ввода данных.

    Этот класс отвечает за взаимодействие с пользователем через
    консольный интерфейс для получения необходимых данных.
    """

    def get_user_data(self) -> UserData:
        """
        Получает данные пользователя.

        Запрашивает у пользователя ширину и высоту изображения,
        количество итераций и набор функций преобразования,
        выполняет валидацию введенных данных и возвращает объект
        UserData с полученными значениями.
        """
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
        """
        Запрашивает размер у пользователя и выполняет его валидацию.

        Принимает название стороны (ширина или высота), минимальный
        и максимальный размер, запрашивает у пользователя ввод и
        проверяет, что введенное значение соответствует условиям.
        В случае ошибки генерирует CustomError с соответствующим
        сообщением.
        """
        size_message = self._get_size_message(side)
        entered_size_str = input(size_message)

        if len(entered_size_str.split()) != 1:
            raise CustomError(self._get_only_one_arg_message())

        entered_size = self._int_validate(entered_size_str)

        if entered_size < min_size:
            raise CustomError(self._get_less_than_min_message() + str(min_size))

        if entered_size > max_size:
            raise CustomError(self._get_more_than_max_message() + str(max_size))
        return entered_size

    def _get_size_message(self, side: str) -> str:
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
        """
        Запрашивает у пользователя количество итераций и выполняет его валидацию.

        Пользователь вводит число итераций, которое проверяется на
        соответствие условиям: должно быть больше нуля и не превышать
        максимальное разрешенное количество итераций. В случае ошибки
        генерируется CustomError с соответствующим сообщением.
        """
        entered_iterations_number_str = input(self._get_iterations_number_message())
        entered_iterations_number = self._int_validate(entered_iterations_number_str)
        if entered_iterations_number <= 0:
            raise CustomError(self._get_more_than_zero_message())

        if entered_iterations_number > MAX_ITERATION_NUM:
            raise CustomError(self._get_iter_num_more_than_max())

        return entered_iterations_number

    def _get_iterations_number_message(self) -> str:
        return "Введите количество итераций: "

    def _get_more_than_zero_message(self) -> str:
        return "Ввод должен быть положительным числом."

    def _get_iter_num_more_than_max(self) -> str:
        return "Введеное число итераций превышает максимальное значение, программа будет слишком долго работать."

    def _get_transformer_function_set(self) -> set[int]:
        """
        Запрашивает у пользователя набор функций преобразования и выполняет его валидацию.

        Пользователь получает список доступных функций преобразования и
        должен ввести их номера через пробел. Введенные данные проверяются на
        наличие ошибок: не должно быть пустого ввода, номера должны
        находиться в допустимом диапазоне и не должно быть дубликатов.
        В случае ошибок генерируются CustomError с соответствующими
        сообщениями.
        """
        print(self._get_transformer_function_listing())
        entered_list = input(self._get_enter_func_set_message()).split()
        if len(entered_list) == 0:
            raise CustomError(self._get_empty_input_message())

        max_num = len(TRANSFORMER_FUNCTIONS)
        functions_num_set = set()
        for num_str in entered_list:
            num = self._int_validate(num_str)
            if not (0 <= num <= max_num):
                raise CustomError(self._get_not_in_range_message())
            if num in functions_num_set:
                raise CustomError(self._get_duplicate_input())
            functions_num_set.add(num)
        return functions_num_set

    def _get_duplicate_input(self) -> str:
        return "Вы ввели повторяющееся значение."

    def _get_not_in_range_message(self) -> str:
        return "Вы ввели число не из заданного диапазона."

    def _int_validate(self, number_str: str) -> int:
        """
        Валидирует строку, преобразуя её в целое число.

        Этот метод пытается преобразовать переданную строку в целое число.
        Если преобразование не удается, генерируется CustomError
        с соответствующим сообщением.

        """
        try:
            number = int(number_str)
        except Exception as e:
            raise CustomError(self._get_not_int_message()) from e
        return number

    def _get_transformer_function_listing(self) -> str:
        """
        Формирует и возвращает строку со списком доступных функций преобразования.

        Этот метод создает строку, в которой перечислены индексы
        и названия всех доступных функций преобразования.
        Каждая функция отображается с её индексом для удобства выбора.
        """
        result_message = """Выберите несколько трансфармирующих функций из списка.\n"""

        for ind, function in enumerate(TRANSFORMER_FUNCTIONS):
            result_message += str(ind) + " " + function + "\n"
        return result_message

    def _get_enter_func_set_message(self) -> str:
        return "Введите только номера через пробел: "

    def _get_empty_input_message(self) -> str:
        return "Введите не пустую строку."
