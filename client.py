import socket
import sys

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))


def keywords(msg):
    if msg == "!quit":
        print(f"DISCONNECTED [{my_username}]")
        sys.exit()


def send_message():
    try:
        message = input(f"{my_username}> ")
        while message == '':
            message = input(f"{my_username}> ")
        msg = message.encode('utf-8')
        msg_length = len(msg)
        send_length = str(msg_length).encode('utf-8')
        send_length += b' ' * (1024 - len(send_length))
        client.send(send_length)
        client.send(msg)
        keywords(message)
        response = client.recv(1024).decode('utf-8')
        print(response)
    except:
        sys.exit()


my_username = input("Username: ")
client.send(my_username.encode('utf-8'))
msgUser = ''
first = True
while msgUser != "> Username is good.":
    if first == False:
        my_username = input("Username: ")
        client.send(my_username.encode('utf-8'))
    msgUser = client.recv(1024).decode('utf-8')
    if msgUser == "BUSY.":
        print("BUSY.")
        keywords("!quit")
    print(msgUser)
    first = False


while True:
    send_message()
