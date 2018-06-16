from tkinter import *
from time import sleep
from math import *

root = Tk()
c = Canvas(root, width = 800, height = 800)
c.pack()


gridSize = 40
grid = []
grid.append([1]*gridSize)
for i in range(gridSize-2):
    grid.append([1] + [0]*(gridSize-2) + [1])

grid.append([1]*gridSize)

squaresize = 20
gridCanvas = []

def displayGrid():
    for i in gridCanvas:
        c.delete(i)
    
    for i in range(gridSize):
        for j in range(gridSize):
            if grid[i][j] == 1:
                color = 'red'
            else:
                color = 'green'
            gridCanvas.append(c.create_rectangle(j * squaresize, i * squaresize, (j+1) * squaresize, (i + 1) * squaresize, fill = color))

def toggleSquare(e):
    global grid
    indX = e.x // squaresize
    indY = e.y // squaresize
    grid[indY][indX] = int(not grid[indY][indX])

def printGrid(e):
    for i in grid:
        print(i)

c.bind("<Button-1>", toggleSquare)
root.bind("<space>", printGrid)

while True:
    displayGrid()
    c.update()
    sleep(0.03)