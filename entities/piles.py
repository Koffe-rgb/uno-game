from entities.card import Card, shuffle_deck

class DiscardPile:
  def __init__(self) -> None:
    self.pile = []
    self.size = 0
  

  def __str__(self) -> str:
    return ' -> '.join(self.pile)
  

  def is_empty(self) -> bool:
    return self.size == 0
  

  def top(self) -> Card:
    if self.is_empty():
      raise Exception('Pile is empty')
    return self.pile[-1]
  

  def discard(self, card : Card) -> None:
    self.pile.append(card)
    self.size += 1
  

  def clear(self) -> None:
    top_card = self.top()
    self.pile.clear()
    self.discard(top_card)
    self.size = 1


class DrawPile:
  def __init__(self, deck : list[Card], discard_pile : DiscardPile) -> None:
    self.pile = deck
    self.size = len(deck)
    self.discard_pile = discard_pile
  

  def __str__(self) -> str:
    return ' -> '.join(self.pile)
  

  def is_empty(self) -> bool:
    return self.size == 0
  

  def draw(self) -> Card:
    if self.is_empty():
      self.pile.extend(self.discard_pile.pile)
      self.pile = shuffle_deck(self.pile)
      self.discard_pile.clear()
      print('Draw pile was renewed, discard pile was emptied')
    self.size -= 1
    return self.pile.pop()
  

  def slice_top(self, size : int) -> list[Card]:
    to_return = self.pile[:size]
    self.pile = self.pile[size:]
    self.size -= size
    return to_return