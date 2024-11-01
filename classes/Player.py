import pygame
import math
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

        self.ammo = 1000
    
    def shooting(self, vector):
        """Method to simulate shooting"""
        # TODO: implement shooting logic here
        if self.ammo > 0:
            self.ammo -= 1
            return Bullet(self.body.centerx, self.body.centery, vector)





class Bullet:
    def __init__(self, x, y, vector) -> None:
        self.x = x
        self.y = y
        self.speed = 10
        self.body = pygame.Rect(self.x, self.y, 2, 2)
        self.vector = vector
        self.fading_distance = 250
        self.alpha = 0

    def move(self) -> None:
        """Method to simulate bullet movement"""
        # TODO: implement bullet movement logic here
        self.body.x += self.vector.x * self.speed
        self.body.y += self.vector.y * self.speed

    def update_visibility(self, player):
        distance = math.sqrt((self.body.centerx - player.body.centerx)**2 + (self.body.centery - player.body.centery)**2)
        # Normalize the distance to a value between 0 and 1
        normalized_distance = min(distance / self.fading_distance, 1)  # Clamp at 1 to avoid exceeding max visibility
        # Calculate the alpha value based on normalized distance
        self.alpha = int(255 * (1 - normalized_distance))  # Higher distance => lower alpha



        
    def draw(self, screen):
        """Method to draw the bullet"""
        pygame.draw.rect(screen, (self.alpha, self.alpha, self.alpha), self.body)