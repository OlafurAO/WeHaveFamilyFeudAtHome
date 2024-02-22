import random
import json
from enum import Enum

from question_repo.question_repo import QuestionRepo

MAX_PLAYERS = 2

class GameState(Enum):
  SET_NAME = 0
  PLAY = 1

class Game:
  def __init__(self) -> None:
    self.question_repo = QuestionRepo()
    self.question_status = None
    self.players = []
    self.game_state = GameState.SET_NAME

  def register_user(self, ip_address):
    self.players.append(Player(ip_address))

  def remove_user(self, ip_address):
    self.players = [player for player in self.players if player.ip_address != ip_address]

  def process_game_command(self, client_ip, command: str, data):
    if self.game_state == GameState.SET_NAME:
      for player in self.players:
        if player.ip_address == client_ip:
          player.set_name(command)
          print(f'(ip_address: {player.ip_address}, name: {player.name} score: {player.score})')
      if self.is_game_ready():
        self.game_state = GameState.PLAY
      else:
        data.outb += self.get_json_obj('WAITING FOR OTHER PLAYERS...')
    elif self.game_state == GameState.PLAY:
      self.question_status.guess_answer(command, client_ip)


  def update_game(self, data):
    if self.game_state == GameState.SET_NAME:
      return
    elif self.game_state == GameState.PLAY:
      if self.question_status is None:
        self.question_status = QuestionStatus(self.question_repo.get_new_question())
        # TODO: remove and implement buzzer shit
        self.question_status.set_player_answering(random.choice(self.players))
      else:
        pass    

    data.outb += self.get_json_obj()

  def get_json_obj(self, message: str = None):
    return json.dumps({
      'game_state': self.game_state.name,
      'players': [player.__dict__() for player in self.players],
      'question_status': self.question_status.__dict__() 
        if self.question_status is not None else None,
      'message': message
    }).encode()

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

  def __dict__(self):
    return {
      'ip_address': self.ip_address,
      'name': self.name,
      'score': self.score
    }

class QuestionStatus:
  def __init__(self, question_obj) -> None:
    self.question = question_obj['question']
    self.answers = [
      {'answer': answer, 'score': score, 'hide': True}
      for answer, score in question_obj['answers'].items()
    ]
    self.current_total = 0
    self.player_answering = None
    self.strikes = 0

  def set_player_answering(self, player):
    self.player_answering = player
    self.strikes = 0

  def guess_answer(self, answer: str, client_ip):
    for a in self.answers:      
      if a['answer'].lower() == answer.lower() and a['hide'] == True:
        self.current_total += a['score']
        a['hide'] = False

  def __dict__(self):
    return {
      'question': self.question,
      'answers': self.answers,
      'current_total': self.current_total,
      'player_answering': self.player_answering.__dict__(),
      'strikes': self.strikes,
    }