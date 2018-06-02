from Tile import *
from GameObject import *
from GameItem import *
from Scene import Scene

class GameScene(Scene):

    def __init__(self, screen, KHandler):
        super().__init__("scene_game", screen, KHandler, connections = ["scene_main", "scene_menu"])

    def showTiles(self, tileArray):
        for i in tileArray:
            for j in i:
                j.display()
    
    def checkRendered(self, tileArray):
        for i in tileArray:
            for j in i:
                if not j.isOnScreen():
                    return False
        
        return True
    
    def setRenderGrid(self,tileArray, renderArray):
        newRenderArray = []

        if renderArray == None:
            firstIndexX = 0
            firstIndexY = 0
            lastIndexX = tileGridWidth
            lastIndexY = tileGridHeight
        
        else:
            firstIndexX = renderArray[0][0].indexX
            firstIndexX = max(0, firstIndexX - 2)

            firstIndexY = renderArray[0][0].indexY
            firstIndexY = max(0, firstIndexY - 2)

            lastIndexX = renderArray[-1][-1].indexX
            lastIndexX = min(tileGridWidth, lastIndexX + 2)

            lastIndexY = renderArray[-1][-1].indexY
            lastIndexY = min(tileGridHeight, lastIndexY + 2)

            for i in renderArray:
                for j in i:
                    self.screen.canv.delete(j.screenObj)
        print("First", firstIndexX, firstIndexY)
        print("Last", lastIndexX, lastIndexY)

        for i in tileArray[firstIndexY:lastIndexY + 1]:
            newRenderArray.append([])
            for j in i[firstIndexX:lastIndexX + 1]:
                if j.isOnScreen():
                    newRenderArray[-1].append(j)
        

        for i in range(len(newRenderArray) - 1, -1, -1):
            if newRenderArray[i] == []:
                newRenderArray.pop(i)

        # print(lastIndexX - firstIndexX, lastIndexY - firstIndexY)
        print(len(newRenderArray[0]), len(newRenderArray))

        return newRenderArray