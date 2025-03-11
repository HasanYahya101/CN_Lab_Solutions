import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10000)
print(f"Connecting to {server_address[0]} port {server_address[1]}")
sock.connect(server_address)

try:
    client_id = input("Enter your client ID (0-9): ").strip()
    if not (client_id.isdigit() and len(client_id) == 1):
        print("Invalid ID. Please enter a single digit between 0 and 9.")
    else:
        message = f"Hello I am client and My id is {client_id}"
        print(f"Sending: {message}")
        sock.sendall(message.encode())
        data = sock.recv(1024).decode()
        print(f"Received from server: {data}")

finally:
    print("Closing connection")
    sock.close()
