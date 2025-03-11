import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10000)
print(f"Starting up on {server_address[0]} port {server_address[1]}")
sock.bind(server_address)

sock.listen(5)

print("Server is running and waiting for connections...")

while True:
    connection, client_address = sock.accept()
    try:
        print(f"Connection from {client_address}")

        data = connection.recv(1024).decode()
        print(f"Received: {data}")

        if "My id is" in data:
            client_id = data.split("My id is")[-1].strip()
            response = f"Hello I am server. Your received id is {client_id}"
        else:
            response = "Invalid message format."

        connection.sendall(response.encode())

    except Exception as e:
        print(f"Error: {e}")
    finally:
        connection.close()
        print("Connection closed\n")
