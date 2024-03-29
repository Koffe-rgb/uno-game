from game import Game
from entities.piles import DiscardPile, DrawPile
from entities.card import Card, colors_ru_en
from entities.bot import Bot
import questionary as qs

white_answer_style = qs.Style([
  ('answer', 'fg:white')
])

class Player:
  def __init__(self, name : str, hand_size : int, discard_pile : DiscardPile, draw_pile : DrawPile, game : Game) -> None:
    self.name = name
    self.hand = draw_pile.slice_top(hand_size)
    self.discard_pile = discard_pile
    self.draw_pile = draw_pile
    self.game = game

    self.actions = {
      'Пропусти ход' : self.play_skip,
      'Наоборот' : self.play_reverse,
      'Возьми 2' : self.play_draw_2,
      'Закажи цвет и возьми 4' : self.play_draw_4,
    }
  

  def can_play(self, top_card : Card, player_hand : list) -> bool:
    for card in player_hand:
      if card.color == '': # 'Wild' and 'Wild Draw 4' doesn't have color
        return True
      elif top_card.color == card.color or top_card.action == card.action:
        return True
    return False
  

  def play_wild(self, wild_card : Card):
    selected_color = qs.select(
      message='Заказывайте цвет',
      choices=colors_ru_en.keys(),
      use_shortcuts=False,
      instruction='(Используйте стрелки)',
      style=white_answer_style
    ).ask()

    wild_card.color = selected_color
    wild_card.title = wild_card.create_title()
    

  def play_skip(self) -> None:
    self.game.increment_turn()


  def play_reverse(self) -> None:
    self.game.reverse_direction()
  

  def play_draw(self, num : int) -> None:
    next_player = self.game.get_next_player()
    for _ in range(num):
      if not self.draw_pile.is_empty():
        next_player.hand.append(self.draw_pile.draw())


  def play_draw_2(self) -> None:
    self.play_draw(2)


  def play_draw_4(self) -> None:
    self.play_draw(4)


  def play_card(self, selected_card : Card) -> bool:
    top_card = self.discard_pile.top()

    if self.can_play(top_card, [ selected_card ]):
      self.hand.remove(selected_card)
      
      if selected_card.color == '': # 'Wild' AND 'Wild Draw 4'
        self.play_wild(selected_card)

      if selected_card.action in self.actions: # 'Skip', 'Draw 2', 'Reverse' AND 'Wild Draw 4'
        self.actions[ selected_card.action ]()

      self.discard_pile.discard(selected_card)
      return True

    else:
      qs.print('Неподходящая карта. Пожалуйста, выберите другую карту', 'fg:red')
      return False
  

  def make_choice(self) -> None:
    correct_choice = False
    while not correct_choice:
      selected_card = qs.select(
        message='Выберите карту для сброса:',
        choices=self.hand,
        use_shortcuts=False,
        instruction='(Используйте стрелки)',
        style=white_answer_style
        ).ask()
      correct_choice = self.play_card(selected_card)  
  
  
  def is_empty(self) -> bool:
    return len(self.hand) == 0
  

  def do_turn(self) -> None:
    top_card = self.discard_pile.top()

    if not self.can_play(top_card, self.hand):
      self.draw_cards(top_card)
      
    self.make_choice()


  def draw_cards(self, top_card):
    qs.select(
      message='У вас нет подходящих карт',
      choices=[ 'Тянуть карты' ],
      use_shortcuts=False,
      instruction='(Используйте стрелки)',
      style=white_answer_style
    ).ask()
    
    self.game.turn_counts[self] = 0
    if not self.draw_pile.is_empty():
      drawn_card = self.draw_pile.draw()
      drawns = [ drawn_card ]

      while not self.draw_pile.is_empty() and not self.can_play(top_card, [ drawn_card ]):
        drawn_card = self.draw_pile.draw()
        drawns.append(drawn_card)
      
      qs.print(f'Вы вытянули следующие карты: ' + ', '.join(str(card) for card in drawns))
      self.hand.extend(drawns)


def generate_players(hand_size : int, player_count : int, bot_count : int, discard_pile : DiscardPile, draw_pile : DrawPile, game : Game) -> list[Player]:
  players = []
  for i in range(player_count):
    player = Player(f'Игрок {i + 1}', hand_size, discard_pile, draw_pile, game)
    players.append(player)
  
  for i in range(bot_count):
    bot = Bot(f'Бот {i + 1}', hand_size, discard_pile, draw_pile, game)
    players.append(bot)
  
  return players