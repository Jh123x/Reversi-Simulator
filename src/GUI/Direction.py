import enum
from pygame.rect import Rect


def center(rect: Rect, x: int, y: int) -> Rect:
    rect.center = (x, y)
    return rect


def left(rect: Rect, x: int, y: int) -> Rect:
    rect.left = (x, y)
    return rect


def right(rect: Rect, x: int, y: int) -> Rect:
    rect.right = (x, y)
    return rect


def up(rect: Rect, x: int, y: int) -> Rect:
    rect.top = (x, y)
    return rect


def down(rect: Rect, x: int, y: int) -> Rect:
    rect.bottom = (x, y)
    return rect


class DIRECTION(enum):
    CENTER = center
    LEFT = left
    RIGHT = right
    UP = up
    DOWN = down
