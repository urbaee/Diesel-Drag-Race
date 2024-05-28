import sys
import pygame
from button import Button
from player import Player
from scripts.util import get_font, load_image, quit_game
from sfx import SFXController
from ui.ui import UIComponent
from ui.ui_car_info import UICarInfo

# Implementasi Game Option
class UIGame(UIComponent):
    def __init__(self, game):
        self.game = game
        self.screen = self.game.get_screen()
        self.font = get_font(36)
        self.background_img = pygame.transform.scale(load_image('backgroundgame2.jpg', is_color_key=False), (1280, 720))
        self.start_btn = Button(850, 125, load_image('start.png', convert_alpha=True), 0.4)
        self.rules_btn = Button(850, 325, load_image('help.png',convert_alpha=True), 0.4)
        self.music_btn = Button(50, 50, load_image('music.png',convert_alpha=True), 0.2)
        self.home_btn = Button(520, 520, load_image('back.png',convert_alpha=True), 0.3)
        self.fullscreen_btn = Button(50, 120, load_image('fullscreen.png',convert_alpha=True), 0.2)
        self.selection_btn = Button(50, 250, load_image('back.png',convert_alpha=True), 0.2)
        self.bg_color = (144, 201, 120)
        self.sfx_controller: SFXController = self.game.get_sfxcontroller()

    def render(self, player1, player2):
        self.game.reset_game()

        self.player1: Player = player1
        self.player2: Player = player2

        self.player1.apply_image()
        self.player2.apply_image()

        self.countdown(3)

        self.is_active = True
        victory_sounds = False

        while self.is_active:
            if not self.player1.get_distance_traveled() and not self.player2.get_distance_traveled():        
                self.player1.start_timer()
                self.player2.start_timer()  

            if not self.game.is_game_stop():
                self.player1.move()
                self.player2.move()        

            if self.player1.rect.right >= self.screen.get_width() + 270:
                self.player1.rect.left = -self.player1.rect.width
            if self.player2.rect.right >= self.screen.get_width() + 270:
                self.player2.rect.left = -self.player2.rect.width

            if not self.game.is_game_stop():
                current_max_speed = max(self.player1.get_speed(), self.player2.get_speed())
                current_background_img_x = self.game.get_background_img_x() - current_max_speed

                self.game.set_background_img_x(current_background_img_x)

                if current_background_img_x <= -self.screen.get_width():
                    self.game.set_background_img_x(0)   

            self.draw_bg()
            self.player1.draw(self.screen)
            self.player2.draw(self.screen)
            self.draw_player_text()
            self.draw_distance(self.player1.get_distance_traveled(), 1)
            self.draw_distance(self.player2.get_distance_traveled(), 2)

            winner = self.check_winner()

            if winner:
                font = get_font(36)
                text = font.render(winner, True, (255, 255, 255))
                self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, self.screen.get_height() // 2 - text.get_height() // 2))
                self.home_btn.draw(self.screen)

                if winner is not None:
                    if winner == "Player 1":
                        if not self.game.win:
                            self.time_taken = self.player2.stop_timer()
                            self.game.win = True
                        self.time_taken = self.player1.stop_timer()
                    else:
                        if not self.game.win:
                            self.time_taken = self.player2.stop_timer()
                            self.game.win = True
                        self.time_text = f"Time taken: {self.time_taken:.2f} seconds"

                text = font.render(self.time_text, True, (0, 0, 0))
                self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, self.screen.get_height() // 2 + text.get_height() // 2))
                
                pygame.mixer.music.set_volume(0)
                self.sfx_controller.stop('engine')
                if not victory_sounds:
                            self.sfx_controller.stop('background')
                            self.sfx_controller.play('speak')
                            self.sfx_controller.play('victory')
                            victory_sounds = True
            self.handle_event()

            pygame.display.update()
            self.game.clock.tick(self.game.FPS)
            
    def check_winner(self):
        if self.player1.get_distance_traveled() >= 2000:
            self.game.game_stop = True
            return "Player 1 WIN!"
        elif self.player2.get_distance_traveled() >= 2000:
            self.game.game_stop = True
            return "Player 2 WIN!"
        return None

    def toggle_music(self):
        if self.music_muted:
            pygame.mixer.music.set_volume(0.5)
        else:
            pygame.mixer.music.set_volume(0) 
        self.music_muted = not self.music_muted 

    def draw_bg(self):
        background_img_x = self.game.get_background_img_x()
        self.screen.fill(self.bg_color)
        self.screen.blit(self.background_img, (background_img_x, 0))
        self.screen.blit(self.background_img, (background_img_x + self.screen.get_width(), 0))

    def draw_distance(self, distance, player):
        font = get_font(24)
        if player == 1:
            text = font.render(f'Distance Player 1: {distance:.2f} meters', True, (0, 0, 0))
            text_rect = text.get_rect(midtop=(self.screen.get_width() // 4, 10))
        else:
            text = font.render(f'Distance Player 2: {distance:.2f} meters', True, (0, 0, 0))
            text_rect = text.get_rect(midtop=(3 * self.screen.get_width() // 4, 10))
        self.screen.blit(text, text_rect)

    def draw_player_text(self):
        font = get_font(24)
        player1_text = font.render('Player 1', True, (255, 255, 255))
        player1_text_rect = player1_text.get_rect(midtop=self.player1.rect.midtop)
        self.screen.blit(player1_text, player1_text_rect)

        player2_text = font.render('Player 2', True, (255, 255, 255))
        player2_text_rect = player2_text.get_rect(midtop=self.player2.rect.midtop)
        self.screen.blit(player2_text, player2_text_rect)

    def countdown(self, time):
        countdown = time

        while countdown > 0:
            self.sfx_controller.play('countdown')
            self.screen.fill((0, 0, 0))  
            font = get_font(100)
            text = font.render(str(countdown), True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            self.screen.blit(text, text_rect)
            pygame.display.flip()  
            pygame.time.wait(1000)  
            countdown -= 1
        
        self.sfx_controller.play('go')

    def handle_event(self):
        sound_stop = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.home_btn.is_clicked():
                    self.sfx_controller.stop('victory')
                    self.sfx_controller.play('background')
                    self.is_active = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.sfx_controller.stop('engine')
                    self.sfx_controller.stop('victory')
                    self.sfx_controller.stop('speak')
                    self.is_active = False
                if event.key == pygame.K_UP:
                    self.player1.accelerate()
                    if not sound_stop:
                        self.sfx_controller.play('engine')
                        sound_stop = True
                if event.key == pygame.K_w:
                    self.player2.accelerate()
                    if not sound_stop:
                        self.sfx_controller.play('engine')
                        sound_stop = True
                if event.key == pygame.K_x:
                    self.sfx_controller.set_volume('background', 0)
                if event.key == pygame.K_z:
                    self.sfx_controller.set_volume('background', 0.5)        
                if event.key == pygame.K_f:
                    pygame.display.toggle_fullscreen()