import socket
import threading
import pickle

host_address = "192.168.1.24"
port = 3333

class Server:
    def __init__(self, host_address, port):
        self.clients = []

        self.server_socket = self.initialize_server_socket(host_address, port)
        print("server_socket initialized")
        
        self.accept_loop(self.server_socket)

    def initialize_server_socket(self, host_address, port):

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_socket.bind((host_address, port))
        server_socket.listen(5)

        return server_socket
    
    def accept_loop(self, server_socket):

        while True:
            client_socket, client_address = server_socket.accept()
            clients.append(client_socket)

            threading.Thread(target=send_command, args=()).start()

    def send_command(self):
        while True:
            command = input("Enter command: ")

            command_list = command.split(" ")
            command_dict = {"command": command_list[0], "parameters": command_list[1:]}
            command = pickle.dumps(command_dict)
            
            to_remove = []
            
            for client in self.clients:
                try:
                    if not self.ping(client):
                        to_remove.append(client)
                    else:
                        client.sendall(command)
                except (socket.timeout, socket.error):
                    to_remove.append(client)
            
            # Remove clients after processing the command
            for client in to_remove:
                self.clients.remove(client)
                client.close()

    def ping(self, client):
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

server = Server(host_address, port)
