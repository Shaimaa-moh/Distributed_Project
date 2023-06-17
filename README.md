
# RacingGame_Project 🕹️

A project of a mini racing car game supports the concepts of distributed systems and remote connections.
Throughout this project, we are implementing a 2D racing car game with multiple features.
The system is designed to be distributed system that achieves the main concepts of distribution transparency, reliability, and multiple replicas to maintain fault tolerance.

The game starts by car moving forward, and you must gain score by avoiding collisions with the other racing cars , then the game continues until you or your opponent’s car get crashed. Finally the one who gets the highest score will be the winner.
The game is designed to support real-time playing and viewing by multiple participants, adding chat feature to make all player communicate world widely.

We made two servers, one for the racing game and the other for the chat, in this way we will maintain fault tolerance. So, if the server game fails the chat can stand alone and vice versa.Moreover we used mongo dB, a no sql database that will serve our demands in achieving replication consistency.
![hello to our game.](https://drive.google.com/file/d/1TWDSudZXq6VnW7k5M5lY_T863IuMEsdM/view)

## How to run the project
1) Download the Project Directory in your Visual Studio
![image](https://github.com/Shaimaa-moh/Distributed_Project/assets/67200068/d69f6b58-fbb2-4101-bcc0-bce96810bd3d)
2) Adjust server.py to connect to your local network
![image](https://github.com/Shaimaa-moh/Distributed_Project/assets/67200068/9e264752-e9c7-43b9-9091-64348be01272)
3) Adjust network.py to connect to your local network
![image](https://github.com/Shaimaa-moh/Distributed_Project/assets/67200068/b37d5afd-d158-40bc-8a35-820f308ef58e)
4) Adjust the Chat Server (Chat/serv.py) to connect to your local newtork and chattest.py
![image](https://github.com/Shaimaa-moh/Distributed_Project/assets/67200068/29c8e80f-d11a-4076-b884-ec9bc238ffbc)
5) Run the Game server by **python server.py** in th terminal
![image](https://github.com/Shaimaa-moh/Distributed_Project/assets/67200068/ee4109f3-095d-4753-81ba-2fce5c8992a9)
6) Run the Chat server by **python Chat/serv,py** in the terminal
![image](https://github.com/Shaimaa-moh/Distributed_Project/assets/67200068/6ab02c58-5714-4978-8e46-469b71515a82)
7) Run the game by running **python racing.py** in the terminal and **enjoy our Game**
![image](https://github.com/Shaimaa-moh/Distributed_Project/assets/67200068/6775d6f1-0650-4e01-b9f1-66cfd699cf6b)


---
---



## Game ScreenShots
### The Home Screen
![image](https://github.com/Shaimaa-moh/Distributed_Project/assets/67200068/83374a2c-0462-4b11-8c5c-fd4d4a882a8a)
---
---
### The Waiting Screen
![image](https://github.com/Shaimaa-moh/Distributed_Project/assets/67200068/9f69902b-397e-47d6-a400-8c600e22f489)
---
---
### The Game Run
![image](https://github.com/Shaimaa-moh/Distributed_Project/assets/67200068/161d37f2-24a9-4cef-ba1c-b682e46069fc)
---
---
### Player Chat
![image](https://github.com/Shaimaa-moh/Distributed_Project/assets/67200068/228fb288-5676-4b09-9e36-dc9d39b34fa8)
---
---




## A)Game Implementation
### racing.py main functions
You have to install pygame library :
> pip install pygame

- The code defines various functions like introImg, play, introscreen, waiting, countdown, redrawScreen, show_score, show_highscore, victory, and gameover. These functions handle different aspects of the game such as displaying the intro screen, waiting for other players, counting down before the game starts, updating the game screen, showing scores, handling victory and game over scenarios, etc.
   
- The gameloop function is the main game loop where the gameplay logic is implemented. It sets up the background image, initializes game variables, handles player input, updates player position, checks for collisions, and manages game over and victory conditions.
   
- The main code starts by loading necessary game assets like images and sounds. It then calls the introscreen function to display the introductory screen and wait for user input to start the game.
   
- When the user clicks the "PLAY" button, the gameloop function is called to start the game.
   
- Inside the gameloop, it sets up the game environment, initializes player and enemy car positions, starts the countdown, and enters the game loop where player input and game updates are processed.
   
- The game loop runs until the game is over or the player wins. It checks for collisions, updates player and enemy car positions, displays the game screen, and handles user input.
    
- If a collision occurs, the game enters the game over state and calls the gameover function to display the game over screen with the final score and highscore. The player has the option to restart the game or exit.
    
- If the player wins, the game enters the victory state and calls the victory function to display the victory screen with the final score and highscore. The player has the option to restart the game or exit.
 ---
 
### server.py
You have to install mongodb library :
Type in your terminal 
> $ pip install pymongo 

You have to install socketio library :
> $ pip install socketio

The server is responsible for listening for client connections, bind the socket with our desired ip and port number. It receives and sends data between clients like data of player object and store their positions in list , and that helps performing multi playing concept , if player  0  is playing reply  by  its position to player 1  and vice versa .

Then interacts with a Mongo DB database used for replication. Also we used pickle process which is a process whereby a python object hierarchy is converted into byte stream, and it facilitates sending object of the players.

 ---
### Network.py
- Creating network class which is responsible for connecting to our server using the socket module in Python.
- Invoking the connect() method to establish a connection to our server, initializing the self.client attribute with a new socket object, and stores the return value in the self.p attribute.
- The getP() method which is obtain the data received from the server after a successful connection. It returns self.p which was set by connect() method.
- The connect() method which is responsible to connect to the server and receive data from the server. It connects to the server using the socket object's connect() method and passes the server’s IP address and the port number which are stored in self.addr
- The send() method uses the pickle.dumps() function to serialise the data argument before sending the serialised data to the server using the socket object's send() method.

  ---
  ---
  ## B)Chat Feature Implementation
  ### Serv.py (The server side)
First of all the socket connection is set to bind to an IP and port number, we set the port number to be static in both client and server to be= 3000.
- The run method is the main loop of the server. It listens for incoming connections, reads messages from clients, handles client name updates, and sends messages to all connected clients.
- The method starts by creating a list of readable, writable, and exceptional connections using select.select().
- If the server socket is readable, it accepts the incoming connection, sets it to non-blocking, adds it to the inputs list, and adds the client to the clientList.
- If a client connection is readable, it receives a message from the client. If the message starts with "name", it checks if the name is available in the clientList. If available, it updates the client's name and sends back a response. If not available, it sends back a "taken" response.
- If the message is not a name update, it adds the message to the messageBuffer and updates the writeable list with all client connections.
- It iterates over each connection in the writeable list, which contains the client connections that are ready for writing.
- In the writable connections loop, it retrieves the messages from the messageBuffer and sends them to all connected clients. It initializes an empty string called message to hold the concatenated messages. It starts iterating over the linked list of messages in the messageBuffer using the messageEntry variable, which is set to the head of the list. For each message entry, it appends the text of the message followed by a newline character ('\n') to the message string. This creates a single string where each message is separated by a newline character. After iterating through all the message entries, it encodes the message string into bytes using the encode() method. Encoding is necessary to convert the string into a format that can be sent over the network.
- In the exceptional connections loop, it handles dropped connections, removes the disconnected client from the clientList, and closes the socket.
  ---
  ### chattest.py (The Client Side)
- The __init__ method initializes a Chat object. It creates and configures a Tkinter window (self.win) for the chat interface, sets up the layout of the chat window, starts a separate thread for receiving messages, and starts the main event loop of the Tkinter window.
- The layout method sets up the visual layout of the chat window using various Tkinter widgets such as labels, text areas, entry fields, and buttons.
- The write method is called when the user clicks the send button. It retrieves the message entered by the user, clears the input field, and starts a separate thread for sending the message.
- The receive method runs in a continuous loop and receives messages from the server. It splits the received messages into separate messages using newline characters ('\n') as separators. Each message is then added to the messageList and displayed in the text area of the chat window.
- The sendMessage method sends messages to the server. It retrieves the user's message, combines it with the user's name, and sends it to the server
  

