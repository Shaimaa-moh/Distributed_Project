import pygame
from player import Player

# window height and width
width = 500
height = 500
win = pygame.display.set_mode((width, height))

pygame.display.set_caption("Client")


def redrawWindow():
    
    # draw white window
    win.fill((255,255,255))
 
    pygame.display.update()


def main():
    
    run = True
   
    clock = pygame.time.Clock()
    
#  dayman loop btt3ml fe pygame
    while run:
        clock.tick(60)
  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

     
        redrawWindow()

main()