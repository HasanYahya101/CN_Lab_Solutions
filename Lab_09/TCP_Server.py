import socket

def main():
    host = '127.0.0.1'
    port = 2000
    buffer_size = 2000

    # Create socket
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket created")
    except socket.error as err:
        print(f"Could not create socket. Error: {err}")
        return

    # Bind socket to IP and port
    try:
        server_socket.bind((host, port))
        print("Bind done")
    except socket.error as err:
        print(f"Bind failed. Error: {err}")
        return

    # Listen for incoming connections
    try:
        server_socket.listen(1)
        print("Listening for incoming connections...")
    except socket.error as err:
        print(f"Listen failed. Error: {err}")
        return

    # Accept a client connection
    try:
        client_socket, client_address = server_socket.accept()
        print(f"Client connected with IP: {client_address[0]} and Port No: {client_address[1]}")
    except socket.error as err:
        print(f"Accept failed. Error: {err}")
        return

    # Receive message from client
    try:
        client_message = client_socket.recv(buffer_size).decode()
        print(f"Client Message: {client_message}")
    except socket.error as err:
        print(f"Receive failed. Error: {err}")
        client_socket.close()
        server_socket.close()
        return

    # Send message back to client
    try:
        client_socket.sendall(client_message.encode())
    except socket.error as err:
        print(f"Send failed. Error: {err}")

    # Close sockets
    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    main()
