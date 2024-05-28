import pygame
from button import Button
from scripts.util import get_font, load_image, quit_game
from sfx import SFXController
from ui.ui import UIComponent
from ui.ui_car_info import UICarInfo
from ui.ui_game import UIGame
from ui.ui_rules import UIRules

# Implementasi Game Option
class UIMainMenu(UIComponent):
    def __init__(self, screen, game):
        self.game = game
        self.screen = screen
        self.font = get_font(36)
        self.background_img = load_image('bgfortuner3.png', is_color_key=False)
        self.start_btn = Button(850, 125, load_image('start.png', convert_alpha=True), 0.4)
        self.rules_btn = Button(850, 325, load_image('help.png',convert_alpha=True), 0.4)
        self.music_btn = Button(50, 50, load_image('music.png',convert_alpha=True), 0.2)
        self.back_btn = Button(50, 600, load_image('back.png',convert_alpha=True), 0.2)
        self.home_btn = Button(520, 520, load_image('back.png',convert_alpha=True), 0.3)
        self.fullscreen_btn = Button(50, 120, load_image('fullscreen.png',convert_alpha=True), 0.2)
        self.selection_btn = Button(50, 250, load_image('back.png',convert_alpha=True), 0.2)
        self.bg_color = (144, 201, 120)

        self.sfx_contoller: SFXController = self.game.get_sfxcontroller()

        self.ui_car_info = UICarInfo(self.game)
        self.ui_game = UIGame(self.game)
        self.ui_rules = UIRules(self.game)

    def render(self):
        self.is_active = True
        self.sfx_contoller.play('background', loop=True)

        while self.is_active:
            self.screen.fill(self.bg_color)
            self.screen.blit(self.background_img, (0, 0))
            self.start_btn.draw(self.screen)
            self.rules_btn.draw(self.screen)
            self.music_btn.draw(self.screen)
            self.fullscreen_btn.draw(self.screen)
            self.selection_btn.draw(self.screen)

            self.handle_event()

            pygame.display.update()
        
    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if self.start_btn.is_clicked():
                        player = self.game.get_player()
                        self.ui_game.render(player[0], player[1])
                    if self.rules_btn.is_clicked():
                        self.ui_rules.render()
                    if self.music_btn.is_clicked():
                        self.sfx_contoller.mute()
                    if self.fullscreen_btn.is_clicked():
                        pygame.display.toggle_fullscreen()
                    if self.selection_btn.is_clicked():
                        self.ui_car_info.render()
                    
            if event.type == pygame.KEYDOWN:                                    
                if event.key == pygame.K_x:
                    pygame.mixer.music.set_volume(0)
                if event.key == pygame.K_z:
                    pygame.mixer.music.set_volume(0.5)
                if event.key == pygame.K_f:
                    pygame.display.toggle_fullscreen()   