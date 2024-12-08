class CustomError(Exception):
    """Этот класс предназначен для генерации пользовательских исключений."""

    def __init__(self, message: str) -> None:
        """Инициализация пользовательской ошибки."""
        super().__init__(message)
