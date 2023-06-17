
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
6) Run the Chate server by **python Chat/serv,py** in the terminal
![image](https://github.com/Shaimaa-moh/Distributed_Project/assets/67200068/6ab02c58-5714-4978-8e46-469b71515a82)



## racing.py main functions
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
   
## server.py
You have to install mongodb library :
Type in your terminal 
> $ pip install pymongo 

You have to install socketio library :
> $ pip install socketio

The server is responsible for listening for client connections, bind the socket with our desired ip and port number. It receives and sends data between clients like data of player object and store their positions in list , and that helps performing multi playing concept , if player  0  is playing reply  by  its position to player 1  and vice versa .

Then interacts with a Mongo DB database used for replication. Also we used pickle process which is a process whereby a python object hierarchy is converted into byte stream, and it facilitates sending object of the players.
 
## Network.py
- Creating network class which is responsible for connecting to our server using the socket module in Python.
- Invoking the connect() method to establish a connection to our server, initializing the self.client attribute with a new socket object, and stores the return value in the self.p attribute.
- The getP() method which is obtain the data received from the server after a successful connection. It returns self.p which was set by connect() method.
- The connect() method which is responsible to connect to the server and receive data from the server. It connects to the server using the socket object's connect() method and passes the server’s IP address and the port number which are stored in self.addr
- The send() method uses the pickle.dumps() function to serialise the data argument before sending the serialised data to the server using the socket object's send() method.
  

