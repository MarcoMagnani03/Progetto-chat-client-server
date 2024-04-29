import socket
from config import SERVER_IP, PORT

def client_connection(client_socket, addr, clients):
    print(f"Nuova connessione alla chat! {addr} si è connesso.")
    print(f"Lista di client che si sono collegati {clients}")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_IP, PORT))
    server.listen()

    # Lista di client collegati
    clients = []

    print("Server in ascolto...")

    try:
        while True:
            client_socket, addr = server.accept()
            clients.append(client_socket)
            client_connection(client_socket, addr, clients)
    except KeyboardInterrupt:
        print("Arresto del server...")
        server.close()

if __name__ == "__main__":
    main()