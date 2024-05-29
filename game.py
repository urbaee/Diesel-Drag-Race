import pygame
from player import Player  # Importing the Player class
from car_config import CAR_CONFIGS  # Importing car configurations
from sfx import SFXController  # Importing the sound effects controller
from ui.ui_main_menu import UIMainMenu  # Importing the main menu UI

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen_width = 1280  # Screen width
        self.screen_height = 720  # Screen height
        icon_img = pygame.image.load('images/icon.png')  # Load the game icon
        pygame.display.set_icon(icon_img)  # Set the game icon
        self.__screen = pygame.display.set_mode((self.screen_width, self.screen_height))  # Create the game window
        pygame.display.set_caption('DIESEL DRAG RACE')  # Set the game window title
        self.clock = pygame.time.Clock()  # Initialize the game clock

        self.FPS = 60  # Frames per second
        self.bg_color = (144, 201, 120)  # Background color
        self.font_size = 24  # Font size
        self.background_img_x = 0  # Background image x position

        self.__default_car1 = 'car1'  # Default car for player 1
        self.__default_car2 = 'car2'  # Default car for player 2

        self.music_muted = False  # Flag to indicate if music is muted
        self.game_stop = False  # Flag to indicate if the game is stopped
        self.time_taken = 0  # Time taken for the race
        self.win = False  # Flag to indicate if a player has won

        self.__sfx_controller = SFXController()  # Initialize the sound effects controller
        self.__sfx_controller.add_sfx('engine', 'engine.wav', 0.3)  # Add engine sound effect
        self.__sfx_controller.add_sfx('speak', 'victory_speak.mp3', 1)  # Add victory speak sound effect
        self.__sfx_controller.add_sfx('victory', 'victory.mp3', 0.5)  # Add victory sound effect
        self.__sfx_controller.add_sfx('background', 'ROTS.mp3', 0.5)  # Add background music
        self.__sfx_controller.add_sfx('countdown', 'countdown.mp3', 0.6)  # Add countdown sound effect
        self.__sfx_controller.add_sfx('go', 'go.mp3', 1)  # Add go sound effect

        # Initialize players with default configurations
        self.__player1 = Player(CAR_CONFIGS[self.__default_car1], 100, 600, self.screen_width, self.screen_height)
        self.__player2 = Player(CAR_CONFIGS[self.__default_car2], 100, 400, self.screen_width, self.screen_height)

        self.reset_game()  # Reset the game to its initial state

        self.ui_main_menu = UIMainMenu(self.__screen, self)  # Initialize the main menu UI

    def get_sfxcontroller(self):
        return self.__sfx_controller  # Get the sound effects controller

    def get_background_img_x(self):
        return self.background_img_x  # Get the background image x position

    def set_background_img_x(self, pos):
        self.background_img_x = pos  # Set the background image x position

    def is_game_stop(self):
        return self.game_stop  # Check if the game is stopped

    def get_screen(self):
        return self.__screen  # Get the game screen

    def get_player(self):
        return [self.__player1, self.__player2]  # Get the players

    def reset_game(self):
        self.start_game = False  # Flag to indicate if the game has started
        self.countdown = 3  # Countdown timer for race start
        self.__player1.reset()  # Reset player 1
        self.__player2.reset()  # Reset player 2
        self.win = False  # Reset the win flag
        self.time_taken = 0  # Reset the time taken
        self.time_text = ""  # Reset the time text
        self.background_img_x = 0  # Reset the background image x position
        self.game_stop = False  # Reset the game stop flag

    def toggle_music(self):
        if self.music_muted:
            self.__sfx_controller.mute('background')  # Mute the background music
        else:
            self.__sfx_controller.unmute('background')  # Unmute the background music
        self.music_muted = not self.music_muted  # Toggle the music muted flag

    def run(self):
        try:
            self.ui_main_menu.render()  # Render the main menu UI
        except Exception as e:
            print(e.with_traceback())  # Print the traceback of the exception
            print("An error occurred:", str(e))  # Print the error message
