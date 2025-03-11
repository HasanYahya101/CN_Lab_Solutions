import socket

def contains_vowel(word):
    vowels = "aeiouAEIOU"
    return any(char in vowels for char in word)

def invert_words_with_vowels(sentence):
    words = sentence.split()
    inverted = [word[::-1] if contains_vowel(word) else word for word in words]
    return ' '.join(inverted)

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
        print(f"Received from client: {data}")

        result = invert_words_with_vowels(data)
        print(f"Processed string to send back: {result}")

        connection.sendall(result.encode())

    except Exception as e:
        print(f"Error: {e}")
    finally:
        connection.close()
        print("Connection closed.\n")
