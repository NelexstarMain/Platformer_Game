from classes.Enemy import Spawner
from classes.Player import Player

import pygame
import random

pygame.init()

pygame.mixer.music.load("assets/sounds/loop.mp3")
pygame.mixer.music.play(-1)

shot = pygame.mixer.Sound("assets/sounds/shot.mp3")
shot.set_volume(0.2)
hit = pygame.mixer.Sound("assets/sounds/hit.mp3")
hit.set_volume(0.2)
roar_1 = pygame.mixer.Sound("assets/sounds/roar_1.wav")
roar_1.set_volume(0.3)
roar_2 = pygame.mixer.Sound("assets/sounds/roar_2.wav")
roar_3 = pygame.mixer.Sound("assets/sounds/roar_3.wav")

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((1280, 700))
        self.clock = pygame.time.Clock()
        self.player = Player(x=400, y=300)
        self.enemies = []
        self.spawners = [Spawner(x=random.randint(0, 1280), y=random.randint(0, 700)) for _ in range(3)]
        self.bullets = []


    def run(self):
        while True:
            self.clock.tick(30)  # Maintain 60 FPS frame rate
            self.handle_events()
            self.update_game_state()
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                vector = pygame.Vector2(pygame.mouse.get_pos()) -  pygame.Vector2(self.player.body.center)
                if vector.length() > 0:
                    shot.play()
                    self.bullets.append(self.player.shooting(vector.normalize()))

    def update_game_state(self):
        keys = pygame.key.get_pressed()
        for spawner in self.spawners:
            enemy = spawner.spawn(random.choice(["Zombie", "Zombie", "Zombie", "Pterodactylus", "Pterodactylus", "Boss"]))
            if enemy is not None:
                self.enemies.append(enemy)

        for enemy in self.enemies:
            for bullet in self.bullets:
                if enemy.collided("body", [bullet]):  # Check collision between enemy and each bullet
                    enemy.beeing_hit()
                    hit.play()
                    roar_1.play()
                    if enemy.health <= 0:
                        self.enemies.remove(enemy)
                    self.bullets.remove(bullet)
                
                if bullet.body.x < 0 or bullet.body.x > 1280 or bullet.body.y < 0 or bullet.body.y > 700:
                    self.bullets.remove(bullet)
                
                if enemy.distance == 50:
                    roar_2.play()
                if enemy.distance == 400:
                    roar_3.play()

        # Handle movement using held keys
        if keys[pygame.K_UP]:
            self.player.body.y -= self.player.speed
        if keys[pygame.K_DOWN]:
            self.player.body.y += self.player.speed
        if keys[pygame.K_LEFT]:
            self.player.body.x -= self.player.speed
        if keys[pygame.K_RIGHT]:
            self.player.body.x += self.player.speed
        print(self.enemies)
        # Implement enemy movement and AI logic here
        for enemy in self.enemies:
            print(enemy)    
            enemy.simple_ai(self.player, self.enemies)
            enemy.move()  # Assuming `move` method in Enemy class

    def draw(self):
        self.screen.fill((0, 0, 0))
        for enemy in self.enemies:
            enemy.update_visibility(self.player)
            enemy.draw(self.screen)

        for bullet in self.bullets:

            bullet.move()
            bullet.update_visibility(self.player)
            bullet.draw(self.screen)
            
                
        pygame.draw.rect(self.screen, (255, 255, 0), self.player.body)
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()