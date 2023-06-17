import socket
import threading
from tkinter import *
from tkinter import font
from tkinter import ttk

PORT = 5555
SERVER = "16.170.217.190"
ADDRESS = (SERVER, PORT)
# Create a new client socket
# and connect to the server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)
# GUI class for the chat


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

        # do we have an empty list?
        if self.head is None:
            self.head = newMessage

        else:
            newMessage.next = self.head
            self.head = newMessage


class Chat:
    def __init__(self, name):
        # chat win which is currently hidden
        self.win = Tk()
        self.win.withdraw()
        self.layout(name)
        self.messageList = MessageList()
        rcv = threading.Thread(target=self.receive)
        rcv.start()
        self.win.mainloop()

    # constructor method

    def layout(self, name):
        self.name = name
        # to show chat window
        self.win.deiconify()
        self.win.title("Chat")
        self.win.resizable(width=False, height=False)
        self.win.configure(width=470, height=550, bg="#E2F2EF")
        self.labelHead = Label(
            self.win,
            bg="#E2F2EF",
            fg="#000000",
            text="Chat",
            font="Arial 14 bold",
            pady=5,
        )
        self.labelHead.place(relwidth=1)
        self.text_area = Text(
            self.win,
            width=20,
            height=2,
            bg="#7FBBB2",
            fg="#000000",
            font="Arial 15",
            padx=5,
            pady=5,
        )
        self.text_area.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_area.config(cursor="arrow")
        self.labelBottom = Label(self.win, bg="#7FBBB2", height=80)
        self.labelBottom.place(relwidth=1, rely=0.775)
        self.entry_Msg = Entry(self.labelBottom, font="Arial 13")
        self.entry_Msg.place(relwidth=0.74, relheight=0.06, rely=0.008,
                             relx=0.011)
        self.entry_Msg.focus()
        # create a Send Button
        self.send_Button = Button(
            self.labelBottom,
            text="Send",
            font="Arial 10 bold",
            width=10,
            bg="#E4DED0",
            fg="#000000",
            command=lambda: self.write(self.entry_Msg.get()),
        )
        self.send_Button.place(relx=0.77, rely=0.035, relheight=0.02,
                               relwidth=0.22)
        # create a scroll bar
        scrollbar = Scrollbar(self.text_area)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.config(command=self.text_area.yview)
        self.text_area.config(state=DISABLED)
    # function to start thread for sending messages

    def write(self, msg):
        self.text_area.config(state=DISABLED)
        self.msg = msg
        self.entry_Msg.delete(0, END)
        snd = threading.Thread(target=self.sendMessage)
        snd.start()
    # function to receive messages

    def receive(self):
        while True:
            messages = client.recv(4096).decode()
            if messages:
                for message in messages.split("\n"):
                    if message == '':
                        break
                    splitMessage = message.split(":")
                    # If message is valid then append it to the list of messages
                    if splitMessage is not None:
                        print(splitMessage)
                        self.messageList.add(
                            splitMessage[0], splitMessage[1])
                        self.text_area.config(state=NORMAL)
                        self.text_area.insert(END, message + "\n\n")
                        self.text_area.config(state=DISABLED)
                        self.text_area.see(END)
            # try:
            #     message = client.recv(1024).decode("utf-8")
            #     # if the messages from the server is NAME send the client's name
            #     if message == "NAME":
            #         client.send(self.name.encode("utf-8"))
            #     else:
            #         # insert messages to text box
            #         self.text_area.config(state=NORMAL)
            #         self.text_area.insert(END, message + "\n\n")
            #         self.text_area.config(state=DISABLED)
            #         self.text_area.see(END)
            # except:
            #     # an error will be printed on the command line or console if there's an error
            #     print("An error occurred!")
            #     client.close()
            #     break
    # function to send messages

    def sendMessage(self):
        self.text_area.config(state=DISABLED)
        while True:
            message = self.name + ":" + self.msg
            client.send(message.encode())
            break


c = Chat('Aya')
