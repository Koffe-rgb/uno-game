from game import Game
from entities.piles import DiscardPile, DrawPile
from entities.card import Card, colors
from random import randrange
from time import sleep

class Bot:
  def __init__(self, name : str, hand_size : int, discard_pile : DiscardPile, draw_pile : DrawPile, game : Game) -> None:
    self.name = name
    self.hand = draw_pile.slice_top(hand_size)
    self.discard_pile = discard_pile
    self.draw_pile = draw_pile
    self.game = game

    self.actions = {
      'Skip' : self.play_skip,
      'Reverse' : self.play_reverse,
      'Draw 2' : self.play_draw_2,
      'Wild Draw 4' : self.play_draw_4,
    }
  

  def can_play(self, top_card : Card, player_hand : list) -> bool:
    for card in player_hand:
      if card.color == '': # 'Wild' and 'Wild Draw 4' doesn't have color
        return True
      elif top_card.color == card.color or top_card.action == card.action:
        return True
    return False
  

  def play_wild(self, wild_card : Card):   
    selected_color = colors[randrange(len(colors))]

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
      return False
  
  
  def first_specific_card(self, iterable, condition = lambda x : True) -> Card:
    return next(filter(condition, iterable), None)


  def make_choice(self) -> None:
    top_card = self.discard_pile.top()
    active_cards = [card for card in self.hand if self.can_play(top_card, [ card ])]
    next_player = self.game.get_next_player()
    selected_card = None
    
    # if next player about to win, try to add to his hand more cards or reverse direction of game or skip them
    if len(next_player.hand) < 2:
      selected_card = self.first_specific_card(active_cards, lambda card: card.action.startswith('Draw') 
                                               or card.action == 'Reverse' 
                                               or card.action == 'Skip')
    # needs condition for wild cards. perfect solution - when next player drawn cards last their turn 
    elif 0 <= self.game.turn_counts[next_player] <= 2:
      selected_card = self.first_specific_card(active_cards, lambda card: card.color == '')
      
    if selected_card == None:
      selected_card = active_cards[randrange(len(active_cards))]
    
    self.play_card(selected_card)
    
  
  
  def is_empty(self) -> bool:
    return len(self.hand) == 0
  

  def do_turn(self) -> None:
    top_card = self.discard_pile.top()

    if not self.can_play(top_card, self.hand):
      self.draw_cards(top_card)

    self.make_choice()
    # sleep(1)


  def draw_cards(self, top_card):
    print(f'{self.name} can\' play any card. {self.name} starts to draw')
    self.game.turn_counts[self] = 0
    
    if not self.draw_pile.is_empty():
      drawn_card = self.draw_pile.draw()
      drawns = [ drawn_card ]

      while not self.draw_pile.is_empty() and not self.can_play(top_card, [ drawn_card ]):
        drawn_card = self.draw_pile.draw()
        drawns.append(drawn_card)
      
      self.hand.extend(drawns)