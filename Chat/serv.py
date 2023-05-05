import pygame as pg
import socket
import select
# MVC
# Model
class client:
    #Save clients as a linked List
    def __init__(self,name):
        self.name = name
        self.next=None
        
class ClientList:
    def __init__(self):
        self.head=None

    def add(self,name):
        newClient=client(name)

        #Check if the list is empty
        if self.head is None:
            self.head=newClient

        else:
            newClient.next=self.head
            self.head=newClient        

#View
#creating gui elements

class label:
    def __init__(self, text, font):
        self.text = text
        self.font = font
    
    def draw(self, surface, x, y, color):
        #render the font that takes the text input, bounces it down an image, blit is we copy that image of the text  onto the screen
        surface.blit(self.font.render(self.text, True, color), (x - 8, y - 15))

class Rectangle:
    def __init__(self, topLeft, size):
        self.rect = (topLeft[0], topLeft[1], size[0], size[1])
    
    def draw(self, surface, color):
        pg.draw.rect(surface, color, self.rect)

class Button:
    def __init__(self, panel, text, onColor, offColor):
        self.panel = panel
        self.text = text
        self.onColor = onColor
        self.offColor = offColor
    
    def hasMouse(self):
        (x,y) = pg.mouse.get_pos()
        left = self.panel.rect[0]
        right = self.panel.rect[0] + self.panel.rect[2]
        up = self.panel.rect[1]
        down = self.panel.rect[1] + self.panel.rect[3]
        return x > left and x < right and y > up and y < down

    def draw(self, surface):
        panelColor = self.offColor
        textColor = self.onColor
        if self.hasMouse():
            panelColor = self.onColor
            textColor = self.offColor
        self.panel.draw(surface, panelColor)
        self.text.draw(surface, self.panel.rect[0] + 15, self.panel.rect[1] + 15, textColor)

class ViewController:
    def __init__(self) :
        self.screen=pg.display.set_mode((800,600))
        self.palette={
            'teal':(0,128,128),
            'tur':(79, 185, 175),
            't':(179, 224, 220),
            'dark':(26,36,33)
            
        }
        self.font=pg.font.SysFont('arial',24)
        self.clientBox = Rectangle((50, 40), (600, 400))
        self.quitButton=Button(
            panel=Rectangle((100,500),(200,32)),
            text=label("Shut Down Server",self.font),
            onColor=self.palette["tur"],
            offColor=self.palette['t']
            )
    def drawScreen(self):
        self.screen.fill(self.palette["teal"])
        pg.display.update()
        self.clientBox = Rectangle((50, 40), (600, 400))
        #Draw client box
        self.clientBox.draw(self.screen, self.palette["t"])
        self.quitButton.draw(self.screen)
    def shouldExit(self):
        return self.quitButton.hasMouse()     
# Control

class Server:
    def __init__(self) :
        pg.init()
        self.viewcontroller=ViewController()

    def run(self):
         running=True
         while running:
            for event in pg.event.get():
                if event.type==pg.QUIT:
                     running=False
                elif event.type==pg.MOUSEBUTTONDOWN:
                    running= not self.viewcontroller.shouldExit()     
            self.viewcontroller.drawScreen()   
                
    
    def exit(self):
        pass


if __name__ == '__main__':
    server=Server()
    server.run()
    server.exit()    