import subprocess
from enum import Enum

from graphics.graphics import Graphics

class MenuState(Enum):
  MAIN_MENU = 0
  CREATE_SERVER = 1
  JOIN_SERVER = 2

class Menu:
  def __init__(self) -> None:
    self.graphics = Graphics()
    self.client_state = MenuState.MAIN_MENU

  def update_menu(self, host_info, server_fields):
    if self.client_state == MenuState.MAIN_MENU:
      self.graphics.display_main_menu()
    elif self.client_state == MenuState.CREATE_SERVER:
      self.graphics.display_create_server_menu(host_info)
    elif self.client_state == MenuState.JOIN_SERVER:
      self.graphics.display_join_server_menu(server_fields)

  def process_menu_commands(self, server, server_fields, command=str):
    if self.client_state == MenuState.MAIN_MENU:
      self.handle_main_menu_command(command)
    elif self.client_state == MenuState.CREATE_SERVER:
      self.handle_create_server_command(server, command)
    elif self.client_state == MenuState.JOIN_SERVER:
      self.handle_join_server_command(server, server_fields, command)

  def handle_main_menu_command(self, command: str):
    print(command)
    if command == 'create server':
      self.client_state = MenuState.CREATE_SERVER
    if command == 'join server':
      self.client_state = MenuState.JOIN_SERVER
    elif command == 'quit':
      self.quit = True

  def handle_create_server_command(self, server, command: str):
    if command is not None:
      subprocess.Popen(['python', 'server_launcher.py', command])
      host_info = server.get_host_info()
      server.join_server({ 'IP_ADDRESS': host_info['ip_address'], 'PORT': 58008, 'PASSWORD': command })

  def handle_join_server_command(self, server, server_fields, command: str):
    if server_fields['IP_ADDRESS'] is None:
      server_fields['IP_ADDRESS'] = command
    elif server_fields['PORT'] is None:
      server_fields['PORT'] = command
    elif server_fields['PASSWORD'] is None:
      server_fields['PASSWORD'] = command
      server.join_server(server_fields)
