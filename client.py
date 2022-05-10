import socket
import threading

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))

def send_message():
    try:
        message = input(f"{my_username}> ")
        msg = message.encode('utf-8')
        msg_length = len(msg)
        send_length = str(msg_length).encode('utf-8')
        send_length += b' ' * (1024 - len(send_length))
        client.send(send_length)
        client.send(msg)
        print(client.recv(1024).decode('utf-8'))
    except IOError as e:
        print(f"{e}")


my_username = input("Username: ")
client.send(my_username.encode('utf-8'))


while True:
    send_message()
