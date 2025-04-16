import socket
import threading

LOCK = threading.Lock()
VOTED = set()

def load_voters():
    with open('Voters_List.txt', 'r') as file:
        voters = set()
        for line in file.readlines():
            voters.add(line.strip())
        return voters

def load_candidates():
    with open('Candidates_List.txt', 'r') as file:
        candidates = []
        for line in file.readlines():
            parts = line.strip().split('/')
            if len(parts) == 2:
                name, symbol = parts
                candidates.append((name.strip(), symbol.strip()))
            else:
                print(f"Skipping invalid candidate line: {line.strip()}")
        return candidates

def load_votes():
    try:
        with open('Votes.txt', 'r') as file:
            for line in file:
                stripped = line.strip()
                name, cnic, _ = stripped.split('/')
                VOTED.add(f"{name}/{cnic}")
    except FileNotFoundError:
        pass

def handle_client(client_socket):
    try:
        client_socket.sendall(b"Enter your Name: ")
        name = client_socket.recv(1024).decode().strip()

        client_socket.sendall(b"Enter your CNIC: ")
        cnic = client_socket.recv(1024).decode().strip()

        voter_key = f"{name}/{cnic}"
        if voter_key not in VALID_VOTERS:
            client_socket.sendall(b"Authentication failed. Name and CNIC do not match or you are not a registered voter.\n")
            client_socket.close()
            return

        with LOCK:
            if voter_key in VOTED:
                client_socket.sendall(b"You have already voted. Goodbye.\n")
                client_socket.close()
                return
            else:
                VOTED.add(voter_key)

        candidates = load_candidates()

        candidate_list = []

        user_name = name

        for name_, symbol in candidates:
            candidate_list.append(f"{name_} - {symbol}")
        candidate_list = "\n".join(candidate_list)

        client_socket.sendall(f"Welcome {user_name}! Here are the candidates:\n{candidate_list}\nVote by entering the POLL SYMBOL: ".encode())

        vote = client_socket.recv(1024).decode().strip()

        if vote not in [symbol for _, symbol in candidates]:
            client_socket.sendall(b"Invalid poll symbol. Vote rejected.\n")
        else:
            with LOCK:
                with open('Votes.txt', 'a') as f:
                    f.write(f"{name}/{cnic}/{vote}\n")
            client_socket.sendall(b"Thank you! Your vote has been recorded.\n")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

def start_server():
    load_votes()
    host = 'localhost'
    port = 2000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Voting Server started on {host}:{port}")

    while True:
        client_sock, addr = server_socket.accept()
        print(f"Client connected: {addr}")
        threading.Thread(target=handle_client, args=(client_sock,)).start()

if __name__ == "__main__":
    VALID_VOTERS = load_voters()
    start_server()
