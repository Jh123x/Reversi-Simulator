from .GeneralException import GeneralException

class AlreadyTakenException(GeneralException):
    def __init__(self, message:str, player:int):
        super().__init__(f"The position is already taken by {player} {message}")