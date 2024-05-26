# player.py

import pygame
import time
from game_object import Sprite

class Player(Sprite):
    def __init__(self, config, x, y, screen_width, screen_height):
        super().__init__()
        self.x = x
        self.y = y
        self.__char_type = config['char_type']
        self.__speed = config['initial_speed']
        self.__max_speed = config['max_speed']
        self.__acceleration_rate = config['acceleration_rate']
        img = pygame.image.load(config['image_path'])
        self.image = pygame.transform.scale(img, (int(img.get_width() * config['scale']), int(img.get_height() * config['scale'])))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.__distance_traveled = 0
        self.__screen_width = screen_width
        self.__screen_height = screen_height
        self.__start_time = None
        self.game_stop = False

    def set_speed(self, speed):
        self.__speed = speed

    def get_speed(self):
        return self.__speed
    
    def set_max_speed(self, max_speed):
        self.__max_speed = max_speed

    def get_max_speed(self):
        return self.__max_speed

    def set_acceleration_rate(self, acceleration_rate):
        self.__acceleration_rate = acceleration_rate

    def get_acceleration_rate(self):
        return self.__acceleration_rate       

    def reset(self):
        self.rect.center = (self.x, self.y)
        self.__speed = 0
        self.__distance_traveled = 0
        self.__start_time = False
        self.__start_time = 0

    def move(self):
        self.rect.x += self.__speed
        self.__distance_traveled += abs(self.__speed) / self.__screen_width * self.__screen_height

    def accelerate(self):
        if self.__speed < self.__max_speed:
            self.__speed += self.__acceleration_rate

    def get_distance_traveled(self):
        return self.__distance_traveled

    def start_timer(self):
        self.__start_time = time.time()

    def stop_timer(self):
        end_time = time.time()
        return end_time - self.__start_time

    def update(self):
        self.move()
        self.accelerate()
