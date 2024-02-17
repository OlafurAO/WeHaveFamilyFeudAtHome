import os
import time
import socket
import selectors
import types
from enum import Enum

from server.server import Server
from menu.menu import Menu

class ClientState(Enum):
  MENU = 0
  PLAY = 1

class Client:
  def __init__(self) -> None:
    self.server = Server()
    self.selector = selectors.DefaultSelector()
    self.menu = Menu()
    self.client_socket = None
    self.client_state = ClientState.MENU
    self.join_server_fields = { 'IP_ADDRESS': None, 'PORT': None, 'PASSWORD': None }
    self.quit = False
    print('\033[38;2;0;255;0m')

  def run(self):
    while not self.quit:
      self.update()
      
    print('\033[0m')

  def update(self):
    if self.client_state == ClientState.MENU:
      os.system('cls' if os.name == 'nt' else 'clear')
      self.menu.update_menu(self.server.get_host_info(), self.join_server_fields)
    elif self.client_state == ClientState.PLAY:
      pass

    #if self.client_socket is not None:
      

    print('>$', end='')
    self.process_command(input())

  def process_command(self, command: str):
    if self.client_state == ClientState.MENU:
      self.menu.process_menu_commands(self.server, self.join_server_fields, self.join_server, command)
    elif self.client_state == ClientState.PLAY:
      self.send_server_message(command)
      self.receive_server_message()

  def join_server(self, server_fields):
    time.sleep(1)
    # TODO: replace with server_fields values
    server_address = ('192.168.1.86', 58008)
    max_retries = 5

    for attempt in range(max_retries):
      try:
        print(f'\n[ATTEMPT {attempt}] CONNECTING TO SERVER...')
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.setblocking(False)
        self.client_socket.connect_ex(server_address)

        print(f'[ATTEMPT {attempt}] SUCCESSFULLY CONNECTED...\n')

        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(outb=b'')  
        self.selector.register(self.client_socket, events, data=data)

        self.client_state = ClientState.PLAY
        break
      except ConnectionRefusedError:
        time.sleep(1)

  def send_server_message(self, command):
    self.client_socket.sendall(command.encode())

  def receive_server_message(self):
    for key, mask in self.selector.select(timeout=86400):
      if key.data:
        client_socket = key.fileobj
        if mask & selectors.EVENT_READ:
          try:
            recv_data = client_socket.recv(1024)
            if recv_data:
              print(f'RECEIVED MESSAGE FROM SERVER {recv_data.decode()}')
            else:
              # Server closed the connection
              self.quit = True
              break
          except ConnectionResetError:
            print('Connection with server reset unexpectedly.')
            self.quit = True
            break