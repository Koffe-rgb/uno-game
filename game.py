from entities.piles import DiscardPile, DrawPile
import questionary as qs

#TODO: боты, правила для первой карты, чистка кода, улучшить UI, ini


class Game:
  def __init__(self) -> None:
    from entities.card import shuffle_deck, generate_deck
    from entities.player import generate_players

    self.uno_deck = shuffle_deck( generate_deck() )
    self.discard_pile = DiscardPile()
    self.draw_pile = DrawPile(self.uno_deck, self.discard_pile)

    self.players = generate_players(4, 2, 0, self.discard_pile, self.draw_pile, self)

    self.turn = 0
    self.direction = 1
    self.discard_pile.discard(self.draw_pile.draw())


  def check_victory_condition(self) -> bool:
    playing = True
    for player in self.players:
      playing = playing and not player.is_empty()
    return playing
  

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

      qs.print(f'\nCard on top of discard pile: ', 'bold fg:darkorange', end='')
      qs.print(str(top_card), style=top_card.title[0][0])
      print(f'Direction {dir}')
      qs.print(f'{cur_player.name}', 'fg:yellow', end='')
      print('\'s turn')
      
      cur_player.do_turn()

      self.increment_turn()
      playing = self.check_victory_condition()

    print('End of the game')

if __name__ == '__main__':
  game = Game()
  game.start_game()