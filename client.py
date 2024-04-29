import socket
from config import SERVER_IP, PORT

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((SERVER_IP, PORT))
        print("Connesso al server.")
    except ConnectionRefusedError:
        print("Connessione rifiutata. Assicurati che il server sia in esecuzione.")
        return

if __name__ == "__main__":
    main()
