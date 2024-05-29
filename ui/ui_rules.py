import sys
import pygame
from button import Button  # Import Button class from button module
from car_config import CAR_CONFIGS  # Import car configurations
from scripts.util import get_font, load_image, quit_game  # Import utility functions
from ui.ui import UIComponent  # Import UIComponent base class

# Implement the Game Option
class UIRules(UIComponent):
    def __init__(self, game):
        self.game = game  # Store the reference to the main game object
        self.screen = self.game.get_screen()  # Get the main screen surface
        self.font = get_font(36)  # Load the font with size 36
        self.background_img = load_image('bgfortuner3.png', is_color_key=False)  # Load the background image

        # Initialize various buttons used in the UI
        self.back2_button = Button(520, 550, load_image('back.png', convert_alpha=True), 0.2)
        self.select_car1_button = Button(323, 444, load_image('back.png', convert_alpha=True), 0.2)
        self.select_car2_button = Button(664, 444, load_image('back.png', convert_alpha=True), 0.2)

        self.start_btn = Button(850, 125, load_image('start.png', convert_alpha=True), 0.4)
        self.rules_btn = Button(850, 325, load_image('help.png', convert_alpha=True), 0.4)
        self.music_btn = Button(50, 50, load_image('music.png', convert_alpha=True), 0.2)
        self.back_btn = Button(50, 600, load_image('back.png', convert_alpha=True), 0.2)
        self.home_btn = Button(520, 520, load_image('back.png', convert_alpha=True), 0.3)
        self.fullscreen_btn = Button(50, 120, load_image('fullscreen.png', convert_alpha=True), 0.2)
        self.selection_btn = Button(50, 250, load_image('back.png', convert_alpha=True), 0.2)

        self.bg_color = (144, 201, 120)  # Set the background color

        # Define the rules text
        self.rules_text = [
            "How to play:",
            "1. Player 1 presses/spams the 'UP' key to speed up.",
            "2. Player 2 presses/spams the 'W' key to speed up.",
            "3. If a player reaches 2000 meters, that player wins.",
            "4. Press the 'ESC' key to exit the game."
        ]

    def render(self):
        self.is_active = True  # Flag to indicate if the UI is active

        while self.is_active:
            self.screen.fill((0, 0, 0))  # Fill the screen with black color
            self.back_btn.draw(self.screen)  # Draw the back button
            
            font = get_font(24)  # Load the font with size 24
            for i, text in enumerate(self.rules_text):  # Iterate over the rules text
                rules_text = font.render(text, True, (255, 255, 255))  # Render the text
                text_rect = rules_text.get_rect(center=(630, 300 + i * 30))  # Position the text
                self.screen.blit(rules_text, text_rect)  # Draw the text on the screen

            self.handle_event()  # Handle events

            pygame.display.update()  # Update the display
        
    def handle_event(self):
        for event in pygame.event.get():  # Iterate over the events
            if event.type == pygame.QUIT:  # Check if the event is to quit the game
                quit_game()  # Quit the game
            if event.type == pygame.MOUSEBUTTONDOWN:  # Check if the mouse button is pressed
                if self.back_btn.is_clicked():  # Check if the back button is clicked
                    self.is_active = False  # Deactivate the UI
