import json
import socket
import selectors
import types
import time
import threading
from question_repo.question_repo import QuestionRepo

MAX_PLAYERS = 2

class Server:
	def __init__(self) -> None:
		self.selector = selectors.DefaultSelector()
		self.connected_clients = []

	def init_server(self, password: str):
		self.question_repo = QuestionRepo()
		self.server_password = password

		host_info = self.get_host_info()
		server_address = (host_info['ip_address'], 58008)

		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
			server_socket.bind(server_address)
			server_socket.listen()
			server_socket.setblocking(False)

			self.selector.register(server_socket, selectors.EVENT_READ, data=None)

			print('\nSERVER STARTED...')

			try:
				while True:
					events = self.selector.select(timeout=86400)
					for key, mask in events:
						if key.data is None:
							self.accept_wrapper(key.fileobj)
						else:
							self.service_connection(key, mask)
			except KeyboardInterrupt:
				print('SHUTTING DOWN....')
			finally:
				server_socket.close()

	def accept_wrapper(self, server_socket):
		client_socket, client_address = server_socket.accept()
		client_socket.setblocking(False)

		self.connected_clients.append(client_address[0])

		data = types.SimpleNamespace(addr=client_address, inb=b'', outb=b'')
		events = selectors.EVENT_READ | selectors.EVENT_WRITE

		self.selector.register(client_socket, events, data=data)
		print(f'CLIENT {client_address} CONNECTED')
		#client_thread = threading.Thread(target=self.handle_connection, args=(client_socket, client_address))
		#client_thread.start()

	def service_connection(self, key: selectors.SelectorKey, mask):
		client_socket = key.fileobj
		data = key.data
		if mask & selectors.EVENT_READ:
			recv_data = client_socket.recv(1024)
			if recv_data:
				data.outb += recv_data
				print('--------------------------')
				print(data.outb.decode())
			else:
				self.selector.unregister(client_socket)
				client_socket.close()
		if mask & selectors.EVENT_WRITE:
			if data.outb:
				print(f'Echoing {data.outb!r} to {data.addr}')
				sent = client_socket.send(data.outb)
				data.outb = data.outb[sent:]

	def run(self):
		#print(self.question_repo.get_new_question())
		pass

	def get_host_info(self):
		hostname = socket.gethostname()
		ip_address = socket.gethostbyname(hostname)
		return { 'hostname': hostname, 'ip_address': ip_address }
