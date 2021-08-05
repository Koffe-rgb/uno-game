from configparser import ConfigParser
from validators import HandSizeValidator, NumberValidator
from prompt_toolkit.shortcuts import CompleteStyle
from game import Game
import sys
import questionary as qs

SECTION = 'Options'
NUM_PLAYERS = 'Number of players'
NUM_BOTS = 'Number of bots'
HAND_SIZE = 'Hand size'


def start(config : ConfigParser):
  game = Game(config)
  game.start_game()


def setup(config : ConfigParser):

  def set_players(config : ConfigParser):
    n = qs.text('Input number of players: ', validate=NumberValidator).ask()
    config[SECTION][NUM_PLAYERS] = n


  def set_bots(config : ConfigParser):
    n = qs.text('Input number of bots: ', validate=NumberValidator).ask()
    config[SECTION][NUM_BOTS] = n


  def set_hand_size(config : ConfigParser):
    n = qs.text('Input number of bots: ', validate=HandSizeValidator).ask()
    config[SECTION][HAND_SIZE] = n


  def save_to_file(config : ConfigParser):
    path = qs.path(
      'Input path to save your preferences: ', 
      complete_style=CompleteStyle.COLUMN
      ).ask()
    try:
      with open(path, 'w+') as configfile:
        config.write(configfile)
    except FileExistsError:
      qs.print('Error occured, file with this name already exists', 'fg:red')
    except:
      qs.print('Error occured, couldn\'t save file', 'fg:red')


  def load_from_file(config : ConfigParser):
    path = qs.path(
      'Input path to file of your preferences: ', 
      complete_style=CompleteStyle.COLUMN
      ).ask()
    try:
      config.read(path)
    except FileNotFoundError:
      qs.print('Error ocurred, file not found', 'fg:red')
    except:
      qs.print('Error occured, couldn\'t read file', 'fg:red')


  def back_to_main(config : ConfigParser):
    return 'ExIt FrOm ThE mEnU'
    
  choice = ''
  choices = {
    'Set number of players' : set_players,
    'Set number of bots' : set_bots,
    'Set size of hand' : set_hand_size,
    'Save preferences to file' : save_to_file,
    'Load preferences from file' : load_from_file,
    'Close options' : back_to_main
  }

  while choice != list(choices.keys())[-1]:
    choice = qs.select(
      'Select an option:',
      choices=choices.keys(),
      show_selected=True
    ).ask()

    choices[choice](config)


def end():
  sys.exit()


def main():
  config = ConfigParser()
  options = {
    NUM_PLAYERS : '1',
    NUM_BOTS : '3',
    HAND_SIZE : '4'
  }
  config[SECTION] = options
  
  choices = {
    'Start the game' : start,
    'Setup the game' : setup,
    'Quit' : end
  }

  qs.print('  Welcome to the game UNO  ', 'bold fg:blue bg:white')

  while True:
    choice = qs.select(
      message='Choose the option:',
      choices=choices.keys(),
      show_selected=True
    ).ask()
    
    if choice == list(choices.keys())[-1]:
      choices[choice]()
    else:
      choices[choice](config)


if __name__ == '__main__':
  main()