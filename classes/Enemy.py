import math
import pygame
import random

class Enemy:
    """Enemy class



    will use simple ai algorithm
    to decide where to move
    and what to do
    when seeing the player move in the direction of the player 
    but when you see other enemy atack from other side of Player"""

    def __init__(self, x: int = 100, y: int = 100, health: int = 100) -> None:
        self.x: int = x
        self.y: int = y
        self.health: int = health
        self.angle: int = 0

        self.speed: int = 1
        self.width: int = 30
        self.height: int = 30

        self.view_range: int = 400

        self.view: pygame.Rect = pygame.Rect(0, 0, self.view_range, self.view_range)
        self.body: pygame.Rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.visible: bool = True



    def move(self) -> None:

        self.body.x += math.cos(math.radians(self.angle)) * self.speed
        self.body.y += math.sin(math.radians(self.angle)) * self.speed    
                    
        self.view.center = self.body.center


    def collided(self, first_Rect: str = "body", obstacles: list = []) -> bool:
        """Checks if the player collides with any obstacle"""
        
        for obstacle in obstacles:
            if first_Rect == "body":
                if self.body.colliderect(obstacle.body):
                    return True
                return False
            
            if first_Rect == "view":
                if self.view.colliderect(obstacle.body):
                    return True
                return False

    def simple_ai(self, player) -> bool:
        """Simple ai algorithm to decide which direction to move in
        when player is near
        walking in the direction of the player

        TODO: implement more complex ai algorithms
        TODO: Enemys teamwork
        """

        if self.collided("view", [player]):

            player_position = pygame.Vector2(player.body.centerx, player.body.centery)
            enemy_position = pygame.Vector2(self.body.centerx, self.body.centery)

            direction = (player_position - enemy_position)
            print(direction)
            direction *= self.speed

            angle = math.degrees(math.atan2(direction.y + random.randint(-50, 50), direction.x + random.randint(-50, 50)))

            self.angle = angle

        else:
            self.angle += 10

