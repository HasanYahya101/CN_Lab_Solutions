import socket

def contains_vowel(word):
    vowels = "aeiouAEIOU"
    return any(char in vowels for char in word)

def invert_words_without_vowels(sentence):
    words = sentence.split()
    inverted = [word[::-1] if not contains_vowel(word) else word for word in words]
    return ' '.join(inverted)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10000)
print(f"Connecting to {server_address[0]} port {server_address[1]}")
sock.connect(server_address)

try:
    message = input("Enter the string to send to server: ").strip()
    print(f"Sending to server: {message}")
    sock.sendall(message.encode())

    data = sock.recv(1024).decode()
    print(f"Received from server: {data}")

    final_result = invert_words_without_vowels(data)
    print(f"Final processed string: {final_result}")

finally:
    print("Closing connection")
    sock.close()
