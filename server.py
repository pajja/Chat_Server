import socket
import threading

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))

client_list = []
username_list = []


def keywords(conn, addr, msg):
    if msg == "!quit":
        print("DISCONNECT")
        #idk how to close the server properly
    elif msg == "!who":
        print(f"LIST_OF_CLIENT {client_list}")


def handle_client(conn, addr, username):
    while True:
        try:
            msg_length = conn.recv(1024).decode('utf-8')
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode('utf-8')
                print(f"{addr}> {msg}")

                #threadKeywords = threading.Thread(target=keywords, args=(conn, addr, msg))
                #threadKeywords.start()

                threadBroadcast = threading.Thread(target=broadcast, args=(f"{addr}> {msg}", conn))
                threadBroadcast.start()

                conn.send(f"{username}> {msg}".encode('utf-8'))
            else:
                if conn in client_list:
                    client_list.remove(conn)
                    break
        except:
            continue

def broadcast(msg, conn):
    for clients in client_list:
        if clients != conn:
            try:
                clients.send(msg)
            except:
                clients.close()
                if conn in client_list:
                    client_list.remove(conn)


def start():
    server.listen()
    print(f"LISTENING ON {SERVER}")
    while True:
        conn, addr = server.accept()
        client_list.append(conn)
        username = conn.recv(1024).decode('utf-8')
        username_list.append(username)
        thread = threading.Thread(target=handle_client, args=(conn, addr, username))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("STARTING THE SERVER...")
start()