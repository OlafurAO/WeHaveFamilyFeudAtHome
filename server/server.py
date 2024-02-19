import json
import socket
import selectors
import types
import time
import threading

from game.game import Game

class Server:
	def __init__(self) -> None:
		self.selector = selectors.DefaultSelector()
		self.game = Game()
		self.is_game_running = False

	def init_server(self, password: str):
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

		data = types.SimpleNamespace(addr=client_address, inb=b'', outb=b'')
		events = selectors.EVENT_READ | selectors.EVENT_WRITE

		self.selector.register(client_socket, events, data=data)
		print(f'CLIENT {client_address} CONNECTED')
		
		self.game.register_user(client_address[0])
		if self.game.is_game_ready():
			self.is_game_running = True
		
		welcome_message = "Welcome to the server!"
    # Send the welcome message to the client
		data.outb += welcome_message.encode()

		#client_thread = threading.Thread(target=self.handle_connection, args=(client_socket, client_address))
		#client_thread.start()

	def service_connection(self, key: selectors.SelectorKey, mask):
		client_socket = key.fileobj
		data = key.data

		if mask & selectors.EVENT_READ:
			recv_data = client_socket.recv(1024)
			command = recv_data.decode()

			if self.is_game_running:
				if self.game.is_selecting_name():
					print('11111111111111111')
					data.outb += json.dumps({
						'game_state': self.game.game_state.name,
						'message': 'NAME:'
					}).encode()
				
			if recv_data:
				if self.is_game_running:
					print('2222222222222222222')
					self.game.process_game_command(client_socket.getpeername()[0], command, data.outb)
			else:
				self.game.remove_user(client_socket.getpeername()[0])
				self.selector.unregister(client_socket)
				client_socket.close()
		if mask & selectors.EVENT_WRITE:
			if data.outb:
				print('---------------------------')
				sent = client_socket.send(data.outb)
				data.outb = data.outb[sent:]

	def get_host_info(self):
		hostname = socket.gethostname()
		ip_address = socket.gethostbyname(hostname)
		return { 'hostname': hostname, 'ip_address': ip_address }
