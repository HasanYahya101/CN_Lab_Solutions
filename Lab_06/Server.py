import socket

attendance_db = []

def process_message(message, client_address):
    parts = message.split('-')
    if len(parts) != 3:
        return "Invalid message format. Use YY-AAAA-CI or YY-AAAA-CO."
    
    student_id = f"{parts[0]}-{parts[1]}"
    action = parts[2]

    if action == "CI":
        if student_id in attendance_db:
            return "You are already here."
        else:
            attendance_db.append(student_id)
            return f"Welcome Student {student_id}"
    
    elif action == "CO":
        if student_id in attendance_db:
            attendance_db.remove(student_id)
            return f"GoodBye Student {student_id}! Have a nice day."
        else:
            return "You didn’t check in today. Contact System Administrator."
    
    else:
        return "Invalid action. Use CI for check-in and CO for check-out."

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('127.0.0.1', 2000)
    sock.bind(server_address)
    print("Server started. Listening for messages...\n")

    while True:
        try:
            client_message, client_address = sock.recvfrom(2000)
            message = client_message.decode()
            print(f"Received from {client_address}: {message}")
            if message == "exit":
                break

            response = process_message(message, client_address)
            print("Updated Attendance List:", attendance_db)

            sock.sendto(response.encode(), client_address)

        except Exception as e:
            print(f"An error occurred: {e}")
            break

    sock.close()

if __name__ == "__main__":
    main()
