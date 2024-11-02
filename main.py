import math
import pygame
import random

from classes.Enemy import Spawner
from classes.Player import Player, Bullet
from classes.Terrain import Terrain



# noqa: E1101
pygame.init()


pygame.mixer.music.load("assets/sounds/loop.mp3")
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(-1)

shot = pygame.mixer.Sound("assets/sounds/shot.mp3")
shot.set_volume(0.2)
hit = pygame.mixer.Sound("assets/sounds/hit.mp3")
hit.set_volume(0.2)
roar_1 = pygame.mixer.Sound("assets/sounds/roar_1.wav")
roar_1.set_volume(0.1)

roar_2 = pygame.mixer.Sound("assets/sounds/roar_2.wav")
roar_2.set_volume(0.1)
roar_3 = pygame.mixer.Sound("assets/sounds/roar_3.wav")
roar_3.set_volume(0.2)

class Game:
    """
    Main game class that handles the game loop, player input, game state updates, and drawing the game state.

    Attributes:
        screen (pygame.Surface): The game window surface.
        clock (pygame.time.Clock): The game clock for maintaining a constant frame rate.
        player (Player): The player object.
        terrain (Terrain): The terrain object.
        enemies (list): A list of enemy objects.
        spawners (list): A list of spawner objects.
        bullets (list): A list of bullet objects.

    Methods:
        __init__(self) -> None: Initializes the game window, clock, player, terrain, enemies, spawners, and bullets.
        run(self) -> None: The main game loop that runs the game.
        handle_events(self) -> None: Handles player input and updates the player's position and angle.
        update_game_state(self) -> None: Updates the game state by spawning enemies, handling enemy-bullet collisions, and updating the player's position based on held keys.
        draw(self) -> None: Draws the game state by filling the screen with a background color, drawing the terrain, enemies, bullets, and the player.
    """
    
    def __init__(self) -> None:
        self.screen: pygame.Surface = pygame.display.set_mode((1280, 700))
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.player: Player = Player(x=400, y=300)
        self.terrain: Terrain = Terrain()
        self.enemies: list = []
        self.spawners: list = [Spawner(x=random.randint(0, 1280), y=random.randint(0, 700)) for _ in range(4)]
        self.bullets: list = []


    def run(self) -> None:
        """Main game loop"""
        while True:
            self.player.shooting = False
            self.clock.tick(30)  # Maintain 60 FPS frame rate
            self.handle_events()
            self.update_game_state()
            self.draw()

    def handle_events(self):
        """Handle player input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            
            # Rotate player
            vector = pygame.Vector2(pygame.mouse.get_pos()) -  pygame.Vector2(self.player.body.center)
            self.player.angle = math.degrees(math.atan2(vector.y, vector.x))

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.player.shooting = True
                if vector.length() > 0:

                    # shot sound
                    shot.play()
                    
                    self.bullets.append(Bullet(self.player.rect_1.centerx, self.player.rect_1.centery, vector.normalize()))

    def update_game_state(self) -> None:
        """Update game state"""

        keys = pygame.key.get_pressed()
        for spawner in self.spawners:
            enemy = spawner.spawn(random.choice(["Zombie", "Zombie", "Zombie", "Pterodactylus", "Pterodactylus", "Ghost", "Madzia", "Madzia"]))
            if enemy is not None:
                self.enemies.append(enemy)

        if random.randint(0, 50) == 0:
            if random.randint(0, 3) == 0:
                roar_3.play()    
            else:
                roar_2.play()  

        for enemy in self.enemies:
            for bullet in self.bullets:

                if enemy.collided("body", bullet.body, False): # Bullet has collided with the enemy

                    enemy.beeing_hit()

                    hit.play()

                    roar_1.play()

                    if enemy.health <= 0:
                        self.enemies.remove(enemy)

                    bullet.update(True) # Bullet is deleted
  
        # Handle movement using held keys
        if keys[pygame.K_UP]:
            self.player.body.y -= self.player.speed

        if keys[pygame.K_DOWN]:
            self.player.body.y += self.player.speed

        if keys[pygame.K_LEFT]:
            self.player.body.x -= self.player.speed

        if keys[pygame.K_RIGHT]:
            self.player.body.x += self.player.speed

        # Implement enemy movement and AI logic here
        for enemy in self.enemies:
            
            enemy.simple_ai(self.player, self.enemies)

            enemy.move()  # Assuming `move` method in Enemy class

    def draw(self) -> None:
        """Draw game state"""

        self.screen.fill((0, 0, 0))
        
        self.terrain.draw(self.player, self.screen)

        for enemy in self.enemies:
            enemy.update_visibility(self.player)
            enemy.draw(self.screen)

        for bullet in self.bullets:
            bullet.move()
            bullet.update_visibility(self.player)
            bullet.draw(self.screen)
            bullet.update()
        
            
                
        self.player.draw(self.screen)
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()