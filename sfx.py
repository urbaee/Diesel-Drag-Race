import os
import pygame

BASE_SFX_PATH = "audio/"  # Base path for sound effect files

class SFXController:
    def __init__(self):
        self.__sfx_list = {}  # Dictionary to store sound effects
        self.__last_sfx_vol = {}  # Dictionary to store the last volume settings for sound effects
        self.muted = False  # Flag to indicate if all sound effects are muted
        pygame.mixer.init()  # Initialize the Pygame mixer
        
    def add_sfx(self, sfx_name, path, volume=1.0):
        # check file
        sfx_path = BASE_SFX_PATH + str(path)  # Construct the full file path
        if os.path.isfile(sfx_path):  # Check if the file exists
            self.__sfx_list[sfx_name] = pygame.mixer.Sound(sfx_path)  # Load the sound effect
            self.set_volume(sfx_name, volume)  # Set the volume for the sound effect
        else:
            raise FileNotFoundError(f"File {sfx_path} not found!")  # Raise an error if the file doesn't exist
        
    def set_volume(self, sfx_name, volume, set_last_vol=True):
        if set_last_vol:
            self.__last_sfx_vol[sfx_name] = volume  # Store the volume setting
        self.__sfx_list[sfx_name].set_volume(volume)  # Set the volume for the sound effect
    
    def play(self, sfx_name, loop=False):
        if sfx_name in self.__sfx_list:  # Check if the sound effect exists
            if loop:
                self.__sfx_list[sfx_name].play(loops=-1)  # Play the sound effect in a loop
            else:
                self.__sfx_list[sfx_name].play(loops=0)  # Play the sound effect once
        else:
            raise Exception(f"{sfx_name} does not exist in sfx list!")  # Raise an error if the sound effect doesn't exist
        
    def stop(self, sfx_name):
        if sfx_name in self.__sfx_list:  # Check if the sound effect exists
            self.__sfx_list[sfx_name].stop()  # Stop the sound effect
        else:
            raise Exception(f"{sfx_name} does not exist in sfx list!")  # Raise an error if the sound effect doesn't exist
        
    def mute(self):
        if self.muted:
            for sfx_name, _ in self.__sfx_list.items():
                self.set_volume(sfx_name, self.__last_sfx_vol[sfx_name])  # Restore the volume settings
            self.muted = False  # Update the mute flag
        else:
            for sfx_name, _ in self.__sfx_list.items():
                    self.set_volume(sfx_name, 0, set_last_vol=False)  # Set the volume to 0
            self.muted = True  # Update the mute flag

    # New mute function for individual sound effects
    def mute(self, sfx_name):
        if sfx_name in self.__sfx_list:
            self.set_volume(sfx_name, 0, set_last_vol=False)  # Set the volume to 0
        else:
            raise Exception(f"{sfx_name} does not exist in sfx list!")  # Raise an error if the sound effect doesn't exist

    def unmute(self, sfx_name):
        if sfx_name in self.__sfx_list:
            self.set_volume(sfx_name, self.__last_sfx_vol[sfx_name])  # Restore the volume setting
        else:
            raise Exception(f"{sfx_name} does not exist in sfx list!")  # Raise an error if the sound effect doesn't exist
