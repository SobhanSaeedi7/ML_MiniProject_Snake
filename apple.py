import arcade
import random

class Apple(arcade.Sprite):
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        super().__init__('pics/apple.png')

        self.center_x = random.randint(16, SCREEN_WIDTH-16) // 8 * 8
        self.center_y = random.randint(16, SCREEN_HEIGHT-16) // 8 * 8
        self.width = 32
        self.height = 32

