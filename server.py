import socket
import threading
from config import SERVER_IP, PORT, MSG_SIZE, ENCODING

server_running = True

def manage_client_connection(client_socket, addr, clients):
    try:
        username = client_socket.recv(MSG_SIZE).decode(ENCODING).upper()

        if username in [user[1] for user in clients]:
            print(f"Il nome utente '{username}' è già in uso.")
            client_socket.send("ERRORE NOME UTENTE GIÀ IN USO.".encode(ENCODING))
            return

        clients.append((client_socket, username))
        print(f"Nuova connessione! {addr} connesso come '{username}'")

        while True:
            message = client_socket.recv(MSG_SIZE).decode(ENCODING)
            if not message:
                break
            print(f"[{username}] {message}")
            send_broadcast_message(message, clients, username)
    except ConnectionResetError:
        print(f"Il client {addr} si è disconnesso in modo inatteso.")
    except OSError as e:
        print(f"Errore durante la gestione della connessione con {addr}: {e}")
    finally:
        remove_client(client_socket, clients)

def send_broadcast_message(message, clients, sender_username):
    for client, username in clients:
        if username != sender_username:
            try:
                client.send(f"{sender_username}: {message}".encode(ENCODING))
            except OSError as e:
                print(f"Si è verificato un errore durante l'invio del messaggio a {username}: {e}")

def remove_client(client_socket, clients):
    for client, username in clients:
        if client_socket == client:
            try:
                client_socket.close()
                print(f"Il client {username} si è disconnesso.")
                clients.remove((client, username))
            except OSError as e:
                print(f"Si è verificato un errore durante la disconnessione del client {username}: {e}")

def main():
    global server_running
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_IP, PORT))
    server.listen()

    print(f"Server in ascolto porta {PORT}...")

    clients = []

    try:
        while server_running:
            client_socket, addr = server.accept()
            client_handler = threading.Thread(target=manage_client_connection, args=(client_socket, addr, clients))
            client_handler.start()
    except KeyboardInterrupt:
        print("Arresto del server...")
        server_running = False
        for client_socket, _ in clients:
            client_socket.close()
        server.close()
    except OSError as e:
        print(f"Errore non gestito nel server: {e}")

if __name__ == "__main__":
    main()