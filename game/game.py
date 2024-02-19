from enum import Enum

from question_repo.question_repo import QuestionRepo

MAX_PLAYERS = 2

class GameState(Enum):
  SET_NAME = 0
  PLAY = 1

class Game:
  def __init__(self) -> None:
    self.question_repo = QuestionRepo()
    self.players = []
    self.game_state = GameState.SET_NAME

  def register_user(self, ip_address):
    self.players.append(Player(ip_address))

  def remove_user(self, ip_address):
    self.players = [player for player in self.players if player.ip_address != ip_address]

  def process_game_command(self, client_ip, command: str, outbuffer):
    if self.game_state == GameState.SET_NAME:
      for player in self.players:
        if player.ip_address == client_ip:
          player.set_name(command)
          print(f'(ip_address: {player.ip_address}, name: {player.name} score: {player.score})')

  def update_game(self):
    #self.question_repo.get_new_question()
    if self.game_state == GameState.SET_NAME:
      pass

  def is_game_ready(self):
    return True
    return len(self.players) == MAX_PLAYERS

  def is_selecting_name(self):
    return self.game_state == GameState.SET_NAME

class Player:
  def __init__(self, ip_address) -> None:
    self.ip_address = ip_address
    self.name = ''
    self.score = 0
  
  def set_name(self, name):
    self.name = name

  def set_score(self, score):
    self.score = score
