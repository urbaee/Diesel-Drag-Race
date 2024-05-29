from abc import ABC, abstractmethod  # Importing abstract base class utilities

class GameObject(ABC):
    @abstractmethod
    def update(self):
        pass  # Abstract method for updating the game object

    @abstractmethod
    def move(self):
        pass  # Abstract method for moving the game object

    @abstractmethod
    def accelerate(self):
        pass  # Abstract method for accelerating the game object

    @abstractmethod
    def start_timer(self):
        pass  # Abstract method for starting a timer

    @abstractmethod
    def stop_timer(self):
        pass  # Abstract method for stopping a timer

class Sprite(GameObject):
    def __init__(self):
        super().__init__()
        self.image = None  # Placeholder for the image of the sprite
        self.rect = None  # Placeholder for the rectangle area of the sprite

    def draw(self, screen):
        if self.image and self.rect:
            screen.blit(self.image, self.rect)  # Draw the image at the rect position on the screen
