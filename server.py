import socket
from _thread import *
import sys
from player import Player
import pickle
import random
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
server = "13.51.170.207"  # ip address of my device
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))

except socket.error as e:
    str(e)

# if we give it empty arguments yb2a mmkn y listen to multiple connections

print("waiting for connection , Server Started")


uri = "mongodb+srv://shimomoh693:distributed_game@cluster0.g3zfuko.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
db = client['Distributed_Project2023']
collections = db['Players']
players = [Player(250, 479, "./images/car.png"), Player(400, 479,
                                                        "./images/divo.png")]  # store player object on the server
s.listen()
game_end = False
collide = [False, False]

score = [0, 0]  # for two players


def clientThread(conn, player):  # we want to have multiple connections done at once
    conn.send(pickle.dumps(players[player]))  # send initial player object

    reply = ""
    global score
    global game_end
    global collide

    global currentPlayer
    global collections  # like table players

    victory = False

    while True:
        try:
            # longer the size of receiving msg , longer it can receive information4
            data = pickle.loads(conn.recv(4096))  # object from player
            if data["Game"] == "start":
                document = collections.find_one(
                    {'username': data["Username"]})  # see username in db or not
                if document is None:
                    collections.insert_one(
                        {'username': data["Username"], 'highscore': 0})

            # example :"45 , 67" -> (45,67)
            players[player] = data["Player"]
            collide[player] = data["Crashed"]
            score[player] = data["score"]
            # pos[player]= data
            # reply=data.decode("utf-8") #bec we are receiving encoded info
            if not data:
                print("Disconnected")
                break
            else:  # if there are issues
                car1_x = random.randint(178, 490)
                car2_x = random.randint(178, 490)
                if player == 1:  # if player 1 is playing ,send to him position of player 0
                    if collide[0] == True and collide[1] == False:
                        victory = True
                    if collide[0] == True and collide[1] == True:
                        game_end = True
                    reply = {
                        "Oponent": players[0],
                        "Connections": currentPlayer,
                        "car1": car1_x,  # collision cars
                        "car2": car2_x,
                        "End_Game": game_end,
                        "Victory": victory,
                        "Highscore": document['highscore'],
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
                        "Victory": victory,
                        "Highscore": document['highscore'],
                    }

                print("received: ", data)
                #print("Sending :", reply)

            conn.sendall(pickle.dumps(reply))
            if collide[0] == True and collide[1] == True:
                document_final = collections.find_one(
                    {'username': data["Username"]})  # see username in db or not
                # to take score of player 1 or 2
                if (document_final['highscore'] < score[player]):
                    update = {'$set': {'highscore': score[player]}}
                    collections.update_one(document_final, update)
                conn.sendall(pickle.dumps(reply))
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
