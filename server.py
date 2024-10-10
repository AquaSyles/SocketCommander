import socket
import threading
import pickle

host_address = "192.168.1.24"
port = 3333

class Log:
    def __init__(self, log_level):
        log_levels = [0, 1, 2]

        if log_level in log_levels:
            self.log_level = log_level
        else:
            self.log_level = 2
            self.criticalLog("Invalid log level")

    def debugLog(self, log_text):
        if self.log_level == 2:
            print("--"*20)
            print(f"DEBUG: {log_text}")
            print("--"*20,"\n")

    def warningLog(self, log_text):
        if self.log_level == 2:
            print("-=-"*20)
            print(f"WARNING: {log_text}")
            print("-=-"*20,"\n")

    def criticalLog(self, log_text):
        if self.log_level > 0:
            print("!-*-!"*14)
            print(f"CRITICAL: {log_text}")
            print("!-*-!"*14,"\n")

class Server(Log):
    def __init__(self, host_address, port):
        super().__init__(0)
        self.clients = []

        self.server_socket = self.initialize_server_socket(host_address, port)
        self.debugLog("Initialized Server Socket")
        
        self.accept_loop(self.server_socket)

    def initialize_server_socket(self, host_address, port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_socket.bind((host_address, port))
        server_socket.listen(5)

        return server_socket
    
    def accept_loop(self, server_socket):
        while True:
            client_socket, client_address = server_socket.accept()

            self.add_client(client_socket, client_address)
            self.create_thread()

    def create_thread(self, argument=None):
        if not argument:
            threading.Thread(target=self.send_command, args=()).start()

    def add_client(self, client_socket, client_address):
        self.clients.append(client_socket)

    def get_command(self):
        command = input("Enter command: ")
        command_list = command.split(" ")
        command_dict = {"command": command_list[0], "parameters": command_list[1:]}
        command = pickle.dumps(command_dict)

        return command

    def send_command(self):
        while True:
            command = self.get_command()
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
