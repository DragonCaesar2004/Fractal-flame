import time
from collections.abc import Callable
from src.utils.timing_decorator import (
    timing_decorator,
)  # Замените 'your_module' на имя вашего файла


# Фиктивная функция для тестов
@timing_decorator
def sample_function(duration: float) -> str:
    """
    Функция, которая искусственно ждет время, чтобы протестировать декоратор.
    """
    time.sleep(duration)
    return "done"


def test_timing_decorator_output(capfd):
    """
    Проверяем, что декоратор корректно выводит время выполнения функции.
    """
    expected_duration = 1.0  # Задаем продолжительность
    result = sample_function(expected_duration)
    out, _ = capfd.readouterr()  # Захватываем вывод функции

    # Проверяем, что результат работы функции корректен
    assert result == "done"

    # Проверяем, что время выполнения выводится корректно
    assert "Время выполнения функции 'sample_function':" in out

    # Дополнительно можно проверить близость времени выполнения
    assert (
        abs(expected_duration - float(out.split()[-2])) < 0.1
    )  # Учитываем погрешность


def test_timing_decorator_execution_time():
    """
    Тест: Проверяем, что декоратор измеряет время выполнения с допустимой точностью.
    """
    expected_duration = 2.0  # Время, которое функция ждет
    start_time = time.time()
    sample_function(expected_duration)
    end_time = time.time()

    # Разница между концом и началом не должна сильно отличаться от expected_duration
    assert (
        abs((end_time - start_time) - expected_duration) <= 0.1
    )  # Учитываем погрешность
