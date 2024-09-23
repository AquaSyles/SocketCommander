import socket
import subprocess
import os
import threading

def initialize_client_socket():

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host_address = "192.168.1.24"
    port = 3333

    return client_socket, host_address, port

def run_py_command(command):
    command_path = os.path.join(os.path.dirname(__file__), "commands", command, f"{command}.py") # Gets the path of the command file
    python_version = "python" if os.name == "nt" else "python3" # Needs correct type to run a python file depending on OS

    subprocess.run(["python3", command_path])

def main():
    client_socket, host_address, port = initialize_client_socket()
    print("client_socket initialized.")

    client_socket.connect((host_address, port))
    print("Connection established.")

    while True:
        command = client_socket.recv(1024).decode("utf-8")

        if command == "ping":
            client_socket.send("pong".encode("utf-8"))

        else:
            threading.Thread(target=run_py_command, args=(command,)).start()
main()
