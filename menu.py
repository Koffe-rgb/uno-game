from configparser import ConfigParser
from validators import HandSizeValidator, PlayerNumberValidator, BotNumberValidator
from prompt_toolkit.shortcuts import CompleteStyle
from game import Game
import sys
import os
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
    n = qs.text('Введите количество игроков: ', validate=PlayerNumberValidator).ask()
    config[SECTION][NUM_PLAYERS] = n
    


  def set_bots(config : ConfigParser):
    n = qs.text('Введите количество ботов: ', validate=BotNumberValidator).ask()
    config[SECTION][NUM_BOTS] = n


  def set_hand_size(config : ConfigParser):
    n = qs.text('Введите количество карт в руке в начале игры: ', validate=HandSizeValidator).ask()
    config[SECTION][HAND_SIZE] = n


  def save_to_file(config : ConfigParser):
    path = qs.path(
      'Введите путь и название файла для сохранения настроек: ', 
      complete_style=CompleteStyle.COLUMN
      ).ask()
    try:
      with open(path, 'w+') as configfile:
        config.write(configfile)
    except FileExistsError:
      qs.print('Произошла ошибка, файл с таким именем уже существует', 'fg:red')
    except:
      qs.print('Произошла ошибка, не удалось сохранить файл', 'fg:red')


  def load_from_file(config : ConfigParser):
    path = qs.path(
      'Введите путь до файла настроек, чтобы загрузить настройки: ', 
      complete_style=CompleteStyle.COLUMN
      ).ask()
    try:
      config.read(path)
    except FileNotFoundError:
      qs.print('Произошла ошибка, файл с таким именем не найден', 'fg:red')
    except:
      qs.print('Произошла ошибка, не удалось прочесть файл', 'fg:red')


  def back_to_main(config : ConfigParser):
    return 'ExIt FrOm ThE mEnU'
    
  choice = ''
  choices = {
    'Установить количество игроков' : set_players,
    'Установить количество ботов' : set_bots,
    'Установить количество карт в руке' : set_hand_size,
    'Сохранить настройки' : save_to_file,
    'Загрузить настройки' : load_from_file,
    'Закрыть это окно' : back_to_main
  }

  
  while choice != list(choices.keys())[-1]:
    os.system('cls')
    choice = qs.select(
      'Выберите опцию:',
      choices=choices.keys(),
      instruction='(Используйте стрелки)'
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
    'Начать игру' : start,
    'Настроить игру' : setup,
    'Выйти' : end
  }

  qs.print('  Добро пожаловать в УНО  ', 'bold fg:blue bg:white')

  while True:
    choice = qs.select(
      message='Выберите опцию:',
      choices=choices.keys(),
      instruction='(Используйте стрелки)'
    ).ask()
    
    if choice == list(choices.keys())[-1]:
      choices[choice]()
    else:
      choices[choice](config)


if __name__ == '__main__':
  main()