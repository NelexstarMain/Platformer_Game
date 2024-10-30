import pygame


class Enemy:
    """Enemy class
    will use simple ai algorithm
    to decide where to move
    and what to do
    TODO: implement a method to check if the player is colliding with obstacles
    TODO: create ai algorithm 
    when seeing the player move in the direction of the player 
    but when you see other enemy atack from other side of Player"""

    def __init__(self, x: int = 100, y: int = 100, health: int = 100) -> None:
        self.x: int = x
        self.y: int = y
        self.health: int = health
        self.angle: int = 0

        self.speed: int = 5
        self.width: int = 30
        self.height: int = 30
        self.body: pygame.Rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.visible: bool = True


    def move(self) -> None:
        """Move enemy in the chosen direction"""
        pass


