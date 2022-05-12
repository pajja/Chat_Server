import socket
import threading
import sys

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))

client_list = []
username_list = []


def keywords(conn, msg, username):
    try:
        if msg[0] == "@":
            firstWord = msg.split()[0]
            sendUsername = firstWord.replace('@', '')
            message = msg.replace(firstWord, '')
            if sendUsername in username_list:
                index = username_list.index(sendUsername)
                connSend = client_list[index]
                broadcast(message, connSend, username)
                conn.send(bytes("SEND-OK", 'utf-8'))
            else:
                conn.send(bytes(f"[{firstWord}] UNKNOWN", 'utf-8'))
            conn.send(bytes(" ", 'utf-8'))
        elif msg == "!who":
            print(f"LIST_OF_CLIENTS {username_list}")
            data = f"LIST_OF_CLIENTS {username_list}"
            conn.send(bytes(data, 'utf-8'))
        elif msg == "!quit":
            print(f"DISCONNECTED [{username}]")
            client_list.remove(conn)
            username_list.remove(username)
        elif msg.split()[0] == "HELLO-FROM":
            data = f"HELLO {username}"
            conn.send(bytes(data, 'utf-8'))
        else:
            conn.send(bytes(" ", 'utf-8'))
    except:
        sys.exit()


def handle_client(conn, username):
    while True:
        try:
            msg_length = conn.recv(1024).decode('utf-8')
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode('utf-8')
                print(f"{username}> {msg}")

                threadKeywords = threading.Thread(target=keywords, args=(conn, msg, username))
                threadKeywords.start()
            else:
                if conn in client_list:
                    client_list.remove(conn)
                    break
        except:
            continue


def broadcast(msg, conn, username):
    conn.send(bytes(f"{username}> {msg}", 'utf-8'))


def start():
    server.listen()
    print(f"LISTENING ON {SERVER}")
    while True:
        conn, addr = server.accept()
        client_list.append(conn)
        username = conn.recv(1024).decode('utf-8')
        first = True
        while username in username_list:
            if first == False:
                username = conn.recv(1024).decode('utf-8')
                first = True
            else:
                broadcast("IN-USE. Please pick a new one username.", conn, '')
                first = False
        else:
            if len(client_list) > 2:
                conn.send(bytes("BUSY.", 'utf-8'))
            else:
                broadcast("Username is good.", conn, '')
                username_list.append(username)
                thread = threading.Thread(target=handle_client, args=(conn, username))
                thread.start()
                print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("STARTING THE SERVER...")
start()