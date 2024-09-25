import socket
import threading
import pickle

clients = []

def initialize_server_socket():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host_address = "192.168.1.24"
    port = 3333

    server_socket.bind((host_address, port))
    server_socket.listen(5)

    return server_socket

def ping(client):
    try:
        command = {'command': "ping", "parameters": []}

        client.send(pickle.dumps(command))
        client.settimeout(1)
        response = client.recv(1024)

        if not response:
            return False

        return pickle.loads(response) == "pong"

    except (socket.timeout, socket.error):
        return False

def send_command():
    while True:
        command = input("Enter command: ")

        command_list = command.split(" ")
        command_dict = {"command": command_list[0], "parameters": command_list[1:]}
        command = pickle.dumps(command_dict)
        
        to_remove = []
        
        for client in clients:
            try:
                if not ping(client):
                    to_remove.append(client)
                else:
                    client.sendall(command)
            except (socket.timeout, socket.error):
                to_remove.append(client)
        
        # Remove clients after processing the command
        for client in to_remove:
            clients.remove(client)
            client.close()

def main():
    server_socket = initialize_server_socket()
    print("server_socket initialized.")

    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)

        threading.Thread(target=send_command, args=()).start()
main()
