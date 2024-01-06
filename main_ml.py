import tensorflow as tf
import numpy as np
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
        self.model =  tf.keras.models.load_model('model/model.h5')


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

        # dict_data = {'wu':0, 'wr':0, 'wd':0, 'wl':0, 'au':0, 'ar':0, 'ad':0, 'al':0, 'bu':0, 'br':0, 'bd':0, 'bl':0}
        dict_data = {'au':0, 'ar':0, 'ad':0, 'al':0, 'bu':0, 'br':0, 'bd':0, 'bl':0}

        if self.snake.center_y < self.apple.center_y:
            dict_data['au'] = 1
        elif self.snake.center_y > self.apple.center_y:
            dict_data['ad'] = 1
        elif self.snake.center_x < self.apple.center_x:
            dict_data['ar'] = 1
        elif self.snake.center_x > self.apple.center_x:
            dict_data['al'] = 1

        # dict_data['wu'] = SCREEN_HEIGHT - self.snake.center_y
        # dict_data['wr'] = SCREEN_WIDTH - self.snake.center_x
        # dict_data['wd'] = self.snake.center_y
        # dict_data['wl'] = self.snake.center_x

        for part in self.snake.body:
            if self.snake.center_y < part['center_y']:
                dict_data['bu'] = 1
            elif self.snake.center_y > part['center_y']:
                dict_data['bd'] = 1
            elif self.snake.center_x < part['center_x']:
                dict_data['br'] = 1
            elif self.snake.center_x > part['center_x']:
                dict_data['bl'] = 1

        values_data = dict_data.values()
        list_data = list(values_data)
        data = np.array([list_data])

        output = self.model.predict(data)
        direction = output.argmax()


        if direction == 0:
            self.snake.change_x = 0
            self.snake.change_y = 1
        elif direction == 1:
            self.snake.change_x = 1
            self.snake.change_y = 0
        elif direction == 2:
            self.snake.change_x = 0
            self.snake.change_y = -1
        elif direction == 3:
            self.snake.change_x = -1
            self.snake.change_y = 0

    def on_key_release(self, key, modifiers):
        if key == arcade.key.Q:
            arcade.close_window()
            exit(0)
    

if __name__ == "__main__":
    window = MyGame()
    arcade.run()