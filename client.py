import pygame
from player import Player
from network import Network

# window height and width
width = 500
height = 500
window = pygame.display.set_mode((width, height))

pygame.display.set_caption("Client")


def redrawWindow(window,player,player2):
    
    # draw white window
    window.fill((255,255,255))
    player.draw(window)
    player2.draw(window)
    pygame.display.update()


def main():
    
    run = True
    
    n = Network()
    p = n.getP()
   
    clock = pygame.time.Clock()
    
#  dayman loop btt3ml fe pygame
    while run:
        clock.tick(60)
        p2 = n.send(p)
  
        p2.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p.move()
        redrawWindow(window,p,p2)

main()

