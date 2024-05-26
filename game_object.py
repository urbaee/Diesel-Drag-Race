# game_object.py

from abc import ABC, abstractmethod

class GameObject(ABC):
    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def move(self):
        pass

    @abstractmethod
    def accelerate(self):
        pass

    @abstractmethod
    def start_timer(self):
        pass

    @abstractmethod
    def stop_timer(self):
        pass

class Sprite(GameObject):
    def __init__(self):
        super().__init__()
        self.image = None
        self.rect = None

    def draw(self, screen):
        if self.image and self.rect:
            screen.blit(self.image, self.rect)  # Ensure image is a Surface and rect is a Rect
