import logging
import platform

from src.command_line_interface import CommandLineInterface
from src.core.fractal_manager import Manager

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)
import time

def main() -> None:
    logger.info(platform.python_version())
    try:
        cli = CommandLineInterface()
        user_data = cli.get_user_data()
        start_time = time.time()

        manager = Manager(user_data)
        manager.create_fractal_flame(multistream=True)

        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Время выполнения: {execution_time} секунд")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
