import pygame  # Import the pygame library for game development.
from button import Button  # Import the Button class from a module named 'button'.
from car_config import CAR_CONFIGS  # Import car configurations from a module named 'car_config'.
from player import Player  # Import the Player class from a module named 'player'.
from scripts.util import get_font, load_image, quit_game  # Import specific functions from a module named 'util' in a package named 'scripts'.
from ui.ui import UIComponent  # Import the UIComponent class from a module named 'ui' inside a package also named 'ui'.
from ui.ui_car_selection import UICarSelection  # Import the UICarSelection class from a module named 'ui_car_selection' inside a package named 'ui'.

# Implementasi Game Option
class UICarInfo(UIComponent):  # Define a new class UICarInfo that inherits from UIComponent.
    def __init__(self, game):  # Define the constructor method for UICarInfo class.
        self.game = game  # Assign the game parameter to an instance variable game.
        self.screen: pygame.Surface = self.game.get_screen()  # Get the screen surface from the game and assign it to self.screen, specifying the type as pygame.Surface.
        self.font = get_font(36)  # Set the font for the UI.
        self.background_img = pygame.transform.scale(load_image('garage.jpg', is_color_key=False), (1280, 720))  # Load and scale the background image for the car info screen.

        # Initialize buttons with images for navigation and interaction.
        self.back2_button = Button(570, 550, load_image('back.png', convert_alpha=True), 0.2)
        self.select_car1_button = Button(360, 444, load_image('p1.png', convert_alpha=True), 0.3)
        self.select_car2_button = Button(740, 444, load_image('p2.png', convert_alpha=True), 0.3)
        
        self.ui_car_selection = UICarSelection(self.game)  # Create an instance of UICarSelection to handle car selection.

    def reload_data(self):  # Define a method to reload data, including player information and car images.
        self.player1: Player = self.game.get_player()[0]  # Get the first player from the game and assign it to player1.
        self.player2: Player = self.game.get_player()[1]  # Get the second player from the game and assign it to player2.

        # Load and scale the images of the cars selected by player1 and player2.
        self.car1_img = pygame.transform.scale(load_image(CAR_CONFIGS[self.player1.get_car_name()]['image_path'], convert_alpha=True), (300, 200))
        self.car2_img = pygame.transform.scale(load_image(CAR_CONFIGS[self.player2.get_car_name()]['image_path'], convert_alpha=True), (300, 200))

    def render(self):  # Define the render method to display the car information interface.
        self.reload_data()  # Call the reload_data method to update player and car information.

        self.is_active = True  # Set is_active flag to True to start rendering the car info screen.

        # Loop to render the car info screen until the user exits.
        while self.is_active:
            self.screen.blit(self.background_img, (0,0))  # Draw the background image on the screen.
            self.back2_button.draw(self.screen)  # Draw the back button on the screen.
            self.select_car1_button.draw(self.screen)  # Draw the button to select car for player 1 on the screen.
            self.select_car2_button.draw(self.screen)  # Draw the button to select car for player 2 on the screen.

            self.screen.blit(self.car1_img, (290, 200))  # Draw the car image for player 1 on the screen.
            self.screen.blit(self.car2_img, (650, 200))  # Draw the car image for player 2 on the screen.

            self.handle_event()  # Call the handle_event method to handle user interactions.

            pygame.display.update()  # Update the display to show any changes made.
        
    def handle_event(self):  # Define the method to handle user events.
        for event in pygame.event.get():  # Iterate through all the events in the event queue.
            if event.type == pygame.QUIT:  # Check for the QUIT event to handle the user closing the window.
                quit_game()  # Quit the game.
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Check for mouse button click events.
                if self.back2_button.is_clicked():  # Check if the back button is clicked.
                    self.is_active = False  # Set is_active flag to False to exit the car info screen.
                if self.select_car1_button.is_clicked():  # Check if the button to select car for player 1 is clicked.
                    self.ui_car_selection.render(self.player1)  # Render the car selection screen for player 1.
                    self.reload_data()  # Reload data after car selection.
                if self.select_car2_button.is_clicked():  # Check if the button to select car for player 2 is clicked.
                    self.ui_car_selection.render(self.player2)  # Render the car selection screen for player 2.
                    self.reload_data()  # Reload data after car selection.
