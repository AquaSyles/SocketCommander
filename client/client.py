import socket
import subprocess
import os
import threading

commands_directory_path = os.path.join(os.path.dirname(__file__), "commands")

def initialize_client_socket():

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host_address = "192.168.1.24"
    port = 3333

    return client_socket, host_address, port

def run_py_command(command):
    command_path = os.path.join(commands_directory_path, command, f"{command}.py") # Gets the path of the command file
    running_path =  os.path.join(commands_directory_path, command, "running") 
    python_version = "python" if os.name == "nt" else "python3" # Needs correct type to run a python file depending on OS
    
    with open(running_path, 'w') as file:
        file.write('1')
    subprocess.run([python_version, command_path])
    

def main():
    client_socket, host_address, port = initialize_client_socket()
    print("client_socket initialized.")

    client_socket.connect((host_address, port))
    print("Connection established.")
    
    try:
        while True:
            command = client_socket.recv(1024).decode("utf-8")

            if command == "ping":
                client_socket.send("pong".encode("utf-8"))

            elif command == "close":
                with open(os.path.join(commands_directory_path, "geoinit", "running"), 'w') as file:
                    file.write('0')

            else:
                threading.Thread(target=run_py_command, args=(command,)).start()
                
    except KeyboardInterrupt:
        print("Shutting down...")
        exit()
main()
