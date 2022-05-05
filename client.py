import socket

HEADER = 64
IP = socket.gethostbyname(socket.gethostname())
PORT = 5050

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PORT))

def send_message(msg):
    try:
        message = msg.encode('utf-8')
        msg_length = len(message)
        send_length = str(msg_length).encode('utf-8')
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)
        print(client.recv(2048).decode('utf-8'))
    except IOError as e:
        print(f"{e}")


my_username = input("Username: ")
# trying to store a username somehow
#client.send(my_username.encode('utf-8'))
#print(client.recv(2048).decode('utf-8'))

connected = True
while connected:
    message = input(f"{my_username}> ")
    send_message(message)
    if message == "!quit":
        connected = False
