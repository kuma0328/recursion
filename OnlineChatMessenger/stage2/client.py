import socket


class ChatClient:
  def __init__(self, host="localhost", tcp_port=8080, udp_port=8081):
    self.__host = host
    self.__tcp_port = tcp_port
    self.__udp_port = udp_port

    self.__tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.__udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    self.__tcp_socket.connect((self.__host, self.__tcp_port))
    self.__udp_socket.connect((self.__host, self.__udp_port))

  
  def start():
    