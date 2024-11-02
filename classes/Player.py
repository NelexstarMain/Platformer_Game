import pygame
import math


class Player:

    """Player class
    Represents the player character.
    """

    def __init__(self, x: int = 100, y: int = 100, health: int = 100) -> None:
        self.x = x
        self.y = y
        self.health = health

        self.speed = 3

        self.photo_1 = pygame.image.load("assets/player/player.png")


        self.width = 45
        self.height = 45
        self.angle = 0  # Current facing angle

        self.body = pygame.Rect(self.x, self.y, self.width, self.height)

        self.visible = True
        self.shooting = False

        self.rect_1: pygame.Rect = None


        self.ammo = 1000

    def shooting(self, vector):
        """Method to simulate shooting"""
        if self.ammo > 0:
            self.ammo -= 1
            # Create a bullet object
            return Bullet(self.body.centerx, self.body.centery, vector)
        else:
            # Handle out of ammo scenario (e.g., print message)
            return None

    def draw(self, screen):
        """Method to draw the player"""
        # Rotate image based on current angle
        rotated_photo_1 = pygame.transform.rotate(self.photo_1, 90 - self.angle + 180) 

        self.rect_1 = rotated_photo_1.get_rect(center=rotated_photo_1.get_rect(center=self.body.center).center)
        # Draw appropriate image based on shooting state

        screen.blit(rotated_photo_1, self.rect_1)



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
        self.body.x += self.vector.x * self.speed
        self.body.y += self.vector.y * self.speed

    def update_visibility(self, player):
        """Updates bullet visibility based on distance from player"""
        distance = math.sqrt((self.body.centerx - player.body.centerx) ** 2 + (self.body.centery - player.body.centery) ** 2)
        normalized_distance = min(distance / self.fading_distance, 1)  # Clamp at 1
        self.alpha = int(255 * (1 - normalized_distance))



 
    def draw(self, screen):
        """Method to draw the bullet"""
        pygame.draw.rect(screen, (self.alpha, 0, 0), self.body)