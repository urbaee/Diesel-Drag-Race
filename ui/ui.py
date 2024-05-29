import sys  # Importing the sys module for system-specific parameters and functions
import pygame  # Importing the pygame module for game development

from abc import ABC, abstractmethod  # Importing ABC and abstractmethod to create abstract base classes

from button import Button  # Importing the Button class from the button module
from scripts.util import get_font, load_image  # Importing utility functions to get fonts and load images

# Abstract class for UI components
class UIComponent(ABC):  # Defining the UIComponent abstract class, inheriting from ABC (Abstract Base Class)
    @abstractmethod  # Decorator indicating the following method must be implemented in subclasses
    def render(self, screen):
        pass  # Abstract method render, must be implemented by subclasses
    
    @abstractmethod  # Decorator indicating the following method must be implemented in subclasses
    def handle_event(self, event):
        pass  # Abstract method handle_event, must be implemented by subclasses
