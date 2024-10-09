import socket
import subprocess
import os
import threading
import pickle


class Client:
    def __init__(self):
        self.commands_directory_path = os.path.join(os.path.dirname(__file__), "commands")

        self.client_socket, host_address, port = self.initialize_client_socket()

        self.client_socket.connect((host_address, port))
        print(f"Connected to host at: {host_address}")

        self.accept_loop()



    def initialize_client_socket(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        host_address = "192.168.1.24"
        port = 3333

        return client_socket, host_address, port

    def accept_loop(self):
        try:
            while True:
                command = self.client_socket.recv(1024)
                print("Ready to receive")
                command = pickle.loads(command)

                command, parameters = command['command'], command['parameters']
                
                if command == "ping":
                    self.client_socket.send(pickle.dumps("pong"))

                elif command == "close":
                    with open(os.path.join(self.commands_directory_path, "geoinit", "config.pkl"), 'wb') as file:
                        config_dict = {'status': 0}
                        pickle.dump(config_dict, file)

                else:
                    threading.Thread(target=self.run_py_command, args=(command, parameters,)).start()
                    
        except KeyboardInterrupt:
            print("Shutting down...")
            exit()


    def run_py_command(self, command, parameters):
        command_path = os.path.join(self.commands_directory_path, command, f"{command}.py") # Gets the path of the command file
        python_version = "python" if os.name == "nt" else "python3" # Needs correct type to run a python file depending on OS
        
        self.initiate_running_path(command, parameters) # Command is not allowed to run if running if False, which lets us close threads.

        print("Ready to run python process") 
        print("command_path", command_path)
        print("parameters", parameters)
        subprocess.run([python_version, command_path])

    def initiate_running_path(self, command, parameters):
        with open(os.path.join(self.commands_directory_path, command, "config.pkl"), 'wb') as file:
            config_dict = {'status': 1, 'parameters': parameters}
            pickle.dump(config_dict, file)

client = Client()
