from classes.Enemy import Enemy
from classes.Player import Player
import pygame
import random

pygame.init()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.player = Player(x=400, y=300)
        self.enemies = [Enemy(x=random.randint(0, 800), y=random.randint(0, 600)) for _ in range(10)]



    def run(self):
        while True:
            self.clock.tick(60)  # Maintain 60 FPS frame rate
            self.handle_events()
            self.update_game_state()
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break

    def update_game_state(self):
        keys = pygame.key.get_pressed()

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
            enemy.simple_ai(self.player)
            enemy.move()  # Assuming `move` method in Enemy class

    def draw(self):
        self.screen.fill((0, 0, 0))
        for enemy in self.enemies:
            pygame.draw.rect(self.screen, (255, 0, 0), enemy.body)
        pygame.draw.rect(self.screen, (255, 0, 0), self.player.body)
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()