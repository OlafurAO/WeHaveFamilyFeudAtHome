import json
import socket
import time
import threading
from question_repo.question_repo import QuestionRepo

MAX_PLAYERS = 2

class Server:
	def __init__(self) -> None:
		self.connected_clients = []

	def init_server(self, password: str):
		self.question_repo = QuestionRepo()
		self.server_password = password

		host_info = self.get_host_info()
		server_address = (host_info['ip_address'], 58008)

		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server_socket.bind(server_address)
		self.server_socket.listen(2)

		print('\nSERVER STARTED...')

		try:
			if len(self.connected_clients) < 2:
				client_socket, client_address = self.server_socket.accept()
				client_thread = threading.Thread(target=self.handle_connection, args=(client_socket, client_address))
				client_thread.start()
		finally: 
			self.server_socket.close()

	def join_server(self, server_fields):
		time.sleep(1)
		# TODO: replace with server_fields values
		server_address = ('192.168.1.86', 58008)
		max_retries = 5

		for attempt in range(max_retries):
			try:
				print(f'\n[ATTEMPT {attempt}] CONNECTING TO SERVER...')
				client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				client_socket.connect(server_address)
				print(f'[ATTEMPT {attempt}] SUCCESSFULLY CONNECTED...\n')
				print(client_socket.recv(2048).decode())
				break
			except ConnectionRefusedError:
				time.sleep(1)

	def handle_connection(self, client_socket, client_address):
		self.connected_clients.append(client_address[0])
		while True:
			try:
				data = client_socket.recv(1024).decode()
				print(data)
				#client_socket.sendall('hehehe'.encode())
				pass
			except ConnectionAbortedError:
				break
			finally:
				break

		print(f'disconnected from {client_address}')
		client_socket.close()

	def run(self):
		#print(self.question_repo.get_new_question())
		pass

	def get_host_info(self):
		hostname = socket.gethostname()
		ip_address = socket.gethostbyname(hostname)
		return { 'hostname': hostname, 'ip_address': ip_address }
