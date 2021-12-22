import pygame

from GUI import Direction
from GUI.Direction import DIRECTION
from GUI.State import State


class Screen(object):

    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.font = pygame.font.Font('freesansbold.ttf', 16)
        self.title = pygame.font.Font('freesansbold.ttf', 32)
        self.main_title = pygame.font.Font('freesansbold.ttf', 64)

    def write_main_title(self, x: int, y: int, message: str, background: tuple = False,
                         foreground: tuple = (255, 255, 255), direction: DIRECTION = DIRECTION.CENTER):
        msg = self.main_title.render(message, True, background, foreground)

        return self._write_msg(x, y, msg, direction)

    def write_title(self, x: int, y: int, message: str, background: tuple = False,
                    foreground: tuple = (255, 255, 255), direction: DIRECTION = DIRECTION.CENTER):
        msg = self.title.render(message, True, background, foreground)

        return self._write_msg(x, y, msg, direction)

    def _write_msg(self, x: int, y: int, msg, direction: Direction):
        # Apply function in Enum to the rect
        rect = direction(msg.get_rect(), x, y)

        # Draw the rectangle
        self.screen.blit(msg, rect)

        return rect

    def write(
            self, x: int, y: int, message: str, background: tuple = (0, 0, 0),
            foreground: tuple = (255, 255, 255), direction: DIRECTION = DIRECTION.CENTER,
    ) -> None:
        """Write the message on the screen with (x, y) as center"""

        # Render the message
        msg = self.font.render(message, True, background, foreground)
        return self._write_msg(x, y, msg, direction)

    def render(self, events) -> State:
        raise NotImplementedError()
