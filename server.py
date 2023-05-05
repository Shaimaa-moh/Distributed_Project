import socket
from _thread import * 
import sys
from player import Player 
import pickle
server="192.168.1.5" #ip address of my device
port=5555

s=socket.socket(socket.AF_INET , socket.SOCK_STREAM)

try:
    s.bind((server,port))
    
except socket.error as e:
    str(e)
    
s.listen(2) #if we give it empty arguments yb2a mmkn y listen to multiple connections
print("waiting for connection , Server Started")



players = [ Player(0,0,50,50,(255,0,0)),Player(100,100,50,50,(0,0,255))] #store player object on the server

def clientThread(conn , player ): #we want to have multiple connections done at once
    conn.send(pickle.dumps(players[player])) # send initial player object
    reply=""
    while True:
        try :
            data = pickle.loads(conn.recv(2048))#longer the size of receiving msg , longer it can receive information4
            # example :"45 , 67" -> (45,67)
            players[player] =data
            #pos[player]= data
            #reply=data.decode("utf-8") #bec we are receiving encoded info
            if not data:
                print("Disconnected")
                break
            else: #if there are issues
                if player==1: # if player 1 is playing send to him position of player 0
                    reply =players[0]
                    
                else :
                    reply =players[1]
                    
                print("received: ",data)
                print("Sending :",reply)
            
            conn.sendall(pickle.dumps(reply))
              
        except:
            break
        
    print("lost conection")
    conn.close()        
# server needs to keep track of position of the two players and how many players are connected
currentPlayer = 0
while True: # coninuously look for connections
    conn,addr = s.accept() #accepts any upcoming connections
    print("connected successfully to :", addr)
    start_new_thread(clientThread,(conn , currentPlayer))
    currentPlayer += 1
    
    