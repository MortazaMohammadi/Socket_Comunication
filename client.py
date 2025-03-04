import socket
import threading

# Server details
HOST = '127.0.0.1'
PORT = 65432

# Create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

# Function to receive messages
def receive_messages():
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"\nServer: {data.decode()}")
        except:
            break

# Function to send messages
def send_messages():
    while True:
        message = input("You (Client): ")
        client_socket.sendall(message.encode())

# Start threads
receive_thread = threading.Thread(target=receive_messages)
send_thread = threading.Thread(target=send_messages)
receive_thread.start()
send_thread.start()

receive_thread.join()
send_thread.join()

client_socket.close()
