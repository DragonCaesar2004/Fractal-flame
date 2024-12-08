import time


# Декоратор для расчета времени выполнения функции
def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Начало замера
        result = func(*args, **kwargs)  # Выполнение основной логики функции
        end_time = time.time()  # Конец замера
        execution_time = end_time - start_time  # Время выполнения
        print(
            f"Время выполнения функции '{func.__name__}': {execution_time:.2f} секунд"
        )
        return result

    return wrapper
