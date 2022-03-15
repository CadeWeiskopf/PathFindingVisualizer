
from asyncio.windows_events import NULL
from queue import PriorityQueue
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
        #distance = sqrt(pow(end.x - start.x, 2) + pow(end.y - start.y, 2))
        distance = abs(start.x - end.x) + abs(start.y - end.y)
        return distance

    @staticmethod
    def showPath(cameFrom, current):
        print(' do showPath ')
        while current in cameFrom:
            current.button.background_color = (255, 0, 0, 255)
            current = cameFrom[current]
    
    @staticmethod
    def getNeighbors(maze, current):
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
        return neighbors

    @staticmethod
    def solveMaze(maze):
        start = maze.openSpaces[0]
        start.button.background_color = (255, 0, 0, 255)
        end = maze.destinationButton

        count = 0
        openSet = PriorityQueue()
        openSet.put((start.fScore, count, start))
        cameFrom = {}
        gScore = {space: float('inf') for space in maze.openSpaces}
        gScore[start] = 0
        fScore = {space: float('inf') for space in maze.openSpaces}
        fScore[start] = AStar.getDistance(start, end)

        openSetHash = {start}

        while not openSet.empty():
            current = openSet.get()[2]
            openSetHash.remove(current)

            if current == end:
                print('DONE, SHOW PATH')
                AStar.showPath(cameFrom, end)
                break

            neighbors = AStar.getNeighbors(maze, current)
            for neighbor in neighbors:
                tempGScore = gScore[current] + 1
                
                if tempGScore < gScore[neighbor]:
                    cameFrom[neighbor] = current
                    gScore[neighbor] = tempGScore
                    fScore[neighbor] = tempGScore + AStar.getDistance(neighbor, end)
                    if neighbor not in openSetHash:
                        count += 1
                        openSet.put((fScore[neighbor], count, neighbor))
                        openSetHash.add(neighbor)
                        neighbor.open = True
                        
            if current != start:
                current.open = False
                current.button.background_color = (255, 255, 255, 255)       

class Maze():
    obstacles = []
    openSpaces = []
    path = []
    destination = (-1, -1)
    destinationButton = None

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
        self.gScore = 0
        self.hScore = 0
        self.fScore = 0
        self.previous = NULL
        self.open = False
        
    def printSelf(self):
        print('(' + str(self.x) + ',' + str(self.y) + ')' + 'f=' + str(self.fScore) + ' g=' + str(self.gScore) + ' h=' + str(self.hScore))


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

        for os in maze.openSpaces:
            print(str(os.x) + ',' + str(os.y))

        AStar.solveMaze(maze)

class MyApp(App):
    def build(self):
        return MyGrid()

if __name__ == '__main__':
    myApp = MyApp()
    myApp.run()