import sys
import pygame
from button import Button
from car_config import CAR_CONFIGS
from scripts.util import get_font, load_image, quit_game
from ui.ui import UIComponent

# Implementasi Game Option
class UIRules(UIComponent):
    def __init__(self, game):
        self.game = game
        self.screen = self.game.get_screen()
        self.font = get_font(36)
        self.background_img = load_image('bgfortuner3.png', is_color_key=False)

        self.back2_button = Button(520, 550, load_image('back.png', convert_alpha=True), 0.2)

        self.select_car1_button = Button(323, 444, load_image('back.png', convert_alpha=True), 0.2)
        self.select_car2_button = Button(664, 444, load_image('back.png', convert_alpha=True), 0.2)

        self.start_btn = Button(850, 125, load_image('start.png', convert_alpha=True), 0.4)
        self.rules_btn = Button(850, 325, load_image('help.png',convert_alpha=True), 0.4)
        self.music_btn = Button(50, 50, load_image('music.png',convert_alpha=True), 0.2)
        self.back_btn = Button(50, 600, load_image('back.png',convert_alpha=True), 0.2)
        self.home_btn = Button(520, 520, load_image('back.png',convert_alpha=True), 0.3)
        self.fullscreen_btn = Button(50, 120, load_image('fullscreen.png',convert_alpha=True), 0.2)
        self.selection_btn = Button(50, 250, load_image('back.png',convert_alpha=True), 0.2)
        self.bg_color = (144, 201, 120)

        self.rules_text = [
            "How to play :",
            "1. Player 1 menekan / spam tombol 'UP' untuk mempercepat.",
            "2. Player 2 menekan / spam tombol 'W' untuk mempercepat.",
            "3. Jika salah satu pemain mencapai jarak 2000 meter, pemain tersebut menang.",
            "4. Tekan tombol 'ESC' untuk keluar dari game."
        ]


    def render(self):
        self.is_active = True

        while self.is_active:
            self.screen.fill((0,0,0))
            self.back_btn.draw(self.screen)
            
            font = get_font(24)
            for i, text in enumerate(self.rules_text):
                rules_text = font.render(text, True, (255, 255, 255))
                text_rect = rules_text.get_rect(center=(630, 300 + i * 30))
                self.screen.blit(rules_text, text_rect)

            self.handle_event()

            pygame.display.update()
        
    
    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.back_btn.is_clicked():
                    self.is_active = False