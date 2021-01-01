import enum
from pygame.rect import Rect


def center(rect: Rect, x: int, y: int) -> None:
    rect.center = (x, y)


def left(rect: Rect, x: int, y: int) -> None:
    rect.left = (x, y)


def right(rect: Rect, x: int, y: int) -> None:
    rect.right = (x, y)


def up(rect: Rect, x: int, y: int) -> None:
    rect.top = (x, y)


def down(rect: Rect, x: int, y: int) -> None:
    rect.bottom = (x, y)


class DIRECTION(enum):
    CENTER = center
    LEFT = left
    RIGHT = right
    UP = up
    DOWN = down
