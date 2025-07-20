import pygame
import os


class Piece:
    def __init__(self, type, color):
        self.type = type      
        self.color = color    

    def __repr__(self):
        return f"{self.color[0].upper()}{self.type[0].upper()}"
    
    def get_image(self):
        # Placeholder for image retrieval logic
        image_path = f"assets/{self.color}_{self.type}.png"
        if not os.path.exists(image_path):
            image_path = "assets/NoImage.png"
        try:
            return pygame.image.load(image_path).convert_alpha()
        except pygame.error:
            return pygame.image.load("assets/NoImage.png").convert_alpha()