# import socket
# s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# port=int(input("Connect on port: "))
# s.connect(("192.168.1.7", port))
# this=input("Press any key to exit: ")
import pygame as pg
import socket
import select

# MVC
# Model
#Every client sends a message that then will ping back to all clients
class Message:


    def __init__(self, name, message):
        self.name = name
        self.message = message
        self.next = None

class MessageList:


    def __init__(self):
        self.head = None
    
    def add(self, name, message):

        newMessage = Message(name, message)

        #do we have an empty list?
        if self.head is None:
            self.head = newMessage
        
        else:
            newMessage.next = self.head
            self.head = newMessage

# When we type port number to connect to server we will select name to the client to login
#the server is going to check it
#View
#creating gui elements
## view controllers: Server selection, client login and chatroom

class Label:


   def __init__(self, text, font):
        self.text = text
        self.font = font
    
   def draw(self, surface, x, y, color):
	 #GUI
        #render the font that takes the text input, bounces it down an image, blit is we copy that image of the text  onto the screen
        surface.blit(self.font.render(self.text, True, color), (x - 8, y - 15))

class Rectangle:
    

    def __init__(self, topLeft, size):
        self.rect = (topLeft[0], topLeft[1], size[0], size[1])

        
    def hasMouse(self):
        (x,y) = pg.mouse.get_pos()
        left = self.rect[0]
        right = self.rect[0] + self.rect[2]
        up = self.rect[1]
        down = self.rect[1] + self.rect[3]
        return x > left and x < right and y > up and y < down
    
    def draw(self, surface, color):
        pg.draw.rect(surface, color, self.rect)


class Button:
    

    def __init__(self, panel, text, onColor, offColor):
        self.panel = panel
        self.text = text
        self.onColor = onColor
        self.offColor = offColor
    
    def hasMouse(self):
        
        return self.panel.hasMouse()

    def draw(self, surface):
        panelColor = self.offColor
        textColor = self.onColor
        if self.hasMouse():
            panelColor = self.onColor
            textColor = self.offColor
        self.panel.draw(surface, panelColor)
        self.text.draw(surface, self.panel.rect[0] + 15, self.panel.rect[1] + 15, textColor)

class InputField:


    def __init__(self, text, panel):

        self.text = text
        self.panel = panel
        self.ready = False
        self.active = False
    
    def hasMouse(self):
        
        return self.panel.hasMouse()
    
    def handleKeyPress(self, event):
	 #if we got a key press event then we pass that event on to this function
        if event.key == pg.K_RETURN:
	  #hit enter as during the chat we hit enter to send messages
            self.ready = True
        if event.key == pg.K_BACKSPACE:
	#hit backspace to erase the last character
            #get the string everything up to one before the end
            self.text.text = self.text.text[:-1]
        else:
 	 #hit anything else, will be shown 
            #self.text.text += pg.key.name(event.key).replace("[", "").replace("]", "")
            #Is it alphanumeric and just one character
            if str(pg.key.name(event.key)).isalnum() and len(str(pg.key.name(event.key))) == 1:
                self.text.text += pg.key.name(event.key)

    def draw(self, surface, panelColor, textColor):

        if self.active:
            temp = panelColor
            panelColor = textColor
            textColor = temp
        self.panel.draw(surface, panelColor)
        self.text.draw(surface, self.panel.rect[0] + 15, self.panel.rect[1] + 15, textColor)

class ViewController:

	  #bare minimum needed to stop the program
    

    def __init__(self):
        self.screen = pg.display.set_mode((800, 600))
        self.palette = {
           'teal':(0,128,128), #teal
            'tur':(79, 185, 175), #yello
            't':(246, 209, 183), #light-yellow
            'dark':(26,36,33) #red
        }
        self.font = pg.font.SysFont("arial", 24)
    
    def shouldAdvance(self, controller):

        #override this
        pass

    def getNextViewController(self):
        
        #override this
        pass

    def handleClick(self):
	#handle clicks  
        
        #override this
        pass

    def handleButtonPress(self, event):
	 #handle  button presses
        
        #override this
        pass
    
    def drawScreen(self, controller):

        #override this
        pass
	#     self.screen.fill(self.palette["teal"])
  
    #     pg.display.update()

class ServerSelect(ViewController):

	#window should be small and simple with a fixed text label stating the ip, input field for port number and connect button
    def __init__(self):

        super().__init__()

        self.screen = pg.display.set_mode((400,200))
        self.IPLabel = Label("IP: 192.168.1.4", self.font)

        portLabel = Label("Port: ", self.font)
        portPanel = Rectangle((100,100), (150,32))
        self.portField = InputField(portLabel, portPanel)

        submitLabel = Label("Connect", self.font)
        submitPanel = Rectangle((100,150), (100,32))
        self.submitButton = Button(submitPanel, submitLabel, self.palette["tur"], self.palette["dark"])
	
	#To track if a port number is entered and if a connect button is pressed
        self.ready = False

    def handleClick(self):
	#Field is activated depending on whether the mouse click was inside it
        
        self.portField.active = self.portField.hasMouse()

        if self.submitButton.hasMouse():
		 #set the flag that it is ready to connect
            self.ready = True
    
    def handleButtonPress(self, event):
        
        if self.portField.active:
            self.portField.handleKeyPress(event)
    
    def shouldAdvance(self, controller):
	#Connection
        #if button is pressed, attempt to connect
        #text.text: the first one is label object and the then textfield within that is the actual string
        #return true if itis connected

        if self.ready:
		 # portNumber=  int(''.join(filter(str.isdigit, self.portField.text.text)))
             portNumber = int(self.portField.text.text.split(": ")[1])
             controller.socket.connect(("192.168.1.4", portNumber))
             return True
        return False
    
    def getNextViewController(self):
	 #it returns the next view controller and returns the reference
        
        return ClientLogin()
    
    def drawScreen(self, controller):
        
        self.screen.fill(self.palette["teal"])

        self.IPLabel.draw(self.screen, 100, 50, self.palette["t"])
        self.portField.draw(self.screen, self.palette["tur"], self.palette["dark"])
        self.submitButton.draw(self.screen)

        pg.display.update()
    
class ClientLogin(ViewController):


    def __init__(self):

        super().__init__()

        self.screen = pg.display.set_mode((400,400))
	#input field for username

        nameLabel = Label("Username: ", self.font)
        namePanel = Rectangle((100,200), (200,32))
        self.nameField = InputField(nameLabel, namePanel)

        submitLabel = Label("Login", self.font)
        submitPanel = Rectangle((100,350), (100,32))
        self.submitButton = Button(submitPanel, submitLabel, self.palette["tur"], self.palette["dark"])
	#To track if a port number is entered and if a connect button is pressed
        self.ready = False

    def handleClick(self):
	#Field is activated depending on whether the mouse click was inside it
        
        self.nameField.active = self.nameField.hasMouse()

        if self.submitButton.hasMouse():
		#set the flag that it is ready to connect
            self.ready = True
    
    def handleButtonPress(self, event):
        
        if self.nameField.active:
            self.nameField.handleKeyPress(event)
    
    def shouldAdvance(self, controller):
	#if button is pressed, extract the text from name and try to send that as a name
        #Send it with Message protocol to tell server the sort of message sent
        #encode the string in a byte format
        #the server will respond whether the name is available or taken

        if self.ready: #If we are ready
            #Grab the name from the text field and send it off
            message = "name:" + self.nameField.text.text.split(": ")[1]
            controller.socket.send(message.encode())

            print(f"Sent message \"{message}\"\n")
            response = controller.socket.recv(4096).decode()
            print(f"Got response\"{response}\"\n")
            #If we got back that we are available read the text and set it as a name
            if response == "available":
		 #if name is available set this name to the client to know who we are
                controller.name = self.nameField.text.text.split(": ")[1]
			#True means move on
                return True
            else:
                #If not available, clear the state of everything and get ready for the next input
                
                self.ready = False
                self.nameField.text.text = "Username: "
        #if name is taken
        return False
    
    def getNextViewController(self):
	#it returns the next view controller and returns the reference
        
        return ChatRoom()
    
    def drawScreen(self, controller):
        
        self.screen.fill(self.palette["teal"])

        self.nameField.draw(self.screen, self.palette["tur"], self.palette["dark"])
        self.submitButton.draw(self.screen)

        pg.display.update()

class ChatRoom(ViewController):


    def __init__(self):

        super().__init__()

        self.screen = pg.display.set_mode((800,600))

        messageLabel = Label("", self.font)
        messagePanel = Rectangle((50,515), (630,75))
        self.messageField = InputField(messageLabel, messagePanel)

        submitLabel = Label("Send", self.font)
        submitPanel = Rectangle((690,515), (100,75))
        self.submitButton = Button(submitPanel, submitLabel, self.palette["tur"], self.palette["dark"])

        self.messagePanel = Rectangle((50,10), (630,490))

        self.ready = False

    def handleClick(self):
        
        self.messageField.active = self.messageField.hasMouse()

        if self.submitButton.hasMouse():
            self.ready = True
    
    def handleButtonPress(self, event):
        
        if self.messageField.active:
            self.messageField.handleKeyPress(event)
    
    def shouldAdvance(self, controller):
        #Handle the receiving of messages

        if self.ready:
            #If message is ready to go, just send them off
            message = "message:" + controller.name + ":" + self.messageField.text.text
            controller.socket.send(message.encode())
            self.messageField.text.text = ""
            self.ready = False
        
        inputs = [controller.socket,]
        outputs = []
        #Grab a message from server
        #Pass list of things as readable
        readable, writable, exceptional = select.select(inputs, outputs, inputs, 0.1)

        for s in readable:
            #If we got message from the server which is a single string with a bunch of different messages so split them off(with the new line character)
            if s is controller.socket:
                #message from server
               messages = s.recv(4096).decode()
               if messages:
                    for message in messages.split("\n"):
                        splitMessage = message.split(":")
                        #If message is valid then append it to the list of messages
                        if splitMessage[0] == "message":
                            controller.messageList.add(splitMessage[1], splitMessage[2])
        
        return False

    def getNextViewController(self):
        
        return None
    
    def drawScreen(self, controller):
        #We have a list of messages and when a new message is added it will be added at the head of the list

        self.screen.fill(self.palette["teal"])

        self.messageField.draw(self.screen, self.palette["tur"], self.palette["dark"])
        self.submitButton.draw(self.screen)
        self.messagePanel.draw(self.screen, self.palette["tur"])

        messageLabel = Label("", self.font)

        messageEntry = controller.messageList.head
        y = 440
        while messageEntry is not None and y > 10:
            messageLabel.text = f"{messageEntry.name}: {messageEntry.message}"
            messageLabel.draw(self.screen, 100, y + 25, self.palette["dark"])
            y -= 50
            messageEntry = messageEntry.next
        pg.display.update()

# Control

class Client:

    def __init__(self):
        pg.init()
	#for testing
        # textObject=label(" ... ",pg.font.SysFont("arial",24))

        # panelObject=None

        # self.testTextLabel=InputField(textObject,panelObject)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = None
        self.messageList = MessageList()

        self.viewController = ServerSelect()
   #Create a window pane in which all of the connected clients will be displayed

    def run(self):

        running = True
        while running:

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.KEYDOWN:
		  #if we get key down event, pass the event onto input field so thet it handles it internally
                    self.viewController.handleButtonPress(event)
                elif event.type == pg.MOUSEBUTTONDOWN:
                    self.viewController.handleClick()
             #Testing
            if self.viewController.shouldAdvance(self):
		#passing the instance of the client and 
                self.viewController = self.viewController.getNextViewController()
            
            self.viewController.drawScreen(self)

    def exit(self):
        pass

#-----------------------------------------------------------------------------#

if __name__ == "__main__":
    client = Client()
    client.run()
    client.exit()

#rather than    spawning a new thread for each client,which requires more resources and doesnt scale well and makes the complexity worse
# the other approach is select which polls the connections to see which ones are ready to go and doesnt block