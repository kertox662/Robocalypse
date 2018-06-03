from Tile import *
from GameObject import *
from GameItem import *
from Scene import Scene
from math import ceil, floor

class GameScene(Scene):

    def __init__(self, screen, camera, KHandler):
        super().__init__("scene_game", screen, KHandler, connections = ["scene_main", "scene_menu"])
        self.camera = camera
        self.screen.root.bind("<Escape>", lambda e: self.change_scene("scene_main"))

    
    def change_scene(self, targetscene = None):
        if targetscene == "scene_main":
            if Scene.current_scene == 'scene_game':
                Scene.current_scene = targetscene
        
        else:
            if targetscene in self.connections:
                Scene.current_scene = targetscene
    

    def showTiles(self, tileArray):
        camX = self.camera.x
        camY = self.camera.y
        for i in tileArray:
            for j in i:
                j.display(camX, camY)
    
    def checkRendered(self, tileArray):
        for i in tileArray:
            for j in i:
                if not j.isOnScreen():
                    return False
        
        return True
    
    def setRenderGrid(self,tileArray):
        minX = floor((self.camera.x - self.screen.width/2 - 100) / Tile.tileWidth)
        maxX = ceil((self.camera.x + self.screen.width/2 + 100) / Tile.tileWidth)
        
        minY = floor((self.camera.y - self.screen.height/2 - 100) / Tile.tileHeight)
        maxY = ceil((self.camera.y + self.screen.height/2 + 100) / Tile.tileHeight)

        minX = max(minX, 0)
        maxX = min(maxX, tileGridWidth)

        minY = max(minY, 0)
        maxY = min(maxY, tileGridHeight)

        newRenderArray = []
        for i in tileArray[minY:maxY+1]:
            newRenderArray.append([])
            for j in i[minX:maxX + 1]:
                newRenderArray[-1].append(j)

        # print(len(newRenderArray[0]), len(newRenderArray))

        return newRenderArray