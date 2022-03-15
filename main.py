
from asyncio.windows_events import NULL
from math import sqrt
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
        def getDistance(start, end):
                distance = sqrt(pow(end.x - start.x, 2) + pow(end.y - start.y, 2))
                return distance

        @staticmethod
        def showPath(cameFrom, current):
                print(' do showPath ')

        @staticmethod
        def solveMaze(maze):
                openSet = []
                start = maze.openSpaces[0]
                start.button.background_color = (255, 0, 0, 255)
                print('start '+str(start.x) +',' +str(start.y))
                openSet.append(start)

                cameFrom = []
                
                gScore = {start: 0}

                end = maze.destinationButton
                distance = AStar.getDistance(start, end)
                fScore = {start: distance}

                # currentCost should be in gScore?
                currentCost = 0
                universalCost = 1

                fScoreIndex = 0

                done = False

                while len(openSet) > 0:
                        current = list(fScore.keys())[fScoreIndex]
                        print(str(current.x) + ',' + str(current.y) + ' fscoreindex' + str(fScoreIndex))

                        if current == end:
                                AStar.showPath(cameFrom, current)
                                done = True

                        if done == True:
                                break


                        print('remove-' + str(current.x) + ',' + str(current.y))
                        openSet.remove(current)


                        neighbors = []
                        for space in maze.openSpaces:
                                if space.x == current.x:
                                        if current.y + 1 == space.y or current.y - 1 == space.y:
                                                neighbors.append(space)
                                        else:
                                                continue

                                if space.y == current.y:
                                        if current.x - 1 == space.x or current.x + 1 == space.x:
                                                neighbors.append(space)
                                        else:
                                                continue

                                if current.y - 1 == space.y or current.y + 1 == space.y:
                                        if current.x + 1 == space.x or current.x - 1 == space.x:
                                                neighbors.append(space)
                                        else:
                                                continue

                        tentativeHScores = {}
                        tentativeFScores = {}
                        tentativeGScores = {}
                        flag = True
                        for neighbor in neighbors:
                                tentativeGScore = gScore[current] + universalCost
                                tentativeHScore = AStar.getDistance(neighbor, end)
                                tentativeFScore = tentativeGScore + tentativeHScore
                                tentativeHScores[neighbor] = tentativeHScore
                                tentativeFScores[neighbor] = tentativeFScore
                                tentativeGScores[neighbor] = tentativeGScore
                                print(str(tentativeFScore) + ' = ' + str(tentativeGScore) + ' + ' + str(tentativeHScore) +' ------------ ' + str(fScore[current]))
                                if tentativeFScore < fScore[current]:
                                        gScore[neighbor] = tentativeGScore
                                        fScore[neighbor] = tentativeFScore
                                        fScoreIndex = len(fScore.keys()) - 1
                                        if neighbor not in openSet:
                                                openSet.append(neighbor)
                                        cameFrom.append(current)
                                        current = neighbor
                                        if current != end:
                                                current.button.background_color = (255, 255, 255, 255)
                                        print('new current' + str(current.x) + ',' + str(current.y))
                                        flag = False
                        
                        if flag == True:
                                low = float('inf')
                                lowSpace = NULL
                                for key in tentativeHScores:
                                        if tentativeHScores[key] < low:
                                                low = tentativeHScores[key]
                                                lowSpace = key

                                gScore[lowSpace] = tentativeGScores[lowSpace]
                                fScore[lowSpace] = tentativeFScores[lowSpace]
                                fScoreIndex = len(fScore.keys()) - 1
                                if lowSpace not in openSet:
                                        openSet.append(lowSpace)
                                cameFrom.append(current)
                                current = lowSpace
                                if current != end:
                                        current.button.background_color = (255, 255, 255, 255)
                                print('new current flagged' + str(current.x) + ',' + str(current.y))
                                

class Maze():
        obstacles = []
        openSpaces = []
        path = []
        destination = (-1, -1)
        destinationButton = NULL

        def __init__(self, rows, cols):
                self.rows = rows
                self.cols = cols

        def setDestination(self, x, y):
                self.destination = (x, y)
                for space in self.openSpaces:
                        if space.x == x and space.y == y:
                                space.button.background_color = (0, 255, 0, 255)
                                self.destinationButton = space
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
                                if y + 1 == obstacle.y or y - 1 == obstacle.y:
                                        return False
                                else:
                                        continue

                        if y == obstacle.y:
                                if x - 1 == obstacle.x or x + 1 == obstacle.x:
                                        return False
                                else:
                                        continue

                        if y - 1 == obstacle.y or y + 1 == obstacle.y:
                                if x + 1 == obstacle.x or x - 1 == obstacle.x:
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
                #for ob in maze.obstacles:
                #        print(str(ob))

                for os in maze.openSpaces:
                        print(str(os.x) + ',' + str(os.y))
                
                AStar.solveMaze(maze)


class MyApp(App):
        def build(self):
                return MyGrid()


if __name__ == '__main__':
        myApp = MyApp()
        myApp.run()