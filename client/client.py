import socket
import subprocess
import os
import threading
import pickle

commands_directory_path = os.path.join(os.path.dirname(__file__), "commands")

def initialize_client_socket():

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host_address = "192.168.1.24"
    port = 3333

    return client_socket, host_address, port

def initiate_running_path(running_path, parameters):
    with open(os.path.join(commands_directory_path, "geoinit", "config.pkl"), 'wb') as file:
        config_dict = {'status': 1, 'parameters': parameters}
        pickle.dump(config_dict, file)


def run_py_command(command, parameters):
    command_path = os.path.join(commands_directory_path, command, f"{command}.py") # Gets the path of the command file
    running_path =  os.path.join(commands_directory_path, command, "running") 
    python_version = "python" if os.name == "nt" else "python3" # Needs correct type to run a python file depending on OS
    
    initiate_running_path(running_path, parameters) # Command is not allowed to run if running if False, which lets us close threads.

   
    subprocess.run([python_version, command_path])
    

def main():
    client_socket, host_address, port = initialize_client_socket()
    print("client_socket initialized.")

    client_socket.connect((host_address, port))
    print("Connection established.")
    
    try:
        while True:
            command = client_socket.recv(1024)
            command = pickle.loads(command)

            command, parameters = command['command'], command['parameters']
            
            if command == "ping":
                client_socket.send(pickle.dumps("pong"))

            elif command == "close":
                with open(os.path.join(commands_directory_path, "geoinit", "config.pkl"), 'wb') as file:
                    config_dict = {'status': 0}
                    pickle.dump(config_dict, file)

            else:
                threading.Thread(target=run_py_command, args=(command, parameters,)).start()
                
    except KeyboardInterrupt:
        print("Shutting down...")
        exit()
main()
