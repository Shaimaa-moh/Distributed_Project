
import pygame
class Player():
    def __init__(self,x,y,width,height,color): #creating player 1  
        self.x = x
        self.y = y 
        self.width =width 
        self.height = height
        self.color = color
        self.rect =(x,y,width,height)
        self.vel =3 #initial value in screen
        
    def draw(self,window): #draw rectangle on screen
        pygame.draw.rect(window,self.color,self.rect)
    
    def move(self):
        keys= pygame.key.get_pressed()  # 1 means key is pressed , 0 not pressed
        if keys[pygame.K_LEFT]:
            self.x -= self.vel
        
        if keys[pygame.K_RIGHT]:
            self.x += self.vel
        if keys[pygame.K_UP]:
            self.y -= self.vel
        if keys[pygame.K_DOWN]:
            self.y += self.vel
        self.update()
            
    def update(self): #responsible for updating positions in the window frame
       self.rect =(self.x, self.y, self.width,self.height) #update rectangle