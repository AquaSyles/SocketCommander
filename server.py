import socket
import _thread

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
        client.send("ping".encode("utf-8"))
        client.settimeout(1)
        response = client.recv(1024).decode("utf-8")
        return response == "pong"

    except (socket.timeout, socket.error):
        return False

def send_command():
    while True:
        command = input("Enter command: ").encode("utf-8")
        to_remove = []
            
        for client in clients:
            if not ping(client):
                to_remove.append(client)
                client.close()
            else:
                try:
                    client.sendall(command)
                except socket.error:
                    to_remove.append(client)
                    client.close()
        
        # Remove clients after processing the command
        for client in to_remove:
            clients.remove(client)

def main():
    server_socket = initialize_server_socket()
    print("server_socket initialized.")

    while True:
        client_socket, client_address = server_socket.accept()
        clients.append(client_socket)

        _thread.start_new_thread(send_command, ())
main()
