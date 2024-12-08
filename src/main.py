import logging
import platform

from src.command_line_interface import CommandLineInterface
from src.config import USING_MULTIPROCESSING
from src.core.fractal_manager import Manager

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    """
    Основная функция запуска приложения.

    Эта функция выполняет следующие действия:
    1. Логирует версию Python, используемую для выполнения программы.
    2. Создает экземпляр интерфейса командной строки и получает данные пользователя.
    3. Создает экземпляр менеджера, который обрабатывает данные пользователя и создает фрактальные пламя.

    Если возникает исключение в любом из вышеупомянутых шагов, оно обрабатывается,
    и сообщение об ошибке выводится на экран.
    """
    logger.info(platform.python_version())
    try:
        cli = CommandLineInterface()
        user_data = cli.get_user_data()

        manager = Manager(user_data)
        manager.create_fractal_flame(multistream=USING_MULTIPROCESSING)
        cli.show_config()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
