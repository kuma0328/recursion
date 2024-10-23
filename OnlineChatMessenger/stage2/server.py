import socket
import uuid
import threading

from chat_constants import TCP_HEADER_SIZE, Operation, State, StatusCodes

class ChatServer:
  def __init__(self, host="localhost", tcp_port=8080, udp_port=8081):
    self.__host = host
    self.__tcp_port = tcp_port
    self.__udp_port = udp_port

    self.__tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.__udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    self.__rooms = {}
    self.__token = {}

    self.__tcp_socket.bind((self.__host, self.__tcp_port))
    self.__udp_socket.bind((self.__host, self.__udp_port))

  def start(self):
    self.__tcp_socket.listen(5)
    print("TCP Server started")
    while True:
      client_socket, address = self.__tcp_socket.accept()
      print(f"Connection from {address}")
      client_thread = threading.Thread(target=self.__handle_tcp_client, args=(client_socket,address))
      client_thread.daemon = True
      client_thread.start()

  def __handle_tcp_client(self, client_socket, address):
    try:
      header = client_socket.recv(TCP_HEADER_SIZE)
      if not header:
        return
      
      room_name_size = header[0]
      operation = header[1]
      state = header[2]
      payload_size = int.from_bytees(header[3:32], byteorder="big")

      body = client_socket.recv(room_name_size + payload_size)
      room_name = body[:room_name_size].decode('utf-8')
      payload = body[room_name_size:].decode('utf-8')

      if operation == Operation.CREATE_ROOM.value:
        self.__create_room(room_name, address)
      elif operation == Operation.JOIN_ROOM.value:
        self.__join_room(room_name, address)
    except Exception as e:
      print(f'Error handling TCP client: {e}')
    finally:
      client_socket.close()

  def __create_room(self, room_name, address):
    if room_name in self.__rooms:
      self.__send_response(StatusCodes.INVALID_ROOM_NAME, address)
      return
    
    room_id = str(uuid.uuid4())
    self.__rooms[room_name] = {
      'id': room_id,
      'members': [address]
    }
    self.__send_tcp_response(address, room_name, Operation.CREATE_ROOM.value, State.COMPLETED.value, StatusCodes.SUCCESS)
  
  def __send_tcp_response(self, client_socket, room_name, operation, state, status_code):
    try:
      room_name_bytes = room_name.encode('utf-8')
      payload_bytes = status_code.value.encode('utf-8')
      header = bytes([len(room_name_bytes), operation, state]) + b'\x00' * (TCP_HEADER_SIZE - 3)
      client_socket.send(header + room_name_bytes + payload_bytes)
    except Exception as e:
      print(f'Error sending TCP response: {e}')

  def __join_room(self, room_name, address):
    if room_name not in self.__rooms:
      self.__send_response(StatusCodes.ROOM_NOT_FOUND, address)
      return
    
    self.__rooms[room_name]['members'].append(address)
    self.__send_tcp_response(address, room_name, Operation.JOIN_ROOM.value, State.COMPLETED.value, StatusCodes.SUCCESS)

if __name__ == "__main__":
  chat_server = ChatServer()
  chat_server.start()