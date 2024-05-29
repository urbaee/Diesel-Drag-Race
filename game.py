# game.py

import pygame
from player import Player
from car_config import CAR_CONFIGS
from sfx import SFXController
from ui.ui_main_menu import UIMainMenu

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen_width = 1280
        self.screen_height = 720
        icon_img = pygame.image.load('images/icon.png')
        pygame.display.set_icon(icon_img)
        self.__screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('DIESEL DRAG RACE')
        self.clock = pygame.time.Clock()

        self.FPS = 60
        self.bg_color = (144, 201, 120)
        self.font_size = 24
        self.background_img_x = 0

        self.__default_car1 = 'car1'
        self.__default_car2 = 'car2'

        self.music_muted = False
        self.game_stop = False
        self.time_taken = 0
        self.win = False

        self.__sfx_controller = SFXController()
        self.__sfx_controller.add_sfx('engine', 'engine.wav', 0.3)
        self.__sfx_controller.add_sfx('speak', 'victory_speak.mp3', 1)
        self.__sfx_controller.add_sfx('victory', 'victory.mp3', 0.5)
        self.__sfx_controller.add_sfx('background', 'ROTS.mp3', 0.5)
        self.__sfx_controller.add_sfx('countdown', 'countdown.mp3', 0.6)
        self.__sfx_controller.add_sfx('go', 'go.mp3', 1)

        # default player config
        self.__player1 = Player(CAR_CONFIGS[self.__default_car1], 100, 600, self.screen_width, self.screen_height)
        self.__player2 = Player(CAR_CONFIGS[self.__default_car2], 100, 400, self.screen_width, self.screen_height)

        self.reset_game()

        self.ui_main_menu = UIMainMenu(self.__screen, self)

    def get_sfxcontroller(self):
        return self.__sfx_controller

    def get_background_img_x(self):
        return self.background_img_x

    def set_background_img_x(self, pos):
        self.background_img_x = pos

    def is_game_stop(self):
        return self.game_stop

    def get_screen(self):
        return self.__screen

    def get_player(self):
        return [self.__player1, self.__player2]

    def reset_game(self):
        self.start_game = False
        self.countdown = 3
        self.__player1.reset()
        self.__player2.reset()
        self.win = False
        self.time_taken = 0
        self.time_text = ""
        self.background_img_x = 0
        self.game_stop = False

    def toggle_music(self):
        if self.music_muted:
            self.__sfx_controller.mute('background')
        else:
            self.__sfx_controller.unmute('background')
        self.music_muted = not self.music_muted    

    def run(self):
        try:
            self.ui_main_menu.render()
        except Exception as e:
            print(e.with_traceback())
            print("An error occurred:", str(e))
