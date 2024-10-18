from audioop import add
import socket
import time

class chatServer:
	def __init__(self):
		self.__host = 'localhost'
		self.__port = 8080
		self.__clients = {} # address and last_active
		self.__server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.__timeout = 10
	
	def start(self):
		self.__server.bind((self.__host, self.__port))
		print('Server started')

		while True:
			try:
				data, address = self.__server.recvfrom(1024)
				print(f'Message: {data.decode("utf-8")}')
				self.__clients[address] = time.time()
				self.handle_data(data, address)

			except Exception as e:
				self.__clients.remove(address)
				print(e)
				break
		self.__server.close()

	def relay_message(self, username, message, sender_id):
		self.cleanup_clients()
		for client in self.__clients:
			if client == sender_id:
				continue
			full_message = f'{username}: {message}'
			self.__server.sendto(full_message.encode(), client)
	
	def handle_data(self, data, sender_id):
		try:
			print(f'Data: {data}')
			str_data = data.decode('utf-8')
			username_length = int(str_data[0])
			username = str_data[1:username_length+1]
			message = str_data[username_length+1:]
			self.relay_message(username, message, sender_id)
		except Exception as e:
			print(f'Error handling data: {e}')
	
	def cleanup_clients(self):
		current_time = time.time()
		for client in list(self.__clients):
			if current_time - self.__clients[client] > self.__timeout:
				print(f'Client {client} timed out')
				del self.__clients[client]

if __name__ == '__main__':
	server = chatServer()
	server.start()