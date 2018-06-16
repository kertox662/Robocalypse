from time import sleep, time
from tkinter import *

root = Tk()
c = Canvas(root, width = 800, height = 800)
c.pack()

def func(e):
    print(e.x, e.y)
    try:
        print(e.keysym)
    except:
        pass

x = -1

while True:
    c.delete(x)
    x = c.create_rectangle(200, 200, 300, 300, fill = 'red')
    c.tag_bind(x, "<Button-1>", func)
    c.tag_bind(x, "e", func)
    c.update()
    sleep(0.03)









# start = time()
# sleep(1)
# print(time() - start)


# from random import randint
# # class Tester:
# #     def __init__(self, value):
# #         self.val = value


# # l1 = []
# # for i in range(10):
# #     l1.append(Tester(i))

# # l2 = []
# # for i in range(10):
# #     l2.append(Tester(l1[0].val))
# #     l2[i].val *= 3

# # for i in range(10):
# #     print(l1[i].val, l2[i].val)

# class Grid:
#     def __init__(self):
#         row = [0]*5
#         self.grid = []
#         # for i in self.grid:
#         #     print(i)
#         # print()
#         for i in range(5):
#             self.grid.append(row.copy())
#             for j in range(5):
#                 self.grid[i][j] = randint(0,9)
#                 # print(self.grid[i][j])

#     def display(self):
#         for i in self.grid:
#             print(i)


# gridOfGrids = [[]]*3
# for i in range(3):
#     for j in range(3):
#         gridOfGrids[i].append(Grid())
#         print(len(gridOfGrids[i]))

# print(len(gridOfGrids))

# print(gridOfGrids)

# for i in range(len(gridOfGrids)):
#     for j in range(len(gridOfGrids[0])):
#         grid = gridOfGrids[i][j]
#         grid.display()
#         for i in range(len(gridOfGrids)):
#             try:
#                 indX = gridOfGrids[i].index(grid)
#                 indY = i
            
#             except:
#                 pass
        
#         print("Index:", indX, indY)
#         print()

# # for i in range(len(renderedTiles)):
# #         for j in range(len(renderedTiles[0])):
# #             curTile = renderedTiles[i][j]
# #             for y in range(20):
# #                 for x in range(20):
# #                     curNode = curTile.nodeMap[y][x]
# #                     # print(curNode.x, curNode.y)
# #                     currentNodeMap[y + i*20].append(Node.fromCopy(curNode))