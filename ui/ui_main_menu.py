# Import the Pygame library for game development
import pygame

# Import necessary classes and functions from custom modules
from button import Button
from scripts.util import get_font, load_image, quit_game
from sfx import SFXController
from ui.ui import UIComponent
from ui.ui_car_info import UICarInfo
from ui.ui_game import UIGame
from ui.ui_rules import UIRules

# Implementation of the Main Menu User Interface
class UIMainMenu(UIComponent):
    def __init__(self, screen, game):
        # Initialize the Main Menu UI component with screen and game objects
        self.game = game
        self.screen = screen
        
        # Get a font with a specified size for UI elements
        self.font = get_font(36)
        
        # Load the background image for the main menu
        self.background_img = load_image('bgfortuner.png', is_color_key=False)
        
        # Initialize buttons for various functionalities
        self.start_btn = Button(850, 125, load_image('start.png', convert_alpha=True), 0.4)
        self.rules_btn = Button(850, 325, load_image('help.png',convert_alpha=True), 0.4)
        self.music_btn = Button(50, 50, load_image('music.png',convert_alpha=True), 0.2)
        self.back_btn = Button(50, 600, load_image('back.png',convert_alpha=True), 0.2)
        self.home_btn = Button(520, 520, load_image('back.png',convert_alpha=True), 0.3)
        self.fullscreen_btn = Button(50, 120, load_image('fullscreen.png',convert_alpha=True), 0.2)
        self.selection_btn = Button(50, 250, load_image('car_select.png',convert_alpha=True), 0.23)
        
        # Set background color
        self.bg_color = (144, 201, 120)

        # Get the sound effects controller from the game object
        self.sfx_controller: SFXController = self.game.get_sfxcontroller()

        # Initialize UI components for car info, game, and rules
        self.ui_car_info = UICarInfo(self.game)
        self.ui_game = UIGame(self.game)
        self.ui_rules = UIRules(self.game)

    # Method to render the main menu UI
    def render(self):
        # Set the UI to active and play background music
        self.is_active = True
        self.sfx_controller.play('background', loop=True)

        # Main loop for rendering the UI
        while self.is_active:
            # Fill the screen with background color and draw UI elements
            self.screen.fill(self.bg_color)
            self.screen.blit(self.background_img, (0, 0))
            self.start_btn.draw(self.screen)
            self.rules_btn.draw(self.screen)
            self.music_btn.draw(self.screen)
            self.fullscreen_btn.draw(self.screen)
            self.selection_btn.draw(self.screen)

            # Handle user events
            self.handle_event()

            # Update the display
            pygame.display.update()
        
    # Method to handle user events
    def handle_event(self):
        # Iterate through all the events in the event queue
        for event in pygame.event.get():
            # If the event is to quit the game, quit
            if event.type == pygame.QUIT:
                quit_game()
            # If the event is a mouse button click
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # If the left mouse button is clicked
                if pygame.mouse.get_pressed()[0]:
                    # Check which button is clicked and perform corresponding actions
                    if self.start_btn.is_clicked():
                        self.sfx_controller.set_volume('background', 0.2)
                        player = self.game.get_player()
                        self.ui_game.render(player[0], player[1])
                    if self.rules_btn.is_clicked():
                        self.ui_rules.render()
                    if self.music_btn.is_clicked():
                        self.game.toggle_music()
                    if self.fullscreen_btn.is_clicked():
                        pygame.display.toggle_fullscreen()
                    if self.selection_btn.is_clicked():
                        self.ui_car_info.render()
            # If the event is a key press
            if event.type == pygame.KEYDOWN:
                # Check which key is pressed and perform corresponding actions
                if event.key == pygame.K_x:
                    self.sfx_controller.set_volume('background', 0)
                if event.key == pygame.K_z:
                    self.sfx_controller.set_volume('background', 0.5)
                if event.key == pygame.K_f:
                    pygame.display.toggle_fullscreen()
                if event.key == pygame.K_ESCAPE:
                    quit_game()
