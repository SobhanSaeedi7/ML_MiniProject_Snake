import arcade

from snake import Snake
from apple import Apple


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
SCREEN_TITLE = "Turn and Move Example"
     

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, resizable=True)
        arcade.set_background_color(arcade.color.SAND)

        self.snake = Snake(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.apple = Apple(SCREEN_WIDTH, SCREEN_HEIGHT)

    def on_draw(self):
        arcade.start_render()

        self.snake.draw()
        self.apple.draw()
        
    def on_update(self, delta_time):
        self.snake.on_update(delta_time)
        self.apple.on_update()

        if arcade.check_for_collision(self.snake, self.apple):
            self.snake.eat()
            self.apple = Apple(SCREEN_WIDTH, SCREEN_HEIGHT)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.snake.change_x = -1
            self.snake.change_y = 0
    
        elif key == arcade.key.RIGHT:
            self.snake.change_x = 1
            self.snake.change_y = 0

        elif key == arcade.key.UP:
            self.snake.change_x = 0
            self.snake.change_y = 1
    
        elif key == arcade.key.DOWN:
            self.snake.change_x = 0
            self.snake.change_y = -1
    

if __name__ == "__main__":
    window = MyGame()
    arcade.run()