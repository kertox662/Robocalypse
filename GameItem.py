from time import sleep, time
from tkinter import *



class test:
    def __init__(self,val):
        self.val = val
    
    def change(self):
        self.val += 5


x = 5

t = test(x)
t.change()

print(x)





# root = Tk()
# c = Canvas(root, width = 800, height = 800)
# c.pack()

# def func(e):
#     print(e.x, e.y)
#     try:
#         print(e.keysym)
#     except:
#         pass

# x = -1

# while True:
#     c.delete(x)
#     x = c.create_rectangle(200, 200, 300, 300, fill = 'red')
#     c.tag_bind(x, "<Button-1>", func)
#     c.tag_bind(x, "e", func)
#     c.update()
#     sleep(0.03)









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




# print(listInd, xInd, yInd)
                # grid = []
                # for y in tileYpossibilities:
                #     grid.append([])
                #     for x in tileXpossibilities:
                #         grid[tileYpossibilities.index(y)].append(tileGrid[yInd + y][xInd + x])

                # print(xInd, yInd)
                # print("Coords")
                # for j in grid:
                #     for k in j:
                #         print(k.x, k.y)
                # print()
                # print("Coords Nodes:")
                # for j in grid:
                #     for k in j:
                #         print(k.nodeMap[0][0].x, k.nodeMap[0][0].y)

                # print()
                # sleep(1)
                
                
                # # if xInd != 0:
                # #     tileXpossibilities.append(-1)
                
                # # tileXpossibilities.append(0):

                # # if xInd != tileGridWidth - 1:
                # #     tileXpossibilities.append(1)
                
                # # if yInd != 0:
                # #     tileYpossibilities.append(-1)
                
                # # tileYpossibilities.append(0):

                # # if yInd != tileGridHeight - 1:
                # #     tileYpossibilities.append(1)
                
                # curGrid = []
                # for y in tileYpossibilities:
                #     curGrid.append([])
                
                # for y in tileYpossibilities:
                #     for x in tileXpossibilities:
                #         print("In List:",tileYpossibilities.index(y))
                #         print("Indices:", yInd + y, xInd + x)
                #         curGrid[tileYpossibilities.index(y)].append(tileGrid[yInd + y][xInd + x])
                
                # for a in curGrid:
                #     print()
                #     for b in a:
                #         print(b.nodeMap[0][0].x, b.nodeMap[0][0].y)
                # print()
                # curNodeMap = nodeMapFromTiles(curGrid)

                # for c in curNodeMap:
                #     print(c[0].x, c[0].y)
                # # startIndX = int((i.x - curNodeMap[0][0].x) // 20)
                # # startIndY = int((i.y - curNodeMap[0][0].y) // 20)
                # # startNode = curNodeMap[startIndY][startIndX]

                # direction = atan2(i.y - player.y , i.x - player.x) + pi
                
                # curTileX = int(player.x // Tile.tileWidth)
                # curTileY = int(player.y // Tile.tileHeight)
                # curPlayerTile = tileGrid[curTileY][curTileX]
                
                # targetInMap = False
                # for tileList in curGrid:
                #     if curPlayerTile in tileList:
                #         targetInMap = True
                #         targetX = int((player.x - curPlayerTile.x) // 20)
                #         targetY = int((player.y - curPlayerTile.y) // 20)
                #         target = curPlayerTile.nodeMap[targetY][targetX]
                

                # print((degrees(direction) + 180)%360)

                # if targetInMap == False:
                #     if 3*pi / 8 <= direction <= 5 * pi / 8:
                #         target = curGrid[-1][1].nodeMap[-1][10]

                #     elif 11*pi / 8 <= direction <= 13 * pi / 8:
                #         target = curGrid[0][1].nodeMap[0][10]
                    
                #     elif 7*pi/8 <= direction <= 9*pi/8:
                #         target = tileGrid[indY][indX + 1].nodeMap[10][-1]
                    
                #     elif direction <= pi / 8 or direction >= 15*pi / 8:
                #         target = tileGrid[indY][indX - 1].nodeMap[10][0]
                    


                #     elif 5*pi / 8 <= direction <= 7*pi / 8:
                #         target = curGrid[-1][-1].nodeMap[-1][-1]
                    
                #     elif 9*pi / 8 <= direction <= 11*pi / 8:
                #         target = curGrid[0][-1].nodeMap[0][-1]
                        
                    
                #     elif 13*pi / 8 <= direction <= 15*pi / 8:
                #         target = curGrid[0][0].nodeMap[0][0]
                    
                #     elif pi / 8 <= direction <= 3*pi / 8:
                #         target = curGrid[-1][0].nodeMap[-1][0]
                    
                #     # else:
                #     #     target = 
                
                # i.findShortestPath(curNodeMap, target)