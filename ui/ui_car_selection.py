import sys
import pygame
from button import Button
from car_config import CAR_CONFIGS
from player import Player
from scripts.util import get_font, load_image, quit_game
from ui.ui import UIComponent

# Implementasi Game Option
class UICarSelection(UIComponent):
    def __init__(self, game):
        self.game = game
        self.screen: pygame.Surface = self.game.get_screen()
        self.font = get_font(36)
        self.background_img = pygame.transform.scale(load_image('garage.jpg', is_color_key=False), (1280, 720))

        self.right_arrow_btn = Button(820, 332, load_image('right_arrow.png', convert_alpha=True), 0.3)
        self.left_arrow_btn = Button(354, 332, load_image('left_arrow.png', convert_alpha=True), 0.3)

        self.back_btn = Button(570, 600, load_image('back.png', convert_alpha=True), 0.2)
        self.select_btn = Button(550, 480, load_image('select_car.png', convert_alpha=True), 0.3)

        self.car_img_list = [] 

        self.selected_player: Player

    def render(self, player):
        self.selected_player = player

        self.car_img_list = [] 
        self.car_name_list = []
        for _, car_config in CAR_CONFIGS.items():
            car_img = pygame.transform.scale(load_image(car_config['image_path'], convert_alpha=True), (300, 200))
            self.car_img_list.append(car_img)
            self.car_name_list.append(car_config['car_name'])

        self.showing_car_index = 0
        self.is_active = True

        while self.is_active:
            self.screen.blit(self.background_img, (0,0))
            self.back_btn.draw(self.screen)
            self.select_btn.draw(self.screen)

            self.screen.blit(self.car_img_list[self.showing_car_index], (482,270))

            self.right_arrow_btn.draw(self.screen)
            self.left_arrow_btn.draw(self.screen)

            self.handle_event()

            pygame.display.update()
        
    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_btn.is_clicked():
                    self.is_active = False
                if self.right_arrow_btn.is_clicked():
                    if (self.showing_car_index < len(self.car_img_list) - 1):
                        self.showing_car_index += 1
                    else:
                        self.showing_car_index = 0
                if self.left_arrow_btn.is_clicked():
                    if (self.showing_car_index > 0):
                        self.showing_car_index -= 1
                    else:
                        self.showing_car_index = len(self.car_img_list) - 1
                if self.select_btn.is_clicked():
                    self.selected_player.set_car_name(self.car_name_list[self.showing_car_index])
                    self.is_active = False

