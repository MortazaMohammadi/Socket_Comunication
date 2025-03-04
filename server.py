import socket
import threading

# Server configuration
HOST = '162.152.1.122'
PORT = 50000

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Server listening on {HOST}:{PORT}")
conn, addr = server_socket.accept()
print(f"Connected by {addr}")

# Function to receive messages
def receive_messages():
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            print(f"\nClient: {data.decode()}")
        except:
            break

# Function to send messages
def send_messages():
    while True:
        
        message = 'fuckyou  '
        conn.sendall(message.encode())

# Start threads
receive_thread = threading.Thread(target=receive_messages)
send_thread = threading.Thread(target=send_messages)
receive_thread.start()
send_thread.start()

receive_thread.join()
send_thread.join()

conn.close()
server_socket.close()
