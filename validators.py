from prompt_toolkit.document import Document
from questionary import Validator, ValidationError

def is_int(s : str):
  try: 
    int(s)
    return True
  except ValueError:
    return False


def validate(player_type : str, document):
  if not is_int(document.text.strip()):
      raise ValidationError(
        cursor_position=0, 
        message='Пожалуйста, введите число!'
        )
  elif not 1 <= int(document.text.strip()) <= 4:
    raise ValidationError(
      cursor_position=0, 
      message=f'Количество {player_type} должо быть в промежутке от 1 до 4'
      )


class PlayerNumberValidator(Validator):
  def validate(self, document: Document) -> None:
    validate('игроков', document)


class BotNumberValidator(Validator):
  def validate(self, document: Document) -> None:
    validate('ботов', document)


class HandSizeValidator(Validator):
  def validate(self, document: Document) -> None:
    if not is_int(document.text.strip()):
      raise ValidationError(
        cursor_position=0, 
        message='Пожалуйста, введите число!'
        )
    elif not 4 <= int(document.text.strip()) <= 6:
      raise ValidationError(
        cursor_position=0, 
        message='Размер руки должен быть в промежутке от 4 до 6 карт'
        )