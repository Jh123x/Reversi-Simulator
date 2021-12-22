from enum import Enum

from pygame.rect import Rect


def center(rect: Rect, x: int, y: int) -> Rect:
    rect.center = (x, y)
    return rect


def left(rect: Rect, x: int, y: int) -> Rect:
    rect.center = (x + rect.width / 2, y)
    return rect


def right(rect: Rect, x: int, y: int) -> Rect:
    rect.center = (x - rect.width / 2, y)
    return rect


def up(rect: Rect, x: int, y: int) -> Rect:
    rect.center = (x, y - rect.height / 2)
    return rect


def down(rect: Rect, x: int, y: int) -> Rect:
    rect.center = (x, y + rect.height / 2)
    return rect


class DIRECTION(Enum):
    CENTER = center
    LEFT = left
    RIGHT = right
    UP = up
    DOWN = down
