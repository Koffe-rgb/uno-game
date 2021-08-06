from questionary import Choice
from random import randint

actions = ['Пропусти ход', 'Наоборот', 'Возьми 2']
wild_actions = ['Закажи цвет', 'Закажи цвет и возьми 4']

colors_ru_en = {
  'Красная карта' : 'red',
  'Синяя карта' : 'blue',
  'Желтая карта' : 'yellow',
  'Зеленая карта' : 'green'
}

class Card(Choice):
  def __init__(self, color : str, action : str) -> None:
    self.color = color
    self.action = action
    title = self.create_title()
    super().__init__(title, value=self, disabled=None, checked=None, shortcut_key=False)
  

  def to_string(self) -> str:
    return f'{self.color} {self.action}'.strip()
  

  def create_title(self):
    return [(
      f'fg:{colors_ru_en[self.color]}' if self.color != '' else 'fg:white', 
      f'{self.color} {self.action}'.strip() if self.color != '' else self.action
      )]
  

  def __str__(self) -> str:
    return self.to_string()
    
  
  def __repr__(self) -> str:
    return self.to_string()


def generate_deck() -> list[Card]:
  deck = []
  
  for color in colors_ru_en.keys():
    for action in wild_actions:
      deck.append(Card('', action))

    for action in actions:
      deck.append(Card(color, action))
      deck.append(Card(color, action))

    for number in range(0, 10):
      deck.append(Card(color, str(number)))
      deck.append(Card(color, str(number)))

  return deck


def shuffle_deck(deck : list) -> list[Card]:
  for card_pos in range(len(deck)):
    rand_pos = randint(0, len(deck)-1)
    deck[card_pos], deck[rand_pos] = deck[rand_pos], deck[card_pos]
  return deck