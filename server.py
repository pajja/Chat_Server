import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))

client_list = []
#trying to store a username somehow
#username_list = []
#is_username = True

def keywords(conn, addr, msg):
    if msg == "!quit":
        print("DISCONNECT")
        #idk how to close the server properly
    elif msg == "!who":
        print(f"LIST_OF_CLIENT {client_list}")


def handle_client(conn, addr):
    connected = True
    while connected:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)

                #if is_username:
                #    username_list.append(msg)
                #    is_username = False

                print(f"{addr}> {msg}")
                keywords(conn, addr, msg)
                broadcast(f"{addr}> {msg}", conn)
                conn.send("Msg received".encode(FORMAT))
            else:
                connected = False
                if conn in client_list:
                    client_list.remove(conn)
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
    connected = True
    while connected:
        conn, addr = server.accept()
        client_list.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
        if (threading.active_count() - 1) < 1:
            connected = False
            conn.close()
            server.close()



print("STARTING THE SERVER...")
start()