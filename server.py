import socket
import _thread

clients = []

def initialize_server_socket():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    host_address = "127.0.0.1"
    port = 3333

    server_socket.bind((host_address, port))
    server_socket.listen(5)

    return server_socket

def thread_socket(client_socket):
    while True:
        pass

def send_command():
    while True:
        command = input("Enter command: ").encode("utf-8")
        for client in clients:
            client.sendall(command)


def main():
    server_socket = initialize_server_socket()
    print("server_socket initialized.")

    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)

        _thread.start_new_thread(thread_socket, (client_socket,))
        _thread.start_new_thread(send_command, ())
main()
