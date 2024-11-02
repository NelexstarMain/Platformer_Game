import numpy as np
import math
import pygame
import cv2


class Terrain:
    def __init__(self, x: int = 100, y: int = 100) -> None:
        self.x: int = x
        self.y: int = y

        # Grayscale intensity map (0-255)
        self.map = np.zeros((1280, 700), dtype=np.uint8)

        self.fading_distance: int = 350
        self.body = pygame.Rect(0, 0, 1280, 700)
        
        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 700))  # Create a display surface
        
        self.update_visibility()
        rotated_image = cv2.rotate(self.map, cv2.ROTATE_90_CLOCKWISE)
        cv2.imwrite('assets/zielony_obraz.png', rotated_image)  # Save the image
        self.image = pygame.image.load('assets/zielony_obraz.png', 'PNG')  # Load the image

    def update_visibility(self):
        for i in range(self.map.shape[0]):
            for j in range(self.map.shape[1]):
                enemy_position = pygame.Vector2(i, j)
                player_position = pygame.Vector2(self.body.centerx, self.body.centery)
                

                direction = (enemy_position - player_position)
                if 50 < direction.length() < self.fading_distance:  # Clamp at 1 to avoid exceeding max visibility direction.length() / self.fading_distance
                    color = int(255 * (1 - direction.length() / self.fading_distance)) / 1
                    self.map[i][j] = color
                if direction.length() < 50:
                    color = int(255 * (1 + direction.length() / 60)) / 1
                    self.map[i][j] = color


    def draw(self, player, screen: pygame.Surface):
        self.body.center = player.body.center
        screen.blit(self.image, self.body)
