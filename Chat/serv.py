import pygame as pg
import socket
import select
# MVC
# Model


class client:
    # Save clients as a linked List
    def __init__(self, name, connection):
        self.name = name
        self.next = None
        self.connection = connection


class ClientList:

    def __init__(self):
        self.head = None

    def add(self, name, connection):
        newClient = client(name, connection)

        # Check if the list is empty
        if self.head is None:
            self.head = newClient

        else:
            newClient.next = self.head
            self.head = newClient

    def nameAvailable(self, name):
        client = self.head
        while client is not None:
            if client.name == name:
                return False
            client = client.next
        return True

    def getByConnection(self, connection):
     # put in connection and check through the list of clients and get the client which corresponds to that connection
        client = self.head
        while client is not None:
            if client.connection == connection:
                return client
            client = client.next
        return None

    def drop(self, client):

        temp = self.head
        if temp is None or client is None:
            return

        if temp == client:
            # Head of the list is the client
            # set the head to the next thing skipping the client and it will be automatically deleted
            self.head = temp.next
            return

        while temp:
            if temp.next == client:
                # If next thing matched the client
                temp.next = client.next
                return
            temp = temp.next


class Message:

    def __init__(self, text):
        self.text = text
        self.next = None


class MessageList:
    # When one of the clients sends a message or a bunch of messages we want to save them then send them off to all of the clients

    def __init__(self):
        self.head = None

    def add(self, text):

        newMessage = Message(text)

        # do we have an empty list?
        if self.head is None:
            self.head = newMessage

        else:
            newMessage.next = self.head
            self.head = newMessage

# View
# creating gui elements


class label:
    def __init__(self, text, font):
        self.text = text
        self.font = font

    def draw(self, surface, x, y, color):
        # GUI
        # render the font that takes the text input, bounces it down an image, blit is we copy that image of the text  onto the screen
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
        (x, y) = pg.mouse.get_pos()
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
        self.text.draw(
            surface, self.panel.rect[0] + 15, self.panel.rect[1] + 15, textColor)


class ViewController:
    def __init__(self, port):
        self.screen = pg.display.set_mode((800, 600))
        self.palette = {
            'teal': (0, 128, 128),  # teal
            'tur': (79, 185, 175),  # yello
            't': (246, 209, 183),  # light-yellow
            'dark': (26, 36, 33)  # red

        }
        self.font = pg.font.SysFont('arial', 24)

        self.clientBox = Rectangle((50, 40), (600, 400))

        self.quitButton = Button(
            panel=Rectangle((100, 500), (200, 32)),
            text=label("Shut Down Server", self.font),
            onColor=self.palette["dark"],
            offColor=self.palette['t']
        )
        self.clientLabel = label("...", self.font)
        self.portLabel = label(f"Listening on port {port}", self.font)

    def drawScreen(self, clientList):
        self.screen.fill(self.palette["teal"])

        # Draw client box

        self.clientBox.draw(self.screen, self.palette["tur"])
        client = clientList.head
        y = 50
        # Loop to check the name of the label and drop it down and draw it for each client until the end of the list

        while client is not None:
            self.clientLabel.text = client.name
            self.clientLabel.draw(self.screen, 100, y+25, self.palette['dark'])
            y += 50
            client = client.next
        self.portLabel.draw(self.screen, 300, 20, self.palette['t'])
        self.quitButton.draw(self.screen)
        pg.display.update()

    def shouldExit(self):
        return self.quitButton.hasMouse()
# Control


class Server:
    def __init__(self):
        pg.init()

        # self.clientList.add('Mary')
        # self.clientList.add('bob')
        # ipconfig on commandline
        self.host = '13.51.234.66'
        self.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)  # IP uses 4 bytes
    # It doesnt block other processes if it waits to accept a connection
        self.socket.setblocking(0)
        self.socket.bind((self.host, 3000))
        # self.port=self.socket.getsockname()[1] #we get the port number
        self.port = 3000
        # self.viewcontroller=ViewController(self.port)
        self.clientList = ClientList()

 # Create a window pane in which all of the connected clients will be displayed

    def run(self):

        self.socket.listen()
        # use list to keep track of which devices or connections we can read from or work with and which ones can output data
        inputs = [self.socket]
        outputs = []
        clientNumber = 0
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    running = not self.viewcontroller.shouldExit()
            # read from a client
            # call select given devices the first one is a list of things we can read from, lists to write to and list of things that could cause an exception
            # exception as if  client suddenly disconnect would be appended to the exception list

            readable, writeable, exceptional = select.select(
                inputs, outputs, inputs, 0.1)
            # timeout = 0.1 which is the number of seconds the server waits
            # Every time the server updates, set up a new sets of messages that will be rewritten everytime and flush them out to the clients
            messageBuffer = MessageList()
            for s in readable:
                # select goes when a device is readable which is there is a connection ready
                if s is self.socket:
                    # give server time to form a connection
                    # listen on server
                    connection, client_address = s.accept()
                    connection.setblocking(0)
                    inputs.append(connection)
                    self.clientList.add(f"Client {clientNumber}", connection)
                    clientNumber += 1
                else:
                    # client connection
                    message = s.recv(4096).decode()
                    if message:
                        # Check client name,either update or tell the client the name is taken
                        print(f"Got message \"{message}\"\n ")
                        if message.split(":")[0] == "name":
                            if self.clientList.nameAvailable(message.split(":")[0]):
                                client = self.clientList.getByConnection(s)
                                client.name = message.split(":")[0]
                                response = "available".encode()
                            else:
                                response = "taken".encode()
                            s.send(response)
                        # elif message.split(":")[0] == "message":
                        else:
                            splitMessage = message.split(":")
                            # message:bob:hello
                            # Split up and store the info in a string and pass it to the message buffer to be stored
                            messageBuffer.add(
                                f"{splitMessage[0]}:{splitMessage[1]}")
                            client = self.clientList.head
                            while client is not None:
                                # When getting a single message, set up every single client in the list to write
                                # */The next time we got  a message if its witthin the same time cycle
                                # the clients will be already in the queue, that messsage will be added to the queue and queued up clients will get that messages*/
                                if client.connection not in writeable:
                                    writeable.append(client.connection)
                                client = client.next
                    else:

                        exceptional.append(s)
            for s in writeable:
                # Looking through the buffered messages and append them into a single string seperated with a new line
                messageEntry = messageBuffer.head
                message = ""
                # On the client side get that string and split it into different messages based on the new line character
                while messageEntry is not None:
                    message += f"{messageEntry.text}\n"
                    messageEntry = messageEntry.next
                message = message.encode()

                if s is not self.socket:
                    # Send the chat messages to all of the clients
                    s.send(message)
            for s in exceptional:
                # TCP

                client = self.clientList.getByConnection(s)
                # When client connection is dropped
                print(f"Lost connection with {client.name}")
                # When dropped remove the client from the connection
                if s in inputs:
                    inputs.pop(inputs.index(s))
                if s in outputs:
                    outputs.pop(outputs.index(s))
                s.close()

                self.clientList.drop(client)
            # self.viewcontroller.drawScreen(self.clientList)

    def exit(self):
        pass


if __name__ == '__main__':
    server = Server()
    server.run()
    server.exit()


# rather than    spawning a new thread for each client,which requires more resources and doesnt scale well and makes the complexity worse
# the other approach is select which polls the connections to see which ones are ready to go and doesnt block
