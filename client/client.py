import socket
import subprocess

def initialize_client_socket():

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host_address = "192.168.1.24"
    port = 3333

    return client_socket, host_address, port

def run_py_command(command):
    subprocess.run(["python3", f"commands/{command}/{command}.py"])

def main():
    client_socket, host_address, port = initialize_client_socket()
    print("client_socket initialized.")

    client_socket.connect((host_address, port))
    print("Connection established.")

    while True:
        command = client_socket.recv(1024).decode("utf-8")
        run_py_command("geoinit")
main()
