import socket
from faker import Faker
import threading

def handle_client(client_socket, address, faker):
    print(f'Connection from {address}')
    
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                print(f'Client {address} disconnected')
                break
            
            print(f'Received from {address}: {data.decode()}')
            
            response = faker.text().encode()
            client_socket.sendall(response)
            print(f'Sent {len(response)} bytes back to {address}')
    
    except Exception as e:
        print(f'Error handling client {address}: {e}')
    finally:
        client_socket.close()

def start_server(host, port):
    faker = Faker()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port)
    
    try:
        server_socket.bind(server_address)
        server_socket.listen(5)
        print(f'Server is listening on {host}:{port}')

        while True:
            client_socket, address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, address, faker))
            client_thread.start()

    except Exception as e:
        print(f'Server error: {e}')
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server('localhost', 8080)