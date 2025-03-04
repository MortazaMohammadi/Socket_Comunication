import socket
import threading

HOST = '162.152.1.122'  # Server's IP
PORT = 50000

# Create a socket for the client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))  # Connect to server

def receive_messages():
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print("Server disconnected.")
                break
            print(f"\nServer: {data.decode()}")
        except ConnectionResetError:
            print("Server forcibly closed the connection.")
            break
    client_socket.close()

def send_messages():
    while True:
        try:
            message = input("You (Client): ")
            client_socket.sendall(message.encode())
        except:
            print("Connection closed. Exiting...")
            break

# Run sender and receiver in parallel threads
receive_thread = threading.Thread(target=receive_messages)
send_thread = threading.Thread(target=send_messages)
receive_thread.start()
send_thread.start()

receive_thread.join()
send_thread.join()
