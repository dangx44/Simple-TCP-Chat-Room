import threading
import socket

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
nicknames = []

#Broadcast msg to all clients
def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f"{nickname} left the chat!".encode('ascii'))
            nicknames.remove(nickname)
            break

def receive():
    while True:
        #Constantly accept new clients
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        #Send keyword NICK to client, they send back nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f"nickname of client is {nickname}")
        #broadcast to all clients
        broadcast(f"{nickname} joined the chat!".encode('ascii'))
        #Send msg to specific client that they are connected
        client.send("Connected to the server".encode('ascii'))
        #Start Thread to handle this specific client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server is Listening")
receive()
