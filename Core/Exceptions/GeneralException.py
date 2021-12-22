class GeneralException(Exception):
    def __init__(self, message: str):
        """The general exception for the game"""
        super().__init__(message)
