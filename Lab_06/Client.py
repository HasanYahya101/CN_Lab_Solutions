import socket

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('127.0.0.1', 2000)
    
    try:
        while True:
            client_message = input("Enter Message (YY-AAAA-CI or YY-AAAA-CO): ")
            if not client_message:
                break
            
            sock.sendto(client_message.encode(), server_address)

            if client_message == "exit":
                break
            server_message, _ = sock.recvfrom(2000)
            print(f"Server Response: {server_message.decode()}")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        sock.close()

if __name__ == "__main__":
    main()
