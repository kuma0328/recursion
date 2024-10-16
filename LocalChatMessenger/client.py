import socket
import sys

def create_connection(server_address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Connecting to {}:{}'.format(*server_address))
    try:
        sock.connect(server_address)
        return sock
    except socket.error as e:
        print('Connection error:', e)
        sys.exit(1)

def send_and_receive(sock):
    try:
        sock.settimeout(5)  # 5秒のタイムアウトを設定

        while True:
            message = input('Enter message to send to server (or "quit" to exit): ')
            if message.lower() == 'quit':
                break

            print('Sending:', message)
            sock.sendall(message.encode())

            try:
                data = sock.recv(1024)
                if data:
                    print('Received:', data.decode())
                else:
                    print('Server closed the connection')
                    break
            except socket.timeout:
                print('No response from server within timeout')

    except socket.error as e:
        print('Communication error:', e)
    finally:
        print('Closing socket')
        sock.close()

if __name__ == "__main__":
    server_address = ('localhost', 8080)  # サーバーのアドレスとポート
    sock = create_connection(server_address)
    send_and_receive(sock)