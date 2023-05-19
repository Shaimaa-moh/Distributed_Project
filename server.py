import socket
from _thread import *
import sys
from player import Player
import pickle
import random
server = "192.168.1.2"  # ip address of my device
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))

except socket.error as e:
    str(e)

# if we give it empty arguments yb2a mmkn y listen to multiple connections
s.listen(2)
print("waiting for connection , Server Started")


players = [Player(250, 479, "./images/car.png"), Player(400, 479,
                                                        "./images/divo.png")]  # store player object on the server

game_end = False
collide = [False, False]



def clientThread(conn, player):  # we want to have multiple connections done at once
    conn.send(pickle.dumps(players[player]))  # send initial player object
    reply = ""
    global game_end
    global collide
    global currentPlayer
    victory = False

    while True:
        try:
            # longer the size of receiving msg , longer it can receive information4
            data = pickle.loads(conn.recv(4096))
            # example :"45 , 67" -> (45,67)
            players[player] = data["Player"]
            collide[player] = data["Crashed"]
            #pos[player]= data
            # reply=data.decode("utf-8") #bec we are receiving encoded info
            if not data:
                print("Disconnected")
                break
            else:  # if there are issues
                car1_x = random.randint(178, 490)
                car2_x = random.randint(178, 490)
                if player == 1:  # if player 1 is playing send to him position of player 0
                    if collide[0] == True and collide[1] == False:
                        victory = True
                    if collide[0] == True and collide[1] == True:
                        game_end = True
                    reply = {
                        "Oponent": players[0],
                        "Connections": currentPlayer,
                        "car1": car1_x,
                        "car2": car2_x,
                        "End_Game": game_end,
                        "Victory": victory
                    }

                else:
                    if collide[0] == False and collide[1] == True:
                        victory = True
                    if collide[0] == True and collide[1] == True:
                        game_end = True

                    reply = {
                        "Oponent": players[1],
                        "Connections": currentPlayer,
                        "car1": car1_x,
                        "car2": car2_x,
                        "End_Game": game_end,
                        "Victory": victory
                    }

                #print("received: ", data)
                #print("Sending :", reply)

            conn.sendall(pickle.dumps(reply))
            if collide[0] == True and collide[1] == True:
                currentPlayer -= 1
                break

        except:
            break

    print("lost conection")
    conn.close()


# server needs to keep track of position of the two players and how many players are connected
currentPlayer = 0
while True:  # coninuously look for connections
    conn, addr = s.accept()  # accepts any upcoming connections
    print("connected successfully to :", addr)
    start_new_thread(clientThread, (conn, currentPlayer))
    currentPlayer += 1
    print(currentPlayer)
