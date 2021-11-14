import pygame
from GUI.State import State
from GUI.Direction import DIRECTION


class Screen(object):

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font('freesansbold.ttf', 16)
        self.title = pygame.font.Font('freesansbold.ttf', 32)

    def write(
        self, x: int, y: int, message: str, background: tuple = (0, 0, 0),
        foreground: tuple = (255, 255, 255), direction: DIRECTION = DIRECTION.CENTER, title: bool = False
    ) -> None:
        """Write the message on the screen with (x, y) as center"""

        # Render the message
        if title:
            msg = self.title.render(message, True, foreground)
        else:
            msg = self.font.render(message, True, background, foreground)

        # Apply function in Enum to the rect
        rect = direction(msg.get_rect(), x, y)

        # Draw the rectangle
        self.screen.blit(msg, rect)

    def render(self, events) -> State:
        raise NotImplementedError()