import json
import socket
import threading
from question_repo.question_repo import QuestionRepo

class Server:
	def __init__(self) -> None:
		pass

	def join_server():
		client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def init_server(self, password: str):
		self.question_repo = QuestionRepo()
		self.server_password = password

		self.host_info = self.get_host_info()
		server_address = (self.host_info['ip_address'], 58008)

		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_socket.bind(server_address)
		self.server_socket.listen(2)

		print('server is listening...')

		try:
			client_socket, client_address = self.server_socket.accept()
			client_thread = threading.Thread(target=self.handle_connection, args=(client_socket, client_address))
			client_thread.start()
		finally: 
			self.server_socket.close()

	def handle_connection(self, client_socket, client_address):
		print(f'connected to {client_address}')
		while True:
			data = client_socket.recv(1024)
			print(data)
			client_socket.sendall(data)

		print(f'disconnected from {client_address}')
		print(client_socket.close())

	def run(self):
		print(self.question_repo.get_new_question())

	def get_host_info(self):
		hostname = socket.gethostname()
		ip_address = socket.gethostbyname(hostname)
		return { 'hostname': hostname, 'ip_address': ip_address }
