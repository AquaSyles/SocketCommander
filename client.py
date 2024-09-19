import socket

def initialize_client_socket():

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host_address = "127.0.0.1"
    port = 3333

    return client_socket, host_address, port



def main():
    client_socket, host_address, port = initialize_client_socket()
    print("client_socket initialized.")

    client_socket.connect((host_address, port))
    print("Connection established.")

    while True:
        command = client_socket.recv(1024).decode("utf-8")
        print(command)

main()
