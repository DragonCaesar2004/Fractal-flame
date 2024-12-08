import time
from collections.abc import Callable
from typing import Any


# Декоратор для расчета времени выполнения функции
def timing_decorator(func: Callable) -> Callable:
    """
    Декоратор для измерения времени выполнения функции.

    Этот декоратор оборачивает функцию, вычисляет и выводит время её выполнения.

    Параметры:
        func (Callable): Функция, время выполнения которой необходимо измерить.

    Возвращает:
        Callable: Обёртка функции, которая выводит время её выполнения перед возвращением результата.

    Пример использования:
        @timing_decorator
        def example_function():
            # Логика функции
            pass
    """

    def wrapper(
        *args: tuple[Any, ...], **kwargs: dict[Any, Any]
    ) -> (
        Any
    ):  # noqa: ANN401 чтобы ruff не ругался на динамически возвращаемый тип данных
        start_time = time.time()  # Начало замера
        result = func(*args, **kwargs)  # Выполнение основной логики функции
        end_time = time.time()  # Конец замера
        execution_time = end_time - start_time  # Время выполнения
        print(
            f"Время выполнения функции '{func.__name__}': {execution_time:.2f} секунд"
        )
        return result

    return wrapper
