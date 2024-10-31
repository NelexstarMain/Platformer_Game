import pygame


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

        self.speed: int = 5
        self.width: int = 30
        self.height: int = 30

        self.view_range: int = 100

        self.view: pygame.Rect = pygame.Rect(0, 0, self.view_range, self.view_range)
        self.body: pygame.Rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.visible: bool = True

        self.move_direction: int = 0


    def move(self) -> None:
        """Move enemy in the chosen direction"""
        match self.move_direction:
            case 0:
                self.x += self.speed # RIGHT
            case 1:
                self.x -= self.speed # LEFT
            case 2:
                self.y += self.speed # UP
            case 3:
                self.y -= self.speed # DOWN
            case _:
                raise ValueError("Invalid direction")
            
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

    def simple_ai(self, player) -> None:
        """Simple ai algorithm to decide which direction to move in
        when player is near
        walking in the direction of the player

        TODO: implement more complex ai algorithms
        TODO: Enemys teamwork"""

        if self.collided("view", [player]):

        player_position = pygame.Vector2(player.body.x, player.body.y)
        enemy_position = pygame.Vector2(self.body.x, self.body.y)

        direction = (player_position - enemy_position).normalize()
        direction *= self.speed

        if direction.x > direction.y:
            if direction.x > 0:
                self.move_direction = 0
            else:
                self.move_direction = 1
                
        else:
            if direction.y > 0:
                self.move_direction = 3
            else:
                self.move_direction = 2

