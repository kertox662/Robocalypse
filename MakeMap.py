from tkinter import *
from getData import *
from time import sleep

with open('data/TileData.txt') as mapD:
        tileMap = mapD.read().split('\n')
    
for i in range(len(tileMap)):
    tileMap[i] = tileMap[i].split(',')

# for i in tileMap:
#     print(i)

root = Tk()
c = Canvas(root, width = 800, height = 800)
c.pack()

squares = [0]*2500

for i in range(50):
        for j in range(50):
            tileText = tileMap[i][j]
            if tileText == "2":
                col = 'blue'
            elif tileText in ['20','21', '22', '23', '24', '25', '26', '27', '28', '33','34','35','36']:
                col = 'sandy brown'
            else:
                col = 'green'
            squares[j + i*50] = c.create_text(i*16, j*16, fill = col, text = tileText)#, text = tileMap[i][j])


while True:
    for i in range(50):
        for j in range(50):
            tileText = tileMap[i][j]
            if tileText == '2':
                col = 'blue'

            elif tileText in ['20','21', '22', '23', '24', '25', '26', '27', '28', '33','34','35','36']:
                col = 'sandy brown'
            
            else:
                col = 'green'
                                
            c.delete(squares[j + i*50])

            squares[j + i*50] = c.create_text(j*16 + 8, i*16 + 8, fill = col, text = tileText)#, text = tileMap[i][j])
    
    c.update()
    sleep(0.03)



c.mainloop()