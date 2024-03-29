import arcade
import pandas as pd


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
        self.dataset = []


    def on_draw(self):
        arcade.start_render()

        self.snake.draw()
        self.apple.draw()
        
    def on_update(self, delta_time):

        # data = {'wu':0, 'wr':0, 'wd':0, 'wl':0, 'au':0, 'ar':0, 'ad':0, 'al':0, 'bu':0, 'br':0, 'bd':0, 'bl':0, 'direction':0}    
        data = {'au':0, 'ar':0, 'ad':0, 'al':0, 'bu':0, 'br':0, 'bd':0, 'bl':0, 'direction':0}    

        self.snake.on_update(delta_time)
        self.apple.on_update()

        if arcade.check_for_collision(self.snake, self.apple):
            self.snake.eat()
            self.apple = Apple(SCREEN_WIDTH, SCREEN_HEIGHT)

        if self.snake.center_y > self.apple.center_y:
            self.snake.change_x = 0
            self.snake.change_y = -1
            data['direction'] = '2'
        elif self.snake.center_y < self.apple.center_y:
            self.snake.change_x = 0
            self.snake.change_y = 1
            data['direction'] = '0'
        elif self.snake.center_x > self.apple.center_x:
            self.snake.change_x = -1
            self.snake.change_y = 0
            data['direction'] = '3'
        elif self.snake.center_x < self.apple.center_x:
            self.snake.change_x = 1
            self.snake.change_y = 0
            data['direction'] = '1'

        if self.snake.center_y < self.apple.center_y:
            data['au'] = 1
        elif self.snake.center_y > self.apple.center_y:
            data['ad'] = 1
        elif self.snake.center_x < self.apple.center_x:
            data['ar'] = 1
        elif self.snake.center_x > self.apple.center_x:
            data['al'] = 1

        # data['wu'] = SCREEN_HEIGHT - self.snake.center_y
        # data['wr'] = SCREEN_WIDTH - self.snake.center_x
        # data['wd'] = self.snake.center_y
        # data['wl'] = self.snake.center_x

        for part in self.snake.body:
            if self.snake.center_y < part['center_y']:
                data['bu'] = 1
            elif self.snake.center_y > part['center_y']:
                data['bd'] = 1
            elif self.snake.center_x < part['center_x']:
                data['br'] = 1
            elif self.snake.center_x > part['center_x']:
                data['bl'] = 1


        self.dataset.append(data)

    def on_key_release(self, key, modifiers):
        if key == arcade.key.Q:
            df = pd.DataFrame(self.dataset)
            df.to_csv('dataset/dataset.csv', index=False)
            arcade.close_window()
            exit(0)
    

if __name__ == "__main__":
    window = MyGame()
    arcade.run()