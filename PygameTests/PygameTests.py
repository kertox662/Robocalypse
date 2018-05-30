import pygame
from tkinter import *
import time

# pygame.init()
# screenSize = [1,1]
# pygame.display.set_mode(screenSize)

root = Tk()

pygame.mixer.init(44100, -16,2,2048)
pygame.mixer.music.load('TestExplosion.mp3')
pygame.mixer.music.play(0)
s = pygame.mixer.Sound('RNoise.wav')
empty_channel = pygame.mixer.find_channel()
empty_channel.play(s)
time.sleep(0.5)
empty_channel = pygame.mixer.find_channel()
empty_channel.play(s)

root.mainloop()

# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.KEYDOWN:
#             # Figure out if it was an arrow key. If so
#             # adjust speed.
#             if event.key == pygame.K_LEFT:
#                 print("Left Press")
#             elif event.key == pygame.K_RIGHT:
#                 print("Right Press")
#             elif event.key == pygame.K_UP:
#                 print("Up Press")
#             elif event.key == pygame.K_DOWN:
#                 print("Down Press")
    
#             # User let up on a key
#         elif event.type == pygame.KEYUP:
#             # If it is an arrow key, reset vector back to zero
#             if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
#                 print("Left/Right Release")
#             elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
#                 print("Up/Down Release")