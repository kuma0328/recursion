import socket
import select
import sys

class chatClient:
  def __init__(self):
    self.__host = 'localhost'
    self.__port = 8080
    self.__client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.__username = input('Enter your username: ')
  
  def start(self):
    self.__client.connect((self.__host, self.__port))
    print('Client started')
    while True:
      try:
        readable, _, _ = select.select([sys.stdin, self.__client], [], [])
        for ready in readable:
          if ready == sys.stdin:
            self._handle_input()
          else:
            self._receive_message()
      except Exception as e:
        print(f'Error sending message: {e}')
        break
    self.__client.close()

  def _handle_input(self):
    message = input()
    full_message = f'{len(self.__username)}{self.__username}{message}'
    self.__client.send(full_message.encode('utf-8'))

  def _receive_message(self):
    try:
      message = self.__client.recv(1024).decode('utf-8')
      print(f'Message: {message}')
    except Exception as e:
      print(f'Error receiving message: {e}')

if __name__ == '__main__':
  client = chatClient()
  client.start()
