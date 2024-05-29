import sys  # Import the sys module for system-specific parameters and functions.
import pygame  # Import the pygame library for game development.
import os  # Import the os module for interacting with the operating system.

BASE_IMG_PATH = 'images/'  # Define the base path for loading images.

# Define a function to load an image.
def load_image(path, color_key=(0,0,0), convert_alpha=False, is_color_key=True):
    # Load the image from the specified path.
    if convert_alpha:
        img = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()  # Load image with alpha transparency.
    else:
        img = pygame.image.load(BASE_IMG_PATH + path).convert()  # Load image without alpha transparency.
    
    if is_color_key:
        img.set_colorkey(color_key)  # Set color key for transparency. 

    return img  # Return the loaded image.

# Define a function to load multiple images from a directory.
def load_images(path, is_color_key=True, convert_alpha=False):
    images = []  # Initialize an empty list to store loaded images.
    
    # Loop through each image file in the specified directory path.
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name, is_color_key=is_color_key, convert_alpha=convert_alpha))  # Load each image and append it to the list.
        
    return images  # Return the list of loaded images.

# Define a function to get a font object with the specified size.
def get_font(size):
        return pygame.font.Font("textfont/Minecraft.ttf", size)  # Return a font object with the specified size.

# Define a function to quit the game.
def quit_game():
    pygame.quit()  # Quit the pygame library.
    sys.exit()  # Exit the Python interpreter.
