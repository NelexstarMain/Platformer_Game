import pygame
import math
from typing import Union, Type



class Bullet:
    """
    Bullet class
    --------------------------------------------------------------------------------
    Represents a bullet fired by the player.

    Attributes:
        x (int): Initial x-coordinate of the bullet.
        y (int): Initial y-coordinate of the bullet.
        speed (int): Speed of the bullet.
        body (pygame.Rect): Rectangle representing the bullet's body.
        vector (pygame.Vector2): Direction vector of the bullet.
        fading_distance (int): Distance at which the bullet will start to fade.
        alpha (int): Transparency level of the bullet.

    Methods:
        __init__(x: int, y: int, vector: pygame.Vector2) -> None:
            Initializes the bullet object with the specified attributes.

        move() -> None:
            Method to simulate bullet movement. The bullet moves in the x and y axes based on its vector.

        update_visibility(player: pygame.Rect) -> None:
            Updates bullet visibility based on distance from player. The bullet will be fully visible when it is at the fading distance, and will be completely transparent when it is at 0 distance. This allows for smooth fading effect when the player is close to the bullet.

        update(colided: bool = False) -> None:
            Updates the bullet's state. Checks if the bullet has left the screen or has collided with the Enemy, and removes the bullet if either condition is met.

        draw(screen) -> None:
            Method to draw the bullet on the screen. Draws a rectangle representing the bullet with a semi-transparent color based on its distance from the player.
    """

    def __init__(self, x, y, vector) -> None:
        self.x: int = x
        self.y: int = y
        self.speed: int = 10
        self.body: pygame.Rect = pygame.Rect(self.x, self.y, 2, 2)
        self.vector: pygame.Vector2 = vector
        self.fading_distance: int = 250
        self.alpha: int = 0

    def move(self) -> None:
        """Method to simulate bullet movement"""

        # Bullets moves in the x axis
        self.body.x += self.vector.x * self.speed

        # Bullets moves in the y axis
        self.body.y += self.vector.y * self.speed

    def update_visibility(self, player: pygame.Rect) -> None:
        """Updates bullet visibility based on distance from player"""

        # Calculate the distance between the bullet and the player and normalize it to a value between 0 and 1
        # The bullet will be fully visible when it is at the fading distance, and will be completely transparent when it is at 0 distance.
        # This allows for smooth fading effect when the player is close to the bullet.

        distance = math.sqrt((self.body.centerx - player.body.centerx) ** 2 + (self.body.centery - player.body.centery) ** 2)
        normalized_distance = min(distance / self.fading_distance, 1)  # Clamp at 1
        self.alpha = int(255 * (1 - normalized_distance))
    
    def update(self, colided: bool = False) -> None:
        """Updates the bullet's state"""

        # Check if the bullet has left the screen 
        if self.body.x < 0 or self.body.x > 1280 or self.body.y < 0 or self.body.y > 700:
            del self

        # Check if the bullet has collided with the Enemy
        if colided:
            del self


    def draw(self, screen):
        """Method to draw the bullet"""
        pygame.draw.rect(screen, (self.alpha, 0, 0), self.body)



class Player:

    """
    Player class
    --------------------------------------------------------------------------------
    Represents the player character.

    Attributes:
        x (int): Initial x-coordinate of the player.
        y (int): Initial y-coordinate of the player.
        health (int): Initial health of the player.
        speed (int): Speed of the player.
        photo_1 (pygame.Surface): Image of the player.
        width (int): Width of the player's body.
        height (int): Height of the player's body.
        angle (int): Current facing angle of the player.
        body (pygame.Rect): Rectangle representing the player's body.
        visible (bool): Flag indicating whether the player is visible.
        shooting (bool): Flag indicating whether the player is currently shooting.
        rect_1 (pygame.Rect): Rectangle representing the player's image.
        ammo (int): Number of ammo the player has.

    Methods:
        __init__(x: int = 100, y: int = 100, health: int = 100) -> None:
            Initializes the player object with the specified attributes.

        shooting(self, vector) -> None:
            Method to simulate shooting. If the player has enough ammo, it will decrease the ammo count and return a Bullet object.

        draw(self, screen) -> None:
            Method to draw the player on the screen. It rotates the player's image based on the current angle and draws it on the specified position.

        update_visibility(self, player) -> None:
            Updates the bullet's visibility based on the distance from the player.

        draw(self, screen) -> None:
            Method to draw the bullet on the screen. It draws a rectangle representing the bullet with a semi-transparent color based on its distance from the player.
    """

    def __init__(self, x: int = 100, y: int = 100, health: int = 100) -> None:
        self.x = x
        self.y = y

        # Player health
        self.health: int = health

        # Player speed
        self.speed: int = 3

        # Player angle
        self.angle: int = 0 # Current facing angle

        # Player width
        self.width: int = 45

        # Player height
        self.height: int = 45

        # Load player image
        self.photo_1 = pygame.image.load("assets/player/player.png")

        # Player pygame rect
        self.body: pygame.Rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # if the player is visible
        self.visible: bool = True

        # if the player is shooting
        self.shooting: bool = False

        # Player rect image
        self.rect_1: pygame.Rect = None

        # Player ammo
        self.ammo: int = 1000

    def shoot(self, vector: pygame.Vector2) -> Union[Type[Bullet], None]:
        """Method to simulate shooting"""
        if self.ammo > 0:
            self.ammo -= 1
            # Create a bullet object
            return Bullet(self.body.centerx, self.body.centery, vector)
        
        # If the player doesn't have enough ammo, return None
        return None

    def draw(self, screen: pygame.Surface) -> None:
        """Method to draw the player"""
        # Rotate image based on current angle
        rotated_photo_1 = pygame.transform.rotate(self.photo_1, 90 - self.angle + 180) 

        self.rect_1 = rotated_photo_1.get_rect(center=rotated_photo_1.get_rect(center=self.body.center).center)
        # Draw appropriate image based on shooting state

        screen.blit(rotated_photo_1, self.rect_1)


