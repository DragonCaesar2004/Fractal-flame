import logging
import platform

from src.command_line_interface import CommandLineInterface
from src.manager import Manager

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info(platform.python_version())
    try:
        cli = CommandLineInterface()
        user_data = cli.get_user_data()
        manager = Manager(user_data, cli)
        
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
