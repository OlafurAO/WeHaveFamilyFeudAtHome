import os
import threading
import subprocess
from enum import Enum

from server.server import Server
from graphics.graphics import Graphics

class ClientState(Enum):
  MAIN_MENU = 0
  CREATE_SERVER = 1
  JOIN_SERVER = 2
  ENTER_NAME = 3
  PLAY = 4

class Client:
  def __init__(self) -> None:
    self.server = Server()
    self.graphics = Graphics()
    self.client_state = ClientState.MAIN_MENU
    self.join_server_fields = { 'IP_ADDRESS': None, 'PORT': None, 'PASSWORD': None }
    self.quit = False
    print('\033[38;2;0;255;0m')

  def run(self):
    while not self.quit:
      self.update()

    print('\033[0m')

  def update(self):
    #os.system('cls' if os.name == 'nt' else 'clear')

    if self.client_state == ClientState.MAIN_MENU:
      self.graphics.display_main_menu()
    elif self.client_state == ClientState.CREATE_SERVER:
      self.graphics.display_create_server_menu(self.server.get_host_info())
    elif self.client_state == ClientState.JOIN_SERVER:
      self.graphics.display_join_server_menu(self.join_server_fields)

    print('>$ ', end='')
    self.process_command(input())

  def process_command(self, command: str):
    if self.client_state == ClientState.MAIN_MENU:
      self.handle_main_menu_command(command)
    elif self.client_state == ClientState.CREATE_SERVER:
      self.handle_create_server_command(command)
    elif self.client_state == ClientState.JOIN_SERVER:
      self.handle_join_server_command(command)

  def handle_main_menu_command(self, command: str):
    if command == 'create server':
      self.client_state = ClientState.CREATE_SERVER
    if command == 'join server':
      self.client_state = ClientState.JOIN_SERVER
    elif command == 'quit':
      self.quit = True
  
  def handle_create_server_command(self, command: str):
    if command is not None:
      subprocess.Popen(['python', 'server_launcher.py', command])
      host_info = self.server.get_host_info()
      self.server.join_server({ 'IP_ADDRESS': host_info['ip_address'], 'PORT': 58008, 'PASSWORD': command })

  def handle_join_server_command(self, command: str):
    if self.join_server_fields['IP_ADDRESS'] is None:
      self.join_server_fields['IP_ADDRESS'] = command
    elif self.join_server_fields['PORT'] is None:
      self.join_server_fields['PORT'] = command
    elif self.join_server_fields['PASSWORD'] is None:
      self.join_server_fields['PASSWORD'] = command
      self.server.join_server(self.join_server_fields)
