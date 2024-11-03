from typing import List

class Settings:

    def __init__(self) -> None:
        self.screen_x: int = 1400
        self.screen_y: int = 800
        
        self.player_speed: int = 5
        self.bullet_speed: int = 10
        
        self.light_phases: List[List[int]] = [[50, -1, 1, 300], [0, 1, 2, 150]]
        
        
        
        
set = Settings()