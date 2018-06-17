from getData import loadSettings
from Entity import stationaryEntity
from random import randint


def findMap(tileID, variation):
    entityData = tileData[tileID][variation].copy()
    print(entityData)
    entities = []
    entNum = entityData[0]
    entityData.pop(0)
    for i in range(entNum):
        entities.append(stationaryEntity(entityData[1], entityData[2], "None", 0, None, None, None, entityInfo[entityData[0]]["collision"] , True, None, None, None))
        if len(entityData) >= 3:
            for j in range(3):
                entityData.pop(0)

    for i in entities:
        print("x:",min(i.collisionBox[0]) + i.x + i.xOff, max(i.collisionBox[0]) + i.x + i.xOff)
        print("y:", min(i.collisionBox[1]) + i.y + i.yOff, max(i.collisionBox[1]) + i.y + i.yOff)

    nMap = []
    for i in range(20):
        row = [0]*20
        nMap.append(row)


    for eY in range(20):
        for eX in range(20):
            for ent in entities:
                x = eX*20
                y = eY*20
                # print(x,y)
                nMap[eY][eX] = int(ent.isPointInBox([x, y], "collision"))
                if nMap[eY][eX] == 1:
                    print("Found collision")
                    break

    for i in range(20):
        print(nMap[i])
    return

def findMapFromPrevious(grid, entities):
    for eY in range(20):
        for eX in range(20):
            for ent in entities:
                x = eX*20
                y = eY*20
                # print(x,y)
                nMap[eY][eX] = int(ent.isPointInBox([x, y], "collision"))


tileData = loadSettings("data/tileEntityArrangement.json")
entityInfo = loadSettings("data/entities.json")

tileID, variation = input("ID Variation").split(",")

print(findMap(tileID, variation))