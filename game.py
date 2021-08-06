from configparser import ConfigParser
from entities.piles import DiscardPile, DrawPile
import questionary as qs

#TODO: правила для первой карты


class Game:
  def __init__(self, config : ConfigParser) -> None:
    from entities.card import shuffle_deck, generate_deck
    from entities.player import generate_players

    self.uno_deck = shuffle_deck( generate_deck() )
    self.discard_pile = DiscardPile()
    self.draw_pile = DrawPile(self.uno_deck, self.discard_pile)

    hand_size = config['Options'].getint('Hand size')
    player_num = config['Options'].getint('Number of players')
    bot_num = config['Options'].getint('Number of bots')
    self.players = generate_players(hand_size, player_num, bot_num, self.discard_pile, self.draw_pile, self)
    self.turn_counts = {}.fromkeys(self.players, -1)

    self.turn = 0
    self.direction = 1
    self.discard_pile.discard(self.draw_pile.draw())


  def check_victory_condition(self) -> bool:
    playing = True
    for player in self.players:
      playing = playing and not player.is_empty()
    return playing
  
  
  def update_turn_counts(self) -> None:
    for k, v in self.turn_counts.items():
      if v != -1:
        self.turn_counts[k] += 1
  

  def increment_turn(self) -> None:
    self.turn = (self.turn + self.direction) % len(self.players)


  def get_next_player(self):
    next_turn = (self.turn + self.direction) % len(self.players)
    return self.players[next_turn]
  

  def reverse_direction(self) -> None:
    self.direction *= -1


  def start_game(self) -> None:
    playing = True

    while playing:
      top_card = self.discard_pile.top()
      cur_player = self.players[self.turn]
      dir = '-->' if self.direction > 0 else '<--'

      qs.print(f'Последняя карта в стопке сброса:', 'bold fg:purple bg:white', end='')
      qs.print(' ' + str(top_card), style=top_card.title[0][0])
      print(f'Направление хода игры {dir}\n')
      print('Сейчас ходит ', end='')
      qs.print(f'{cur_player.name}', 'fg:purple')
      
      cur_player.do_turn()

      self.increment_turn()
      self.update_turn_counts()
      playing = self.check_victory_condition()
      if not playing:
        qs.print(f'{cur_player.name} победил!', style='bold fg:red')

    print('Конец игры')
    input('Конец игры. Нажмите Enter')