import pygame
from GUI.Screens.Screen import Screen
from GUI.Screens.Screen import Screen
from GUI.State import State


class MenuScreen(Screen):

    def __init__(self, screen):
        super().__init__(screen)
        self.draw_menu()

    def draw_menu(self):
        """
        Draws the menu for the game
        """
        start_of_row = self.height // 2 + self.height // 16
        x_coord = self.width // 2

        self.title_btn = self.write_main_title(x_coord, 64, "Othello") 

        self.play_btn = self.write_title(
            x_coord, start_of_row, "Single Player")

        self.two_player_btn = self.write_title(
            x_coord, start_of_row + 40, "Two Player")

        self.quit_btn = self.write_title(
            x_coord, start_of_row + 80, "Quit")

    def render(self, events) -> State:
        self.draw_menu()
        for event in events:
            # Todo check button clicks
            if event.type == pygame.MOUSEBUTTONUP:
                if self.play_btn.collidepoint(event.pos):
                    return State.AGAINST_AI
                elif self.two_player_btn.collidepoint(event.pos):
                    return State.TWO_PLAYER
                elif self.quit_btn.collidepoint(event.pos):
                    return State.QUIT

        
        return State.MENU
