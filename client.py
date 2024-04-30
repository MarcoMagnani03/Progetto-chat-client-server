import socket
import threading
import sys
from config import MSG_SIZE, ENCODING

def receive_messages(client_socket):
    try:
        while True:
            message = client_socket.recv(MSG_SIZE).decode(ENCODING)
            if not message:
                break
            print(f"{message}")
            if message.strip().upper() == "NOME UTENTE GIÀ IN USO.":
                print("\nLa connessione è stata chiusa, riavvia e tenta un nuovo nome utente...")
                break
    except Exception as e:
        print(f"\nErrore durante la ricezione dei messaggi: {e}")
    finally:
        client_socket.close()

def send_message(client_socket):
    try:
        while True:
            message = input("")
            print(f"Messaggio inviato: {message}")
            client_socket.send(message.encode(ENCODING))
    except KeyboardInterrupt:
        print("\nChiusura del client...")
    except Exception as e:
        print(f"\nErrore durante l'invio del messaggio: {e}")
    finally:
        client_socket.close()

def main():
    if len(sys.argv) != 4:
        print("Il comando non è corretto. Usa il seguente formato: client.py indirizzo_ip_del_server porta_server username")
        sys.exit(0)

    server_ip = str(sys.argv[1])
    server_port = int(sys.argv[2])
    username = sys.argv[3].strip().upper()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect((server_ip, server_port))
        print("\nTi sei collegato al server!! Verifica che il nome utente sia univoco...,\nse non vedi un errore allora puoi inviare il tuo messaggio scrivendolo e premendo invio")
        client.send(username.encode(ENCODING))
    except ConnectionRefusedError:
        print("\nConnessione rifiutata. Assicurati che il server sia in esecuzione.")
        return

    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    send_thread = threading.Thread(target=send_message, args=(client,))

    receive_thread.start()
    send_thread.start()

    try:
        while True:
            pass  
    except KeyboardInterrupt:
        print("\nChiusura del client...")

if __name__ == "__main__":
    main()