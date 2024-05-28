import pygame
from button import Button
from car_config import CAR_CONFIGS
from player import Player
from scripts.util import get_font, load_image, quit_game
from ui.ui import UIComponent
from ui.ui_car_selection import UICarSelection

# Implementasi Game Option
class UICarInfo(UIComponent):
    def __init__(self, game):
        self.game = game
        self.screen: pygame.Surface = self.game.get_screen()
        self.font = get_font(36)
        self.background_img = load_image('bgfortuner.png', is_color_key=False)

        self.back2_button = Button(520, 550, load_image('back.png', convert_alpha=True), 0.2)

        self.select_car1_button = Button(323, 444, load_image('back.png', convert_alpha=True), 0.2)
        self.select_car2_button = Button(664, 444, load_image('back.png', convert_alpha=True), 0.2)

        self.ui_car_selection = UICarSelection(self.game)
        
    def reload_data(self):
        self.player1: Player = self.game.get_player()[0] # [0] = player 1
        self.player2: Player = self.game.get_player()[1] # [1] = player 2

        self.car1_img = pygame.transform.scale(load_image(CAR_CONFIGS[self.player1.get_car_name()]['image_path'], convert_alpha=True), (300, 200))
        self.car2_img = pygame.transform.scale(load_image(CAR_CONFIGS[self.player2.get_car_name()]['image_path'], convert_alpha=True), (300, 200))

    def render(self):
        self.reload_data()

        self.is_active = True

        while self.is_active:
            self.screen.blit(self.background_img, (0,0))
            self.back2_button.draw(self.screen)
            self.select_car1_button.draw(self.screen)
            self.select_car2_button.draw(self.screen)

            self.screen.blit(self.car1_img, (290, 200))
            self.screen.blit(self.car2_img, (650, 200))

            self.handle_event()

            pygame.display.update()
        
    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.back2_button.is_clicked():
                    self.is_active = False
                if self.select_car1_button.is_clicked():
                    self.ui_car_selection.render(self.player1)
                    self.reload_data()
                if self.select_car2_button.is_clicked():
                    self.ui_car_selection.render(self.player2)
                    self.reload_data()