import pygame
import time
from game_object import Sprite
from scripts.util import load_image  # Custom utility function for loading images
from car_config import CAR_CONFIGS  # Configuration dictionary for car attributes

class Player(Sprite):
    def __init__(self, config, x, y, screen_width, screen_height):
        super().__init__()
        self.x = x  # Initial x position
        self.y = y  # Initial y position
        self.__car_name = config['car_name']  # Car name from config
        self.__speed = config['initial_speed']  # Initial speed from config
        self.__max_speed = config['max_speed']  # Maximum speed from config
        self.__acceleration_rate = config['acceleration_rate']  # Acceleration rate from config
        img = load_image(config['image_path'], convert_alpha=True)  # Load the car image
        self.__scale = config['scale']  # Scale factor for the image
        self.image = pygame.transform.scale(img, (int(img.get_width() * self.__scale), int(img.get_height() * self.__scale)))  # Scale the image
        self.rect = self.image.get_rect()  # Get the rectangle area of the image
        self.rect.center = (x, y)  # Set the center of the rectangle to the initial position
        self.__distance_traveled = 0  # Initialize distance traveled
        self.__screen_width = screen_width  # Screen width
        self.__screen_height = screen_height  # Screen height
        self.__start_time = None  # Timer start time
        self.game_stop = False  # Flag to indicate if the game is stopped

    def apply_image(self):
        img = load_image(CAR_CONFIGS[self.__car_name]['image_path'], convert_alpha=True)  # Reload the car image based on the car name
        self.image = pygame.transform.scale(img, (int(img.get_width() * self.__scale), int(img.get_height() * self.__scale)))  # Scale the image

    def set_car_name(self, name):
        self.__car_name = name  # Set the car name

    def get_car_name(self):
        return self.__car_name  # Get the car name

    def set_speed(self, speed):
        self.__speed = speed  # Set the speed

    def get_speed(self):
        return self.__speed  # Get the speed
    
    def set_max_speed(self, max_speed):
        self.__max_speed = max_speed  # Set the maximum speed

    def get_max_speed(self):
        return self.__max_speed  # Get the maximum speed

    def set_acceleration_rate(self, acceleration_rate):
        self.__acceleration_rate = acceleration_rate  # Set the acceleration rate

    def get_acceleration_rate(self):
        return self.__acceleration_rate  # Get the acceleration rate

    def reset(self):
        self.rect.center = (self.x, self.y)  # Reset the position to the initial values
        self.__speed = 0  # Reset the speed
        self.__distance_traveled = 0  # Reset the distance traveled
        self.__start_time = False  # Reset the timer start flag
        self.__start_time = 0  # Reset the timer

    def move(self):
        self.rect.x += self.__speed  # Move the car horizontally based on the speed
        self.__distance_traveled += abs(self.__speed) / self.__screen_width * self.__screen_height  # Update the distance traveled

    def accelerate(self):
        if self.__speed < self.__max_speed:  # Check if the speed is less than the maximum speed
            self.__speed += self.__acceleration_rate  # Increase the speed by the acceleration rate

    def get_distance_traveled(self):
        return self.__distance_traveled  # Get the total distance traveled

    def start_timer(self):
        self.__start_time = time.time()  # Start the timer by setting the current time

    def stop_timer(self):
        end_time = time.time()  # Get the current time
        return end_time - self.__start_time  # Calculate and return the elapsed time

    def update(self):
        self.move()  # Update the position of the car
        self.accelerate()  # Accelerate the car
