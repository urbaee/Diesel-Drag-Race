import pygame  # Importing the Pygame library for graphical functionality

class Button:
    """
    Class to create a clickable button in a Pygame application.
    
    Attributes:
        image: The image of the button, scaled appropriately.
        rect: The rectangle area of the button, used for positioning and collision detection.
    """
    def __init__(self, x, y, image, scale):
        """
        Initialize the button with a position, image, and scale factor.
        
        Parameters:
            x (int): The x-coordinate of the button's top-left corner.
            y (int): The y-coordinate of the button's top-left corner.
            image (pygame.Surface): The Pygame surface to use as the button image.
            scale (float): The scale factor to resize the button image.
        """
        if not isinstance(image, pygame.Surface):
            raise TypeError("image must be a Pygame Surface")
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
 
    def draw(self, screen):
        """
        Draw the button on the given screen.
        
        Parameters:
            screen (pygame.Surface): The Pygame surface to draw the button on.
        """
        screen.blit(self.image, self.rect)

    def is_clicked(self):
        """
        Check if the button is clicked (i.e., if the mouse is over the button and the left mouse button is pressed).
        
        Returns:
            bool: True if the button is clicked, False otherwise.
        """
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
            return True
        return False
