from math import e
import socket
import threading
from chat_constants import MAX_UDP_PACKET_SIZE, TCP_HEADER_SIZE, Operation, State
import sys
import select
class ChatClient:
  def __init__(self, host='localhost', tcp_port=8080, udp_port=8081):
    self.__host = host
    self.__tcp_port = tcp_port
    self.__tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.__tcp_server.connect((self.__host, self.__tcp_port))
    self.__udp_port = udp_port
    self.__udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.__udp_server.bind(('', 0))

    self.__running = False
    self.__receive_tcp_thread = threading.Thread(target=self.__receive_tcp)
    self.__receive_tcp_thread.daemon = True
    self.__receive_tcp_thread.start()

    self.__room_token = None
    self.__room_name = None

  def start(self):
    user_name = input('Enter user name: ')
    room_name = input('Enter room name: ')
    choice = input('Create room or join room? (c/j): ')
    if choice == 'c':
      self.__send_tcp_message(room_name, Operation.CREATE_ROOM, State.INIT, user_name)
    elif choice == 'j':
      self.__send_tcp_message(room_name, Operation.JOIN_ROOM, State.INIT, user_name)
    
    while not self.__running:
      pass

    while self.__running:
      try:
        readable, _, _ = select.select([sys.stdin, self.__udp_server], [], [])
        for ready in readable:
          if ready == sys.stdin:
            message = sys.stdin.readline().strip()
            self.__send_udp_message(message)
            sys.stdout.flush()
          else:
            data = self.__udp_server.recv(MAX_UDP_PACKET_SIZE)
            sys.stdout.write(data.decode() + '\n')
            sys.stdout.flush()
      except Exception as e:
        print(e)

  def __send_tcp_message(self, room_name, operation, state, payload):
    try:
      header = bytes([len(room_name), operation.value, state.value, len(payload)])
      body = f'{room_name}{payload}'.encode()
      self.__tcp_server.send(header + body)
    except Exception as e:
      print(e)
  
  def __send_udp_message(self, message):
    try:
      header = bytes([len(self.__room_name), len(self.__room_token)])
      body = f'{self.__room_name}{self.__room_token}{message}'.encode()
      self.__udp_server.sendto(header + body, (self.__host, self.__udp_port))
    except Exception as e:
      print(e)

  def __receive_tcp(self):
    while not self.__running:
      try:
        header = self.__tcp_server.recv(TCP_HEADER_SIZE)
        print("headerを出力します")
        print(header)
        room_name_size = int(header[0])
        operation = Operation(int(header[1]))
        state = State(int(header[2]))
        payload_size = int(header[3])

        room_name = self.__tcp_server.recv(room_name_size).decode()
        payload = self.__tcp_server.recv(payload_size).decode()
        print(room_name, operation, state, payload)

        if state == State.ACKNOWLEDGED:
          print('処理中です')
        elif state == State.COMPLETED:
          self.__room_token = payload
          print(f'部屋トークン: {self.__room_token}')
          self.__room_name = room_name
          self.__tcp_server.close()
          print('メッセージを開始します')
          self.__running = True
      except Exception as e:
        print(e)
  

if __name__ == '__main__':
  chat_server = ChatClient()
  chat_server.start()
