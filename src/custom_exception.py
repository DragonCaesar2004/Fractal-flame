class CustomException(Exception):
    '''Этот класс предназначен для генерации пользовательских исключений '''
    def __init__(self, message):
        super().__init__(message)
