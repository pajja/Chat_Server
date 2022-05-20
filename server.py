import socket
import threading
import sys

PORT = 5378
SERVER = socket.gethostbyname(socket.gethostname())

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))

client_list = []
username_list = []

global connOriginal

def keywords(conn, msg, username):
    try:
        key = msg.split()[0]

        if msg.split()[1] not in username_list:
            broadcast(conn, f"UNKNOWN\n")
        elif key == "WHO":
            broadcast(conn, f"WHO-OK {username_list}\n")
        elif key == "SEND":
            broadcast(conn, f"SEND-OK {username}\n")
            i = 2
            msgSplit = msg.split()
            fullMsg = ""
            while i < len(msgSplit):
                fullMsg = fullMsg + msgSplit[i] + " "
                i += 1
            print(f"sending to {msg.split()[1]}")
            index = username_list.index(msg.split()[1])
            connToSend = client_list[index]
            broadcast(connToSend, f"DELIVERY {msg.split()[1]} {fullMsg}\n")
            broadcast(connToSend, username)
        elif key == "HELLO-FROM\n":
            broadcast(conn, f"HELLO {username}\n")
    except:
        sys.exit()


def first_handshake(conn, addr):
    firstHandshake = conn.recv(1024).decode('utf-8')
    username = firstHandshake.split()[1]

    if firstHandshake.split()[0] == "HELLO-FROM":
        broadcast(conn, f"HELLO {username}\n")
        print(f"{addr} username: {username}")
        if username in username_list:
            broadcast(conn, "IN-USE\n")
            first_handshake(conn, addr)
        else:
            if len(client_list) > 64:
                broadcast(conn, "BUSY\n")
            else:
                username_list.append(username)
                thread = threading.Thread(target=handle_client, args=(conn, username))
                thread.start()
                print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
    else:
        remove(conn)


def handle_client(conn, username):
    while True:
        try:
            msg = conn.recv(1024).decode('utf-8')
            print(f"{username}> {msg}")

            threadKeywords = threading.Thread(target=keywords, args=(conn, msg, username))
            threadKeywords.start()
        except:
            continue


def remove(conn):
    if conn in client_list:
        client_list.remove(conn)


def broadcast(conn, msg):
    conn.send(bytes(f"{msg}", 'utf-8'))

def start():
    server.listen()
    print(f"LISTENING ON {SERVER}")
    while True:
        conn, addr = server.accept()
        client_list.append(conn)
        threadFirstHandshake = threading.Thread(target=first_handshake, args=(conn, addr))
        threadFirstHandshake.start()



print("STARTING THE SERVER...")
start()






# import socket
# import threading
# import sys
#
# PORT = 5378
# SERVER = socket.gethostbyname(socket.gethostname())
#
# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind((SERVER, PORT))
#
# client_list = []
# username_list = []
#
#
# def keywords(conn, msg, username):
#     try:
#         key = msg.split()[0]
#
#         if key == "WHO":
#             broadcast(conn, f"WHO-OK {username_list}\n")
#         elif key == "SEND":
#             if msg.split()[1] not in username_list:
#                 broadcast(conn, f"UNKNOWN\n")
#             else:
#                 broadcast(conn, f"SEND-OK {username}\n")
#                 i = 2
#                 msgSplit = msg.split()
#                 fullMsg = ""
#                 while i < len(msgSplit):
#                     fullMsg = fullMsg + msgSplit[i] + " "
#                     i += 1
#                 print(f"sending to {msg.split()[1]}")
#                 index = username_list.index(msg.split()[1])
#                 connToSend = client_list[index]
#                 broadcast(connToSend, f"DELIVERY {msg.split()[1]} {fullMsg}\n")
#         elif key == "HELLO-FROM\n":
#             broadcast(conn, f"HELLO {username}\n")
#     except:
#         sys.exit()
#
#
# def first_handshake(conn, addr):
#     firstHandshake = conn.recv(1024).decode('utf-8')
#     username = firstHandshake.split()[1]
#
#     if firstHandshake.split()[0] == "HELLO-FROM":
#         broadcast(conn, f"HELLO {username}\n")
#         print(f"{addr} username: {username}")
#
#         if username in username_list:
#             broadcast(conn, "IN-USE\n")
#         else:
#             if len(client_list) > 64:
#                 broadcast(conn, "BUSY\n")
#             else:
#                 username_list.append(username)
#                 thread = threading.Thread(target=handle_client, args=(conn, username))
#                 thread.start()
#                 print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
#     else:
#         remove(conn)
#
#
# def handle_client(conn, username):
#     while True:
#         try:
#             msg = conn.recv(1024).decode('utf-8')
#             print(f"{username}> {msg}")
#
#             threadKeywords = threading.Thread(target=keywords, args=(conn, msg, username))
#             threadKeywords.start()
#         except:
#             continue
#
#
# def remove(conn):
#     if conn in client_list:
#         client_list.remove(conn)
#
#
# def broadcast(conn, msg):
#     conn.send(bytes(f"{msg}", 'utf-8'))
#
# def start():
#     server.listen()
#     print(f"LISTENING ON {SERVER}")
#     while True:
#         conn, addr = server.accept()
#         client_list.append(conn)
#         threadFirstHandshake = threading.Thread(target=first_handshake, args=(conn, addr))
#         threadFirstHandshake.start()
#
#
#
# print("STARTING THE SERVER...")
# start()
