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

    def __init__(self, x: int = 100, y: int = 100) -> None:
        self.x: int = x
        self.y: int = y
        self.health: int = 100
        self.angle: int = 0

        self.speed: float = 1
        self.width: int = 30
        self.height: int = 30
        self.fading_distance: int = 200
        self.alpha = 0

        self.distance = 0

        self.view_range: int = 900

        self.view: pygame.Rect = pygame.Rect(0, 0, self.view_range, self.view_range)
        self.body: pygame.Rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.health_bar: pygame.Rect = pygame.Rect(0, 0, self.health/5, 2)


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

    def simple_ai(self, player, enemies) -> bool:
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

            for enemy in enemies:
                if self.collided("body", [enemy]):
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
            # print(direction.length())
            # if direction.length() <= 510:
            #     self.visible = direction.length() / 2
            # else:
            #     self.visible = 255

            angle = math.degrees(math.atan2(direction.y + random.randint(-50, 50), direction.x + random.randint(-50, 50)))

            self.angle = angle

        else:
            self.angle += 10

    def beeing_hit(self) -> None:
        """When the player collides with the enemy"""
        self.health -= 50
        self.alpha = 255
    
    def update_visibility(self, player):
        distance = math.sqrt((self.body.centerx - player.body.centerx)**2 + (self.body.centery - player.body.centery)**2)
        # Normalize the distance to a value between 0 and 1
        normalized_distance = min(distance / self.fading_distance, 1)
        
        self.distance = distance  # Clamp at 1 to avoid exceeding max visibility
        print(self.distance)
        # Calculate the alpha value based on normalized distance
        self.alpha = int(255 * (1 - normalized_distance)) / 6  # Higher distance => lower alpha
    
    def draw(self, screen) -> None:
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
        self.fading_distance: int = 200
        self.body = pygame.Rect(self.x, self.y, self.width, self.height)

class Pterodactylus(Enemy):
    """Pterodactylus class"""
    def __init__(self, x: int = 100, y: int = 100) -> None:
        super().__init__(x, y)
        self.health: int = 50
        self.speed: int = 4
        self.width: int = 30
        self.height: int = 30
        self.view_range: int = 400
        self.fading_distance: int = 200
        self.body = pygame.Rect(self.x, self.y, self.width, self.height)

class Ghost(Enemy):
    """Ghost class"""
    def __init__(self, x: int = 100, y: int = 100) -> None:
        super().__init__(x, y)
        self.health: int = 25
        self.speed: int = 3
        self.width: int = 30
        self.height: int = 30
        self.view_range: int = 600
        self.fading_distance: int = 200
        self.body = pygame.Rect(self.x, self.y, self.width, self.height)



class Spawner:
    """Spawner class"""
    def __init__(self, x: int = 100, y: int = 100) -> None:
        self.x: int = x
        self.y: int = y
     
        self.health: int = 20
        self.body = pygame.Rect(self.x, self.y, 30, 30)
        self.working = True

    
    def spawn(self, name: str) -> pygame.Rect:
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
                    
                    
                    
        else:
            return None




