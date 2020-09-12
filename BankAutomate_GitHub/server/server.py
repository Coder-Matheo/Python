import socket
import threading
import time

HEADER = 64
PORT = 5050
SERVER = "127.0.0.1"
#SERVER = socket.gethostbyname(socket.gethostname())#for public client, do you need change hosname
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
#print(SERVER)#ip address
#print(socket.gethostname())#hostname

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#socket.AF_INET == use IPV4
server.bind(ADDR)




def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")#who connected

    connected = True
    #wait receive information from client
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)  # how many cann byte receive
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)#if don't give the recv, you get missing
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))
    conn.close()

def start():
    server.listen()
    print(f"[LISTINING] server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()#new connection, from where (conn,addr) coming
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() -1}")#how many active threading active



print("[STARTING] server is starting....")
start()