import sys  # Import the sys module for system-specific parameters and functions.
import pygame  # Import the pygame library for game development.
from button import Button  # Import the Button class from a module named 'button'.
from car_config import CAR_CONFIGS  # Import car configurations from a module named 'car_config'.
from player import Player  # Import the Player class from a module named 'player'.
from scripts.util import get_font, load_image, quit_game  # Import specific functions from a module named 'util' in a package named 'scripts'.
from ui.ui import UIComponent  # Import the UIComponent class from a module named 'ui' inside a package also named 'ui'.

# Implementasi Game Option
class UICarSelection(UIComponent):  # Define a new class UICarSelection that inherits from UIComponent.
    def __init__(self, game):  # Define the constructor method for UICarSelection class.
        self.game = game  # Assign the game parameter to an instance variable game.
        self.screen: pygame.Surface = self.game.get_screen()  # Get the screen surface from the game and assign it to self.screen, specifying the type as pygame.Surface.
        self.font = get_font(36)  # Set the font for the UI.
        self.background_img = pygame.transform.scale(load_image('garage.jpg', is_color_key=False), (1280, 720))  # Load and scale the background image for the car selection screen.

        # Initializing buttons with images for navigation and interaction.
        self.right_arrow_btn = Button(820, 332, load_image('right_arrow.png', convert_alpha=True), 0.3)
        self.left_arrow_btn = Button(354, 332, load_image('left_arrow.png', convert_alpha=True), 0.3)
        self.back_btn = Button(570, 600, load_image('back.png', convert_alpha=True), 0.2)
        self.select_btn = Button(550, 480, load_image('select_car.png', convert_alpha=True), 0.3)

        self.car_img_list = []  # Initialize an empty list to store car images.
        self.selected_player: Player  # Initialize the selected_player attribute to hold a reference to the player object whose car is being selected.

    def render(self, player):  # Define the render method to display the car selection interface.
        self.selected_player = player  # Set the selected_player attribute to the provided player object.
        self.car_img_list = []  # Initialize an empty list to store car images.
        self.car_name_list = []  # Initialize an empty list to store car names.
        
        # Loop through car configurations to load and scale images for each car, appending them to self.car_img_list.
        for _, car_config in CAR_CONFIGS.items():
            car_img = pygame.transform.scale(load_image(car_config['image_path'], convert_alpha=True), (300, 200))
            self.car_img_list.append(car_img)
            self.car_name_list.append(car_config['car_name'])

        self.showing_car_index = 0  # Initialize the index for the currently displayed car image.
        self.is_active = True  # Set is_active flag to True to start rendering the car selection screen.

        # Loop to render the car selection screen until the selection is made or the user exits.
        while self.is_active:
            self.screen.blit(self.background_img, (0, 0))  # Draw the background image on the screen.
            self.back_btn.draw(self.screen)  # Draw the back button on the screen.
            self.select_btn.draw(self.screen)  # Draw the select button on the screen.
            self.screen.blit(self.car_img_list[self.showing_car_index], (482, 270))  # Draw the current car image on the screen.

            self.right_arrow_btn.draw(self.screen)  # Draw the right arrow button on the screen.
            self.left_arrow_btn.draw(self.screen)  # Draw the left arrow button on the screen.

            self.handle_event()  # Call the handle_event method to handle user interactions.

            pygame.display.update()  # Update the display to show any changes made.

    def handle_event(self):  # Define the method to handle user events.
        for event in pygame.event.get():  # Iterate through all the events in the event queue.
            if event.type == pygame.QUIT:  # Check for the QUIT event to handle the user closing the window.
                quit_game()  # Quit the game.
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Check for mouse button click events.
                if self.back_btn.is_clicked():  # Check if the back button is clicked.
                    self.is_active = False  # Set is_active flag to False to exit the car selection screen.
                if self.right_arrow_btn.is_clicked():  # Check if the right arrow button is clicked.
                    if self.showing_car_index < len(self.car_img_list) - 1:
                        self.showing_car_index += 1  # Increment the index to display the next car image.
                    else:
                        self.showing_car_index = 0  # Reset the index to display the first car image.
                if self.left_arrow_btn.is_clicked():  # Check if the left arrow button is clicked.
                    if self.showing_car_index > 0:
                        self.showing_car_index -= 1  # Decrement the index to display the previous car image.
                    else:
                        self.showing_car_index = len(self.car_img_list) - 1  # Set the index to display the last car image.
                if self.select_btn.is_clicked():  # Check if the select button is clicked.
                    self.selected_player.set_car_name(self.car_name_list[self.showing_car_index])  # Set the selected car name for the player.
                    self.is_active = False  # Set is_active flag to False to exit the car selection screen.
