import arcade
import pandas as pd


from snake import Snake
from apple import Apple


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
SCREEN_TITLE = "Turn and Move Example"
     

#  Main application class
class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)
        arcade.set_background_color(arcade.color.SAND)

        self.snake = Snake(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.apple = Apple(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.dataset = []
        # self.set_update_rate(1/30)

    def on_draw(self):
        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        # Call draw() on all your sprite lists below
        self.snake.draw()
        self.apple.draw()
        
    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        """
        self.snake.on_update(delta_time)
        self.apple.on_update()

        if arcade.check_for_collision(self.snake, self.apple):
            self.snake.eat()
            self.apple = Apple(SCREEN_WIDTH, SCREEN_HEIGHT)

        if self.snake.center_y > self.apple.center_y:
            self.snake.change_x = 0
            self.snake.change_y = -1
        elif self.snake.center_y < self.apple.center_y:
            self.snake.change_x = 0
            self.snake.change_y = 1
        elif self.snake.center_x > self.apple.center_x:
            self.snake.change_x = -1
            self.snake.change_y = 0
        elif self.snake.center_x < self.apple.center_x:
            self.snake.change_x = 1
            self.snake.change_y = 0

    def on_key_release(self, key, modifiers):
        if symbol == arcade.key.Q:
            df = pd.DataFrame(self.dataset)
            df.to_csv('dataset.csv', index=False)
    

if __name__ == "__main__":
    window = MyGame()
    arcade.run()