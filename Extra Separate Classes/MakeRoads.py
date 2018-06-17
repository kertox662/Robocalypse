from tkinter import *
from getData import *
from time import sleep
from random import choice, randint

with open('data/TileData.txt') as mapD:
        tileMap = mapD.read().split('\n')
    
for i in range(len(tileMap)):
    tileMap[i] = tileMap[i].split(',')

tileCopy = [0]*50
for i in range(50):
    tileCopy[i] = tileMap[i].copy()

# for i in tileMap:
#     print(i)

root = Tk()
c = Canvas(root, width = 800, height = 800)
c.pack()

squares = [0]*2500

def setRoad(e):
    global tileCopy
    i = e.x // 16
    j = e.y//16
    tileCopy[j][i] = 'r'
    # print(tileCopy[i])

def saveRoads():
    with open('data/TileData.txt', 'w') as f:
        for y in tileMap:
            line = str(y)
            line = line[1:len(line)]
            line = line.replace("]", '\n')
            line = line.replace(" ", "")
            line = line.replace("'","")
            f.write(line)

def configureRoads(e):
    global tileMap
    for y in range(50):
        for x in range(50):
            if tileCopy[y][x] in ['20','21', '22', '23', '24', '25', '26', '27', '28', '33','34','35','36', 'r']:
                numConnections = 0
                if tileCopy[y - 1][x] in ['20','21', '22', '23', '24', '25', '26', '27', '28', '33','34','35','36', 'r']:
                    numConnections += 1
                if tileCopy[y + 1][x] in ['20','21', '22', '23', '24', '25', '26', '27', '28', '33','34','35','36', 'r']:
                    numConnections += 1
                if tileCopy[y][x - 1] in ['20','21', '22', '23', '24', '25', '26', '27', '28', '33','34','35','36', 'r']:
                    numConnections += 1
                if tileCopy[y][x + 1] in ['20','21', '22', '23', '24', '25', '26', '27', '28', '33','34','35','36', 'r']:
                    numConnections += 1
                
                # print(tileCopy[y - 1][x], tileCopy[y + 1][x], tileCopy[y][x-1], tileCopy[y][x + 1])

                # print(numConnections)

                if numConnections == 4:
                    tileMap[y][x] = '28'
                
                elif numConnections == 3:
                    if tileCopy[y - 1][x] not in ['20','21', '22', '23', '24', '25', '26', '27', '28', '33','34','35','36', 'r']:
                        tileMap[y][x] = '26'
                    elif tileCopy[y + 1][x] not in ['20','21', '22', '23', '24', '25', '26', '27', '28', '33','34','35','36', 'r']:
                        tileMap[y][x] = '24'
                    elif tileCopy[y][x - 1] not in ['20','21', '22', '23', '24', '25', '26', '27', '28', '33','34','35','36', 'r']:
                        tileMap[y][x] = '25'
                    else:
                        tileMap[y][x] = '27'
                
                elif numConnections == 2:
                    if tileCopy[y - 1][x] not in ['20','21', '22', '23', '24', '25', '26', '27', '28', '33','34','35','36', 'r'] and tileCopy[y + 1][x] not in ['20','21', '22', '23', '24', '25', '26', '27', '28', '33','34','35','36', 'r']:
                        tileMap[y][x] = choice(["20","21"])
                    elif tileCopy[y - 1][x] not in ['20','21', '22', '23', '24', '25', '26', '27', '28', '33','34','35','36', 'r'] and tileCopy[y][x - 1] not in ['20','21', '22', '23', '24', '25', '26', '27', '28', '33','34','35','36', 'r']:
                        tileMap[y][x] = "35"
                    elif tileCopy[y - 1][x] not in ['20','21', '22', '23', '24', '25', '26', '27', '28', '33','34','35','36', 'r'] and tileCopy[y][x + 1] not in ['20','21', '22', '23', '24', '25', '26', '27', '28', '33','34','35','36', 'r']:
                        tileMap[y][x] = "36"
                    elif tileCopy[y + 1][x] not in ['20','21', '22', '23', '24', '25', '26', '27', '28', '33','34','35','36', 'r'] and tileCopy[y][x - 1] not in ['20','21', '22', '23', '24', '25', '26', '27', '28', '33','34','35','36', 'r']:
                        tileMap[y][x] = "34"
                    elif tileCopy[y + 1][x] not in ['20','21', '22', '23', '24', '25', '26', '27', '28', '33','34','35','36', 'r'] and tileCopy[y][x + 1] not in ['20','21', '22', '23', '24', '25', '26', '27', '28', '33','34','35','36', 'r']:
                        tileMap[y][x] = "33"
                    elif tileCopy[y][x-1] not in ['20','21', '22', '23', '24', '25', '26', '27', '28', '33','34','35','36', 'r'] and tileCopy[y][x + 1] not in ['20','21', '22', '23', '24', '25', '26', '27', '28', '33','34','35','36', 'r']:
                        tileMap[y][x] = choice(["22","23"])
                    else:
                        pass
                
                else:
                    tileMap[y][x] = '1'
                
            tileMap[y][j] = int(tileMap[i][j])
    saveRoads()

root.bind("<space>", configureRoads)

for i in range(50):
        for j in range(50):
            tileText = tileCopy[i][j]
            if tileText == "2":
                col = 'blue'
            elif tileText in ['20','21', '22', '23', '24', '25', '26', '27', '28', '33','34','35','36', 'r']:
                col = 'sandy brown'
            else:
                col = 'green'
            squares[j + i*50] = c.create_text(i*16, j*16, fill = col, text = tileText)

while True:
    for i in range(50):
        for j in range(50):
            tileText = tileCopy[i][j]
            if tileText == '2':
                col = 'blue'

            elif tileText in ['20','21', '22', '23', '24', '25', '26', '27', '28', '33','34','35','36', 'r']:
                col = 'sandy brown'
            
            else:
                col = 'green'
                                
            c.delete(squares[j + i*50])

            squares[j + i*50] = c.create_text(j*16 + 8, i*16 + 8, fill = col, text = tileText)
            c.tag_bind(squares[j + i*50], "<Button-1>", setRoad)
    

    c.update()
    sleep(0.03)



c.mainloop()