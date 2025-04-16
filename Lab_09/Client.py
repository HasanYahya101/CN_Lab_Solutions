import socket

def main():
    host = 'localhost'
    port = 2000

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    while True:
        server_msg = client_socket.recv(1024).decode()
        if (not server_msg):
            break
        print(server_msg, end='')

        if ("Goodbye" in server_msg or "rejected" in server_msg or "Thank you" in server_msg):
            break

        user_input = input()
        client_socket.sendall(user_input.encode())

    client_socket.close()

if __name__ == "__main__":
    main()
