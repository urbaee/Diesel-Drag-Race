import sys
import pygame
import os

BASE_IMG_PATH = 'images/'

def load_image(path, color_key=(0,0,0), convert_alpha=False, is_color_key=True):
    if convert_alpha:
        img = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()
    else:
        img = pygame.image.load(BASE_IMG_PATH + path).convert()
    
    if is_color_key:
        img.set_colorkey(color_key) 

    return img


def load_images(path, is_color_key=True, convert_alpha=False):
    images = []
    
    # it's not work for linux!
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name, is_color_key=is_color_key, convert_alpha=convert_alpha))
        
    return images

def get_font(size):
        return pygame.font.Font("textfont/Minecraft.ttf", size)

def quit_game():
    pygame.quit()
    sys.exit()