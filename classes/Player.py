import pygame
# Importing pygame module



#TODO: add shooting method
#TODO: add sprinting key - shift
#TODO: Implement a method to check if the player is colliding with obstacles


class Player:

    """Player class
    Represents the player character.
    Attributes:
    x: int - the x-coordinate of the player
    y: int - the y-coordinate of the player
    health: int - the player's current health
    speed: int - the player's movement speed
    width: int - the player's width
    height: int - the player's height
    body: pygame.Rect - the player's rect object for collision detection
     
    Methods:
    move(self) - moves the player
    collide(self, obstacles) - checks if the player collides with any obstacle"""

    def __init__(self, x: int = 100, y: int = 100, health: int = 100) -> None:
        self.x: int = x
        self.y: int = y
        self.health: int = health

        self.speed: int = 2 

        self.width: int = 30
        self.height: int = 30

        self.body: pygame.Rect = pygame.Rect(self.x, self.y, self.width, self.height)
        # Initializing pygame rect object

        self.visible: bool = True

        self.down = False
        self.left = False
        self.right = False
        self.up = False



        