import os
from enum import Enum

from server.server import Server
from menu.menu import Menu

class ClientState(Enum):
  MENU = 0
  PLAY = 1

class Client:
  def __init__(self) -> None:
    self.server = Server()
    self.menu = Menu()
    self.client_state = ClientState.MENU
    self.join_server_fields = { 'IP_ADDRESS': None, 'PORT': None, 'PASSWORD': None }
    self.quit = False
    print('\033[38;2;0;255;0m')

  def run(self):
    while not self.quit:
      self.update()
    print('\033[0m')

  def update(self):
    os.system('cls' if os.name == 'nt' else 'clear')
    if ClientState.MENU:
      self.menu.update_menu(self.server.get_host_info(), self.join_server_fields)    
    print('>$', end='')
    self.process_command(input())

  def process_command(self, command: str):
    if ClientState.MENU:
      self.menu.process_menu_commands(self.server, self.join_server_fields, command)
