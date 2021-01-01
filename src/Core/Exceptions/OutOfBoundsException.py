from .GeneralException import GeneralException


class OutOfBoundsException(GeneralException):
    def __init__(self, message):
        super().__init__(f"Out of bounds {message}")
