import tensorflow as tf
import arcade

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
        self.model =  tf.keras.models.load_model('model.h5')
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

        data = {}

        if self.snake.center_x == self.apple.center_x and self.snake.center_y < self.apple.center_y:
            data['au'] = 1
            data['ar'] = 0
            data['ad'] = 0
            data['al'] = 0
        elif self.snake.center_x == self.apple.center_x and self.snake.center_y > self.apple.center_y:
            data['au'] = 0
            data['ar'] = 0
            data['ad'] = 1
            data['al'] = 0
        elif self.snake.center_x < self.apple.center_x and self.snake.center_y == self.apple.center_y:
            data['au'] = 0
            data['ar'] = 1
            data['ad'] = 0
            data['al'] = 0
        elif self.snake.center_x > self.apple.center_x and self.snake.center_y == self.apple.center_y:
            data['au'] = 0
            data['ar'] = 0
            data['ad'] = 0
            data['al'] = 1

        data['wu'] = SCREEN_HEIGHT - self.snake.center_y
        data['wr'] = SCREEN_WIDTH - self.snake.center_x
        data['wd'] = self.snake.center_y
        data['wl'] = self.snake.center_x

        for part in self.snake.body:
            if self.snake.center_x == part['center_x'] and self.snake.center_y < part['center_y']:
                data['bu'] = 1
                data['br'] = 0
                data['bd'] = 0
                data['bl'] = 0
            elif self.snake.center_x == part['center_x'] and self.snake.center_y > part['center_y']:
                data['bu'] = 0
                data['br'] = 0
                data['bd'] = 1
                data['bl'] = 0
            elif self.snake.center_x < part['center_x'] and self.snake.center_y == part['center_y']:
                data['bu'] = 0
                data['br'] = 1
                data['bd'] = 0
                data['bl'] = 0
            elif self.snake.center_x > part['center_x'] and self.snake.center_y == part['center_y']:
                data['bu'] = 0
                data['br'] = 0
                data['bd'] = 0
                data['bl'] = 1


        output = self.model.predict(data)
        direction = output.argmax()

        if direction == 'u':
            self.snake.change_x = 0
            self.snake.change_y = 1
        elif direction == 'r':
            self.snake.change_x = 1
            self.snake.change_y = 0
        elif direction == 'd':
            self.snake.change_x = 0
            self.snake.change_y = -1
        elif direction == 'l':
            self.snake.change_x = -1
            self.snake.change_y = 0

    def on_key_release(self, key, modifiers):
        pass
    

if __name__ == "__main__":
    window = MyGame()
    arcade.run()