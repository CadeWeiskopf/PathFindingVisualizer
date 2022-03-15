from ast import AST
from colorsys import hls_to_rgb
import kivy
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
import random


class AStar():
        @staticmethod
        def makeStep():
                print('do makeStep')

        @staticmethod
        def solveMaze(maze):
                step = maze.openSpaces[0].button
                step.background_color = (255, 0, 0, 255)
                for space in maze.openSpaces:
                        AStar.makeStep()


class Maze():
        obstacles = []
        openSpaces = []
        path = []
        destination = (-1, -1)

        def __init__(self, rows, cols):
                self.rows = rows
                self.cols = cols

        def setDestination(self, x, y):
                self.destination = (x, y)
                for space in self.openSpaces:
                        if space.x == x and space.y == y:
                                space.button.background_color = (0, 255, 0, 255)
                                print('destination')


class GridSpace():
        def __init__(self, button, x, y):
                self.button = button
                self.x = x
                self.y = y

class GridObstacle():
        def __init__(self, button, x, y):
                self.button = button
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
                maze = Maze(20, 20)
                self.rows = maze.rows
                self.cols = maze.cols
                print(str(maze.rows) + ' ' + str(maze.cols))
                i = maze.rows
                while i > 0:
                        j = maze.cols
                        while j > 0:
                                if (i == maze.rows and j == maze.cols) == False and (i == 1 and j == 1) == False and GridObstacle.placeObstacle(maze.obstacles, j, i) == True:
                                        # create obstacle
                                        button = Button(text=' ')
                                        self.add_widget(button)
                                        obstacle = GridObstacle(button, j, i)
                                        maze.obstacles.append(obstacle)
                                else:
                                        # create empty space
                                        button = Button(text=' ', background_color=(0,0,0,255))
                                        self.add_widget(button)
                                        space = GridSpace(button, j, i)
                                        maze.openSpaces.append(space)
                                j -= 1
                        i -= 1

                maze.setDestination(1, 1)
                for ob in maze.obstacles:
                        print(str(ob))

                for os in maze.openSpaces:
                        print(str(os))
                
                AStar.solveMaze(maze)



        

class MyApp(App):
        def build(self):
                return MyGrid()

if __name__ == '__main__':
        myApp = MyApp()
        myApp.run()