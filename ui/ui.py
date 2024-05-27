import sys
import pygame
from abc import ABC, abstractmethod

from button import Button
from scripts.util import get_font, load_image

# Kelas abstrak untuk komponen UI
class UIComponent(ABC):
    @abstractmethod
    def render(self, screen):
        pass
    
    @abstractmethod
    def handle_event(self, event):
        pass