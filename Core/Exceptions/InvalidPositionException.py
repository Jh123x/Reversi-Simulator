from .GeneralException import GeneralException


class InvalidPositionException(GeneralException):
    def __init__(self, message: str):
        super().__init__(f"Invalid position {message}")
