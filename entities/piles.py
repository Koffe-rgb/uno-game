from entities.card import Card, shuffle_deck
import questionary as qs

class DiscardPile:
  def __init__(self) -> None:
    self.pile = []
  

  def __str__(self) -> str:
    return ' -> '.join(self.pile)
  

  def is_empty(self) -> bool:
    return len(self.pile) == 0
  

  def top(self) -> Card:
    if self.is_empty():
      raise Exception('Pile is empty')
    return self.pile[-1]
  

  def discard(self, card : Card) -> None:
    self.pile.append(card)
  

  def clear(self) -> None:
    top_card = self.top()
    self.pile.clear()
    self.discard(top_card)


class DrawPile:
  def __init__(self, deck : list[Card], discard_pile : DiscardPile) -> None:
    self.pile = deck
    self.discard_pile = discard_pile
  

  def __str__(self) -> str:
    return ' -> '.join(self.pile)
  

  def is_empty(self) -> bool:
    return len(self.pile) == 0
  

  def draw(self) -> Card:
    to_return = self.pile.pop()
    
    if self.is_empty():
      self.pile.extend(self.discard_pile.pile[:-1])
      self.pile = shuffle_deck(self.pile)
      self.discard_pile.clear()
      qs.print('Стопка добора была обновлена', 'fg:purple bg:white')
      
    return to_return
  

  def slice_top(self, size : int) -> list[Card]:
    to_return = self.pile[:size]
    self.pile = self.pile[size:]
    return to_return