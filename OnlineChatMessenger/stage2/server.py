from math import e
import socket
import uuid
import threading
from chat_constants import MAX_UDP_PACKET_SIZE, TCP_HEADER_SIZE, UDP_HEADER_SIZE, Operation, State


class ChatServer:
  def __init__(self, host='localhost', tcp_port=8080, udp_port=8081):
    self.__host = host
    self.__tcp_port = tcp_port
    self.__tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.__tcp_server.bind((self.__host, self.__tcp_port))
    self.__tcp_server.listen()

    self.__udp_port = udp_port
    self.__udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    self.__udp_server.bind((self.__host, self.__udp_port))

    self.__receive_udp_thread = threading.Thread(target=self.__handle_udp_message)
    self.__receive_udp_thread.daemon = True
    self.__receive_udp_thread.start()

    self.__rooms = {}

  def start(self):
    print('Server started')
    while True:
      try:
        client_socket, address = self.__tcp_server.accept()
        print('Client connected')
        self.__handle_client(client_socket, address)
      except Exception as e:
        print(e)

  def __handle_client(self, client_socket, address):
    header = client_socket.recv(TCP_HEADER_SIZE)
    print(header)
    room_name_size = int(header[0])
    operation = Operation(int(header[1]))
    state = State(int(header[2]))
    user_name_size = int(header[3])
    print(room_name_size, operation, state, user_name_size)
    room_name = client_socket.recv(room_name_size).decode()
    user_name = client_socket.recv(user_name_size).decode()
    print(room_name, user_name)
    self.__send_tcp_message(client_socket, room_name, Operation.CREATE_ROOM, State.ACKNOWLEDGED, user_name)

    if operation == Operation.CREATE_ROOM:
      self.__create_room(client_socket, room_name, user_name, address)
    elif operation == Operation.JOIN_ROOM:
      self.__join_room(client_socket, room_name, user_name, address)

  def __get_room_token(self):
    return uuid.uuid4().hex
  
  def __create_room(self, client_socket, room_name, user_name, address):
    room_token = self.__get_room_token()
    self.__rooms[room_name] = {
      'token': room_token,
      'password': None,
      'users': [],
      'host': {'name': user_name, 'address': address}
    }
    print(f'部屋トークン: {room_token}')
    self.__send_tcp_message(client_socket, room_name, Operation.CREATE_ROOM, State.COMPLETED, room_token)

  def __join_room(self, client_socket, room_name, user_name, address):
    print(self.__rooms)
    room = self.__rooms[room_name]
    self.__send_tcp_message(client_socket, room_name, Operation.JOIN_ROOM, State.COMPLETED, room['token'])

  def __send_tcp_message(self, client_socket, room_name, operation, state, payload):
    try:
      header = bytes([len(room_name), operation.value, state.value, len(payload)])
      body = f'{room_name}{payload}'.encode()
      client_socket.send(header + body)
    except Exception as e:
      print(e)

  def __handle_udp_message(self):
    print('UDP server started')
    while True:
      data, address = self.__udp_server.recvfrom(MAX_UDP_PACKET_SIZE)
      print(data, address)
      room_name_size = int(data[0])
      token_size = int(data[1])
      room_name = data[2:2 + room_name_size].decode()
      token = data[2 + room_name_size:2 + room_name_size + token_size].decode()
      message = data[2 + room_name_size + token_size:].decode()
      print(room_name, token, message)
      if address not in self.__rooms[room_name]['users']:
        self.__rooms[room_name]['users'].append(address)
      self.__relay_message(room_name, message, address)
  
  def __relay_message(self, room_name, message, address):
    room = self.__rooms[room_name]
    print(room['host'])
    for user_address in room['users']:
      print(user_address)
      print(type (user_address))
      if address != user_address:
        self.__udp_server.sendto(message.encode(), user_address)

if __name__ == '__main__':
  chat_server = ChatServer()
  chat_server.start()