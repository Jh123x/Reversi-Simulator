import enum


class PlayerTurn(enum.Enum):
    """
    Enum for the player turn.
    """
    WHITE = 1
    BLACK = 2

    def to_index(self):
        return self.value - 1

    def from_index(self, index):
        if index < 0:
            raise ValueError("Index must be 0 or 1")
        return PlayerTurn((index + 1) % 2)