import math
import pygame
from typing import Union
import random
1280
class Enemy:
    """Enemy class

    The Enemy class represents a generic enemy in the game. It has attributes such as health, speed, width, height, view range, and fading distance. It also has methods for moving, colliding with other objects, updating its visibility, and drawing itself on the screen.

    Attributes:
        x (int): The x-coordinate of the enemy.
        y (int): The y-coordinate of the enemy.
        health (int): The current health of the enemy.
        angle (int): The angle of the enemy's movement.
        speed (float): The speed at which the enemy moves.
        width (int): The width of the enemy's body.
        height (int): The height of the enemy's body.
        view_range (int): The range within which the enemy can see other objects.
        fading_distance (int): The distance at which the enemy's visibility starts to fade.
        body (pygame.Rect): A rectangle representing the position and size of the enemy on the screen.
        view (pygame.Rect): A rectangle representing the view range of the enemy.
        health_bar (pygame.Rect): A rectangle representing the health bar of the enemy.

    Methods:
        __init__(self, x: int = 100, y: int = 100) -> None:
            Initializes the Enemy object with the specified x and y coordinates.
            It also initializes the health, angle, speed, width, height, view range, and fading distance attributes.

        move(self) -> None:

            Updates the position of the enemy based on its angle and speed.

        collided(self, first_Rect: str, obstacles: Union[pygame.Rect, list], return_rect: bool) -> Union[bool, pygame.Rect]:

            Checks if the enemy collides with any obstacle.

        simple_ai(self, player, enemies) -> bool:

            Implements a simple AI algorithm to decide which direction to move in when the player is near.

        beeing_hit(self) -> None:

            Decreases the health of the enemy when it collides with the player.

        update_visibility(self, player) -> int:

            Updates the visibility of the enemy based on its distance from the player.

        draw(self, screen) -> None:

        Draws the enemy on the screen at its current position.
    """


    def __init__(self, x: int = 100, y: int = 100) -> None:
        self.x: int = x
        self.y: int = y
        self.health: int = 100
        self.angle: int = 0

        self.speed: float = 1
        self.width: int = 30
        self.height: int = 30
        self.fading_distance: int = 200
        self.alpha: int = 0

        self.distance: int = 0

        self.view_range: int = 900

        self.view: pygame.Rect = pygame.Rect(0, 0, self.view_range, self.view_range)
        self.body: pygame.Rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.health_bar: pygame.Rect = pygame.Rect(0, 0, self.health/5, 2)


    def move(self) -> None:

        self.body.x += math.cos(math.radians(self.angle)) * self.speed
        self.body.y += math.sin(math.radians(self.angle)) * self.speed    
                    
        self.view.center = self.body.center


    def collided(self, first_rect: str, obstacles: Union[pygame.Rect, list], return_rect: bool) -> Union[bool, pygame.Rect]:
        """Checks if the player collides with any obstacle"""

        if isinstance(obstacles, list):
            for obstacle in obstacles:
                if first_rect == "body":
                    if self.body.colliderect(obstacle.body):
                        if return_rect:
                            return True, obstacle.body
                        
                        return True
                    
                elif first_rect == "view":
                    if self.view.colliderect(obstacle.body):
                        if return_rect:
                            return True, obstacle.body
                        return True
                    
        elif isinstance(obstacles, pygame.Rect):
            if first_rect == "body":
                if self.body.colliderect(obstacles):
                    if return_rect:
                        return True, obstacles
                    return True
                
            elif first_rect == "view":
                if self.view.colliderect(obstacles):
                    if return_rect:
                        return True, obstacles
                    return True

        return False

    def simple_ai(self, player: pygame.Rect, enemies: list) -> None:
        """Simple ai algorithm to decide which direction to move in
        when player is near
        walking in the direction of the player

        TODO: implement more complex ai algorithms
        TODO: Enemys teamwork
        """

        if self.collided("view", player.body, False):

            player_position: pygame.Vector2 = pygame.Vector2(player.body.centerx, player.body.centery)
            enemy_position: pygame.Vector2 = pygame.Vector2(self.body.centerx, self.body.centery)

            direction = (player_position - enemy_position)

            for enemy in enemies:
                if self.collided("body", enemy, False):
                    enemy1_position = pygame.Vector2(enemy.body.centerx, enemy.body.centery)
                    enemy2_position = pygame.Vector2(self.body.centerx, self.body.centery)

                    if enemy1_position.x < enemy2_position.x:
                        direction.x = max(0, direction.x)

                    elif enemy1_position.x > enemy2_position.x:
                        direction.x = min(self.view_range, direction.x)

                    if enemy1_position.y < enemy2_position.y:
                        direction.y = max(0, direction.y)

                    elif enemy1_position.y > enemy2_position.y:
                        direction.y = min(self.view_range, direction.y)

            direction += pygame.Vector2(random.randint(-10, 10), random.randint(-10, 10))
            direction *= self.speed

            angle = math.degrees(math.atan2(direction.y + random.randint(-50, 50), direction.x + random.randint(-50, 50)))

            self.angle = angle

        else:
            self.angle += 10 # Do cirlesh movement

    def beeing_hit(self) -> None:
        """When the player collides with the enemy"""
        self.health -= 50
    
    def update_visibility(self, player) -> int:
        """Updates the visibility of the enemy"""

        distance = math.sqrt((self.body.centerx - player.body.centerx)**2 + (self.body.centery - player.body.centery)**2)
        # Normalize the distance to a value between 0 and 1
        normalized_distance = min(distance / self.fading_distance, 1)
        
        self.distance = distance  # Clamp at 1 to avoid exceeding max visibility
        # Calculate the alpha value based on normalized distance
        self.alpha = int(255 * (1 - normalized_distance)) / 2  # Higher distance => lower alpha

        # Clamp alpha between 0 and 255
        return self.alpha
    
    def draw(self, screen) -> None:
        """Draws the enemy on the screen"""
        pygame.draw.rect(screen, (self.alpha, 0, self.alpha/2), self.body)

        self.health_bar.x = self.body.x 

        self.health_bar.y = self.body.y - 10

        self.health_bar.width = self.health / 5

        pygame.draw.rect(screen, (0, self.alpha, 0), self.health_bar)



class Zombie(Enemy):
    """Zombie class"""
    def __init__(self, x: int = 100, y: int = 100) -> None:
        super().__init__(x, y)
        self.health: int = 100
        self.speed: int = 3
        self.width: int = 45
        self.height: int = 45
        self.view_range: int = 900
        self.fading_distance: int = 350
        self.body = pygame.Rect(self.x, self.y, self.width, self.height)

class Pterodactylus(Enemy):
    """Pterodactylus class"""
    def __init__(self, x: int = 100, y: int = 100) -> None:
        super().__init__(x, y)
        self.health: int = 50
        self.speed: int = 5
        self.width: int = 30
        self.height: int = 30
        self.view_range: int = 400
        self.fading_distance: int = 350
        self.body = pygame.Rect(self.x, self.y, self.width, self.height)

class Ghost(Enemy):
    """Ghost class"""
    def __init__(self, x: int = 100, y: int = 100) -> None:
        super().__init__(x, y)
        self.health: int = 25
        self.speed: int = 6
        self.width: int = 30
        self.height: int = 30
        self.view_range: int = 600
        self.fading_distance: int = 350
        self.body = pygame.Rect(self.x, self.y, self.width, self.height)

class Madzia(Enemy):
    """Madzia class"""
    def __init__(self, x: int = 100, y: int = 100) -> None:
        super().__init__(x, y)
        self.health: int = 200
        self.speed: int = 5
        self.width: int = 15
        self.height: int = 15
        self.view_range: int = 500
        self.fading_distance: int = 350
        self.body = pygame.Rect(self.x, self.y, self.width, self.height)



class Spawner:
    """Spawner class""
    The Spawner class represents a location where enemies can be spawned. It has attributes such as health, body, and a working flag. It also has a method for spawning enemies at its location.

    Attributes:
        x (int): The x-coordinate of the spawner.
        y (int): The y-coordinate of the spawner.
        health (int): The current health of the spawner. If the health is 0, the spawner will not spawn any enemies.
        body (pygame.Rect): A rectangle representing the position and size of the spawner on the screen.
        working (bool): A flag indicating whether the spawner is currently working or not. If the working flag is False, the spawner will not spawn any enemies.

    Methods:
        __init__(self, x: int = 100, y: int = 100) -> None:
            Initializes the Spawner object with the specified x and y coordinates.
            It also initializes the health and body attributes.
    
        spawn(self, name: str = "Zombie") -> Union[pygame.Rect, None]:
            Spawns an enemy at the spawner's location
            If the working flag is True, it will spawn an enemy at the spawner's location. The name parameter determines the type of enemy to be spawned.
            If the health attribute of the spawner is 0, it will not spawn any enemies.
            If the name parameter is not provided, the default value is "Zombie".
            If the working flag is False, it will return None.
    """
    
    def __init__(self, x: int = 100, y: int = 100) -> None:
        self.x: int = x
        self.y: int = y
     
        self.health: int = 50
        self.body: pygame.Rect = pygame.Rect(self.x, self.y, 30, 30)
        self.working: bool = True

    
    def spawn(self, name: str = "Zombie") -> Union[pygame.Rect, None]:
        """Spawns an enemy at the spawner's location"""
        if self.working:
            if random.randint(0, 100) == 0:
                if self.health > 0:

                    if name == "Zombie":
                        enemy = Zombie(self.x, self.y)
                        self.health -= 5
                        return enemy
                    
                    elif name == "Pterodactylus":
                        enemy = Pterodactylus(self.x, self.y)
                        self.health -= 5
                        return enemy
                    
                    elif name == "Ghost":
                        enemy = Ghost(self.x, self.y)
                        self.health -= 5
                        return enemy
                    
                    elif name == "Madzia":
                        enemy = Madzia(self.x, self.y)
                        self.health -= 5
                        return enemy
                    
                    
                    
        else:
            return None




