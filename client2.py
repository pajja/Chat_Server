import socket
import sys
import threading
import time
import os


PORT = 5378
SERVER = socket.gethostbyname(socket.gethostname())
BUFFER = 4096
# Make a dynamic buffer
global client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Trying to connect to ", SERVER+":"+str(PORT))
host_port = (SERVER, PORT)
client.connect(host_port)
print("Connected")

handshaked = False
waitingResp = False

username = ""
quit = False

thread = threading.Thread()
threadListen = threading.Thread()

def whoInServer(msg):
    print("User list :", msg)

def newMessage(user, message):
    if user != username:
        print("\n@"+user+" "+message)

#Recieves messages and parses it from the server
def keyParser(message:str, name):
    if name == "":
        login()
    global waitingResp
    msgArr = message.split(" ")
    key = msgArr[0].strip()

    if key == "WHO-OK":
        waitingResp = False
        userList = ""
        for i in range(1, len(msgArr)):
            userList += msgArr[i] + " "
        whoInServer(userList)
    elif key == "SEND-OK":
        waitingResp = False
        print("Message Sent")
    elif key == "DELIVERY":
        global connSender
        connSender = client.recv(1024).decode("UTF-8")
        recvMsg = ""
        for i in range(2, len(msgArr)):
            recvMsg += msgArr[i] + " "
        print(f"DELIVERY from {connSender}: {recvMsg}")
        newMessage(msgArr[1], recvMsg)
    elif key == "IN-USE":
        print("Username already in use. Please pick another username")
        global handshaked
        handshaked = False
        login()
    elif message == "BUSY\n":
        waitingResp = False
        print("Server is Busy please wait.")
        os._exit(1)
    elif message == "BAD-RQST-HDR\n":
        waitingResp = False
        print("Header sent to the server has faults")
    elif message == "BAD-RQST-BODY\n":
        waitingResp = False
        print("Body sent to the server has faults")
    elif message == "UNKNOWN\n":
        print("UNKNOWN")
        os._exit(1)
        reconnectWithoutClose()
    elif message == "HELLO "+name + "\n":
        handshaked = True


def messageToCommandConverter(msg):
    if msg == "!quit":
        print("Quitting")

        os._exit(1)

    elif msg == "!who":
        return "WHO\n"
    else:
        msgArr = msg.split()
        if msgArr[0][0] == "@":
            poppers = list(msgArr[0]) # Pop the @ from the usertag
            poppers.pop(0)
            name = ""
            for i in poppers:
                name += i
            msgArr[0] = name

            totalMsg = ""
            for i in msgArr:
                totalMsg += i + " "

            return "SEND " + totalMsg + "\n"
        else:
            print("Unknown command. Please enter an existing command.")
            return ''



def sendNewMessage(a):
    global handshaked
    global waitingResp
    while True:
        if not handshaked:
            break
        try:
            newMsg = input(a+": ")
            newMsg = messageToCommandConverter(newMsg)
            while newMsg == '':
                newMsg = input(a + ": ")
                newMsg = messageToCommandConverter(newMsg)
        except:
            continue


        if not handshaked:
            break

        client.send(newMsg.encode("UTF-8"))
        waitingResp = True

        while waitingResp:
            time.sleep(0.1)
        if quit:
            print("Quitting Sender")
            break

def reconnectToServer():
    client.close()
    client.connect((SERVER, PORT))

def reconnectWithoutClose():
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))

def serverListen():
    while True:
        if quit:
            print("Quitting Listener")

            break
        character = ""
        recvMsg = ""
        while "\n" not in recvMsg:
            character = client.recv(1).decode("UTF-8")
            recvMsg += character

        # if recvMsg.split()[0] == "DELIVERY":
        #     global connSender
        #     connSender = client.recv(1024).decode("UTF-8")

        keyParser(recvMsg, username)


def login():
    global handshaked
    global username
    global thread
    while not handshaked:
        name = input("What's your name:")
        txt = "HELLO-FROM " + name + "\n"

        client.sendall(txt.encode("UTF-8"))

        msg = client.recv(BUFFER)
        if not msg:
            client.close()
            client.connect((SERVER, PORT))

        else:
            msg = msg.decode("UTF-8")
            print(msg)
            keyParser(msg, name)

    username = name

    global thread
    thread = threading.Thread(target=sendNewMessage, args=((name,)))
    thread.start()

    global threadListen
    threadListen = threading.Thread(target=serverListen)
    threadListen.start()

login()


while not quit:
    time.sleep(1)


#thread.join()
#threadListen.join()








# import socket
# import sys
# import threading
# import time
# import os
#
#
# PORT = 5378
# SERVER = socket.gethostbyname(socket.gethostname())
# BUFFER = 4096
# # Make a dynamic buffer
# global client
# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# print("Trying to connect to ", SERVER+":"+str(PORT))
# host_port = (SERVER, PORT)
# client.connect(host_port)
# print("Connected")
#
# handshaked = False
# waitingResp = False
#
# username = ""
# quit = False
#
# thread = threading.Thread()
# threadListen = threading.Thread()
#
# def whoInServer(msg):
#     print("User list :", msg)
#
# def newMessage(user, message):
#     if user != username:
#         print("\n@"+user+" "+message)
#
# #Recieves messages and parses it from the server
# def keyParser(message:str, name):
#     if name == "":
#         login()
#     global waitingResp
#     msgArr = message.split(" ")
#     key = msgArr[0].strip()
#
#     if key == "WHO-OK":
#         waitingResp = False
#         userList = ""
#         for i in range(1, len(msgArr)):
#             userList += msgArr[i] + " "
#         whoInServer(userList)
#     elif key == "SEND-OK":
#         waitingResp = False
#         print("Message Sent")
#     elif key == "DELIVERY":
#         recvMsg = ""
#         for i in range(2, len(msgArr)):
#             recvMsg += msgArr[i] + " "
#
#         newMessage(msgArr[1], recvMsg)
#     elif key == "UNKNOWN":
#         print("Destination user is not currently logged in")
#         global handshaked
#         handshaked = False
#         login()
#
#     elif message == "BUSY\n":
#         waitingResp = False
#         print("Server is Busy please wait.")
#     elif message == "BAD-RQST-HDR\n":
#         waitingResp = False
#         print("Header sent to the server has faults")
#     elif message == "BAD-RQST-BODY\n":
#         waitingResp = False
#         print("Body sent to the server has faults")
#     elif message == "IN-USE\n":
#         print("Username already in use. Please pick another username")
#         handshaked = False
#         login()
#         reconnectWithoutClose()
#     elif message == "HELLO "+name + "\n":
#         handshaked = True
#
#
# def messageToCommandConverter(msg):
#     if msg == "!quit":
#         print("Quitting")
#
#         os._exit(1)
#
#     elif msg == "!who":
#         return "WHO\n"
#     else:
#         msgArr = msg.split()
#         if msgArr[0][0] == "@":
#             poppers = list(msgArr[0]) # Pop the @ from the usertag
#             poppers.pop(0)
#             name = ""
#             for i in poppers:
#                 name += i
#             msgArr[0] = name
#
#             totalMsg = ""
#             for i in msgArr:
#                 totalMsg += i + " "
#
#             return "SEND " + totalMsg + "\n"
#         else:
#             print("Unknown command. Please enter an existing command.")
#             return ''
#
#
#
# def sendNewMessage(a):
#     global handshaked
#     global waitingResp
#     while True:
#         if not handshaked:
#             break
#         try:
#             newMsg = input(a+": ")
#             newMsg = messageToCommandConverter(newMsg)
#             while newMsg == '':
#                 newMsg = input(a + ": ")
#                 newMsg = messageToCommandConverter(newMsg)
#         except:
#             continue
#
#
#         if not handshaked:
#             break
#
#         client.send(newMsg.encode("UTF-8"))
#         waitingResp = True
#
#         while waitingResp:
#             time.sleep(0.1)
#         if quit:
#             print("Quitting Sender")
#             break
#
# def reconnectToServer():
#     client.close()
#     client.connect((SERVER, PORT))
#
# def reconnectWithoutClose():
#     global client
#     client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client.connect((SERVER, PORT))
#
# def serverListen():
#     while True:
#         if quit:
#             print("Quitting Listener")
#
#             break
#         character = ""
#         recvMsg = ""
#         while "\n" not in recvMsg:
#             character = client.recv(1).decode("UTF-8")
#             recvMsg += character
#
#
#
#         keyParser(recvMsg, username)
#
#
# def login():
#     global handshaked
#     global username
#     global thread
#     while not handshaked:
#         name = input("What's your name:")
#         txt = "HELLO-FROM " + name + "\n"
#
#         client.sendall(txt.encode("UTF-8"))
#
#         msg = client.recv(BUFFER)
#         if not msg:
#             client.close()
#             client.connect((SERVER, PORT))
#
#         else:
#             msg = msg.decode("UTF-8")
#             print(msg)
#             keyParser(msg, name)
#
#
#
#
#     username = name
#
#     global thread
#     thread = threading.Thread(target=sendNewMessage, args=((name)))
#     thread.start()
#
#     global threadListen
#     threadListen = threading.Thread(target=serverListen)
#     threadListen.start()
#
# login()
#
#
# while not quit:
#     time.sleep(1)
#
#
# #thread.join()
# #threadListen.join()
