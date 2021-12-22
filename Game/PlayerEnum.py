import enum


class PlayerTurn(enum.Enum):
    """
    Enum for the player turn.
    """
    WHITE = -1
    BLACK = 1

    def to_index(self) -> int:
        return int(self.value < 0)

    def from_index(self, index) -> 'PlayerTurn':
        if index < 0:
            raise ValueError("Index must be 0 or 1")
        return PlayerTurn((index + 1) % 2)
