from prompt_toolkit.document import Document
from questionary import Validator, ValidationError

def is_int(s : str):
  try: 
    int(s)
    return True
  except ValueError:
    return False

class NumberValidator(Validator):
  def validate(self, document: Document) -> None:
    if not is_int(document.text.strip()):
      raise ValidationError(
        cursor_position=0, 
        message='Please enter a integer'
        )
    elif not 1 <= int(document.text.strip()) <= 4:
      raise ValidationError(
        cursor_position=0, 
        message='The number of players should be between 1 and 4'
        )

class HandSizeValidator(Validator):
  def validate(self, document: Document) -> None:
    if not is_int(document.text.strip()):
      raise ValidationError(
        cursor_position=0, 
        message='Please enter a integer'
        )
    elif not 4 <= int(document.text.strip()) <= 6:
      raise ValidationError(
        cursor_position=0, 
        message='The hand size should be between 4 and 6'
        )