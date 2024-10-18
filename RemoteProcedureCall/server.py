import socket
import threading
import json

class RPCServer:
  def __init__(self, host='localhost',port=8080):
    self.host = host
    self.port = port
    self.methods = {
      'floor': self.floor,
      'nroot': self.nroot,
      'reverse': self.reverse,
      'validAnagram': self.validAnagram,
      'sort': self.sort,
    }
  
  def floor(self, x):
    return int(x)

  def nroot(self, x, n):
    return x**(1/n)
  
  def reverse(self, s):
    return s[::-1]

  def validAnagram(self, s, t):
    return sorted(s) == sorted(t)
  
  def sort(self, arr):
    return sorted(arr)
  
  def handle_request(self, request):
    try:
      method = request['method']
      params = request['params']
      print(params)
      id = request['id']
      response = self.methods[method](*params)
      print(response)
      return {
        'id': id,
        'response': response,
      }
    except Exception as e:
      return str(e)

  def handle_client(self, client_socket):
    while True:
      try:
        data = client_socket.recv(1024)
        if not data:
            break
        request = json.loads(data.decode("utf-8")) 
        print(f"[*] Received: {request}")
        response = self.handle_request(request)
        client_socket.send(json.dumps(response).encode("utf-8"))
      except Exception as e:
        print(f"[-] Error: {e}")
        break
    client_socket.close()
  
  def start_server(self):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((self.host, self.port))
    server.listen(5)
    print(f"[*] Listening on {self.host}:{self.port}")

    while True:
      client, addr = server.accept()
      print(f"[*] Accepted connection from: {addr[0]}:{addr[1]}")
      client_handler = threading.Thread(target=self.handle_client, args=(client,))
      client_handler.start()


if __name__ == "__main__":
  rpc_server = RPCServer()
  rpc_server.start_server()