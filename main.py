from colorsys import hls_to_rgb
import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
import random


class Grid():
        obstacles = []
        openSpaces = []

        def __init__(self, rows, cols):
                self.rows = rows
                self.cols = cols
        

class GridObstacle():
        def __init__(self, btn, x, y):
                self.btn = btn
                self.x = x
                self.y = y
        
        @staticmethod
        def placeObstacle(obstacles, x, y):
                for obstacle in obstacles:
                        if x == obstacle.x:
                                # if above : y+1
                                # if below : y-1
                                if y + 1 == obstacle.y or y - 1 == obstacle.y:
                                        return False
                                else:
                                        continue

                        if y == obstacle.y:
                                # if left : x-1
                                # if right : x+1
                                if x - 1 == obstacle.x or x + 1 == obstacle.x:
                                        return False
                                else:
                                        continue

                        if x + 1 == obstacle.x:
                                # if topleft : x+1, y-1
                                # if topright : x+1, y+1
                                if y - 1 == obstacle.y or y + 1 == obstacle.y:
                                        return False
                                else:
                                        continue

                        if x - 1 == obstacle.x:
                                # if botleft : x-1, y-1
                                # if botright : x-1, y+1
                                if y - 1 == obstacle.y or y + 1 == obstacle.y:
                                        return False
                                else:
                                        continue

                return bool(random.randint(0, 1))


class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        grid = Grid(20, 20)
        self.rows = grid.rows
        self.cols = grid.cols
        print(str(grid.rows) + ' ' + str(grid.cols))
        i = grid.rows
        while i > 0:
                j = grid.cols
                while j > 0:
                        if (i == grid.rows and j == grid.cols) == False and (i == 1 and j == 1) == False and GridObstacle.placeObstacle(grid.obstacles, j, i) == True:
                                # create obstacle
                                button = Button(text=' ')
                                self.add_widget(button)
                                obstacle = GridObstacle(button, j, i)
                                grid.obstacles.append(obstacle)
                        else:
                                # create empty space
                                button = Button(text=' ', background_color=(0,0,0,255))
                                self.add_widget(button)
                                grid.openSpaces.append((j, i))
                        j -= 1
                i -= 1

        for ob in grid.obstacles:
                print(str(ob))

        for os in grid.openSpaces:
                print(str(os))

class MyApp(App):
    def build(self):
        return MyGrid()

if __name__ == '__main__':
    myApp = MyApp()
    myApp.run()