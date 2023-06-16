
# Distributed_Project

A project of a mini racing car game supports the concepts of distributed systems and remote connections.
Throughout this project, we are implementing a 2D racing car game with multiple features.
The system is designed to be distributed system that achieves the main concepts of distribution transparency, reliability, and multiple replicas to maintain fault tolerance.

The game starts by car moving forward, and you must gain score by avoiding collisions with the other racing cars , then the game continues until you or your opponent’s car get crashed. Finally the one who gets the highest score will be the winner.
The game is designed to support real-time playing and viewing by multiple participants, adding chat feature to make all player communicate world widely.

We made two servers, one for the racing game and the other for the chat, in this way we will maintain fault tolerance. So, if the server game fails the chat can stand alone and vice versa.Moreover we used mongo dB, a no sql database that will serve our demands in achieving replication consistency.
![hello to our game.](https://drive.google.com/drive/u/0/my-drive)

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

