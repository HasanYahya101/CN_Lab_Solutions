import socket

sckt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = ("localhost", 1234)

try:
    name = input("Please enter your name: ")
    if (name.__len__() > 0):
        sckt.sendto(f"Connect:{name}".encode(), address)
        print(sckt.recvfrom(1024).decode(), address)
    else:
        print("Please enter a valid command!")
        exit(0)

except:
    print("Error: An exception occurred")

try:
    while True:
        message = input("Client: ")
        sckt.sendto(message.encode(), address)
        resp = sckt.recvfrom(1024).decode()
        if resp == "Exit":
            print("Exiting!!!")
            exit(0)

        print(resp)

except:
    print("Error: An exception occurred")
    pass