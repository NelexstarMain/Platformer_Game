import numpy as np
import pygame
import cv2

from settings import set


class Terrain:
    """
    The Terrain class represents a 2D terrain with a grayscale intensity map.
    It is used to draw the terrain on the screen and update its visibility based on the distance from the player.

    Attributes:
        x (int): The x-coordinate of the terrain.
        y (int): The y-coordinate of the terrain.
        map (numpy.ndarray): A 2D grayscale intensity map representing the terrain, with dimensions (1280, 700) and values ranging from 0 to 255.
        fading_distance (int): The distance at which the terrain's visibility starts to fade.
        body (pygame.Rect): A rectangle representing the position and size of the terrain on the screen.

    Methods:
        __init__(self, x: int = 100, y: int = 100) -> None:
            Initializes the Terrain object with the specified x and y coordinates.
            It also initializes the grayscale intensity map, fading distance, and the Pygame rectangle.

        update_visibility(self) -> None:
            Updates the terrain's visibility based on the distance from the player.
            It iterates over every pixel in the map and adjusts the visibility based on the distance from the player's position.

        draw(self, player, screen: pygame.Surface) -> None:
            Draws the terrain on the screen at the specified player's position.
            It sets the position of the player and blits the terrain image onto the screen.
    """
    def __init__(self, x: int = 100, y: int = 100) -> None:
        self.x: int = x
        self.y: int = y

        # Grayscale intensity map (0-255)
        self.map: np.ndarray = np.zeros((1280, 700), dtype=np.uint8)

        self.fading_distance: int = 350
        self.body = pygame.Rect(0, 0, 1280, 700)
        
        # Initialize Pygame
        # noqa: E1101
        pygame.init()

        
        self.update_visibility()

        # noqa: E1101
        rotated_image: np.ndarray = cv2.rotate(self.map, cv2.ROTATE_90_CLOCKWISE)

        # noqa: E1101
        cv2.imwrite('assets/image.png', rotated_image)  # Save the image

        self.image: pygame.Surface = pygame.image.load('assets/image.png', 'PNG')  # Load the image

    def update_visibility(self) -> None:
        """Updates terrain visibility based on distance from player"""
        # Iterate over every pixel in the map
        # self.map.shape[0] == 1280
        # self.map.shape[1] == 700


        for i in range(self.map.shape[0]):
            # self.map.shape[0] == 1280
            for j in range(self.map.shape[1]):
                # self.map.shape[1] == 700

                enemy_position: pygame.Vector2 = pygame.Vector2(i, j)
                player_position: pygame.Vector2 = pygame.Vector2(self.body.centerx, self.body.centery)
                

                direction_to_pixel = (enemy_position - player_position)

                # if 50 < direction.length() < self.fading_distance:
                #     # Normalize the distance to a value between 0 and 1
                #     color = int(255 * (1 - direction.length() / self.fading_distance)) / 1
                #     # Clamp at 255 to avoid exceeding max visibility
                #     self.map[i][j] = color
                
                for phase in set.light_phases:
                    lenght = phase[0]
                    direction = phase[1]
                    darknes = phase[2]
                    fading_distance = phase[3]
                    
                    if lenght < direction_to_pixel.length() < fading_distance:
                        color = int(255 * (direction * direction_to_pixel.length() / fading_distance)) / darknes
                        self.map[i][j] = color


    def draw(self, player, screen: pygame.Surface) -> None:
        """Draws the terrain on the screen"""
        
        # Seting the position of the player
        self.body.center = player.body.center

        # blit the image to the screen
        screen.blit(self.image, self.body)
