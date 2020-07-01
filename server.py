import socket
import threading
from win10toast import ToastNotifier

clients = set()


clientsUsernames = []
Clients_ = {}


def clientThreading(clientSocket, address):
    global username, client
    while True:
        try:
            username = clientSocket.recv(1024).decode("utf-8")

            massage = clientSocket.recv(1024).decode("utf-8")
            print(username + " says: " + massage)

            for client in clients:
                if client is not clientSocket:
                    client.send((username + " says: " + massage).encode("utf-8"))

            if massage is False:
                clients.remove(clientSocket)
                print(address[0] + ":" + str(address[1]) + " disconnected")
                break

        except ConnectionResetError:
            clients.remove(clientSocket)
            Addr = address[0] + ":" + str(address[1])
            disconnectClient = Clients_.get(Addr)
            clientsUsernames.remove(disconnectClient)
            print("{} disconnect".format(disconnectClient))
            break

    for client_ in clients:
        client_addr = address[0] + ":" + str(address[1])
        disconnectClient_ = Clients_.get(client_addr)
        client_.send((disconnectClient_ + " disconnect").encode("utf-8"))


hostSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

hostIp = "192.168.14.66"
portNumber = 7500
hostSocket.bind((hostIp, portNumber))
hostSocket.listen()
print("Waiting for connection...")

while True:
    clientSocket, clientAddress = hostSocket.accept()
    clients.add(clientSocket)
    print("Connection established with: ", clientAddress[0] + ":" + str(clientAddress[1]))
    clientUsername = clientSocket.recv(1024).decode("utf-8")

    for client in clients:
        if client is not clientSocket:
            client.send((clientUsername + " Join To The Server").encode("utf-8"))

    if clientUsername not in clientsUsernames:
        clientsUsernames.append(clientUsername)
        message = "-----------------------------\nNew User, " + clientUsername + "\n{} Join To The Chat\n----------------------------".format(clientUsername)
        print(message)

    ClientAddr = str(clientAddress[0]) + ":" + str(clientAddress[1])
    Clients_[ClientAddr] = clientUsername

    clientSocket.send("\n".join(clientsUsernames).encode("utf-8"))

    thread = threading.Thread(target=clientThreading, args=(clientSocket, clientAddress))
    thread.start()