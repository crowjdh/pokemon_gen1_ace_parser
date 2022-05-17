from abc import ABC, abstractmethod

from character import BaseCharacter, Character, LongCharacter
from code.commands import COMMANDS
from code.bit_operations import BIT_OPERATIONS
from code.status_flags import (
  STATUS_FLAGS,
  STATUS_FLAG_XX,
  STATUS_FLAG_YYXX,
)

class BaseCommand(ABC):
  character = None

  def __init__(self, character):
    self.character = character

  @property
  @abstractmethod
  def command_format(self):
    pass

  def __str__(self):
    return self.command_format

  @property
  def description(self):
    return f'{str(self)}  ; {self.character}'

  @staticmethod
  def is_convertible(character):
    return False

  @staticmethod
  @abstractmethod
  def from_character(character, arg_characters=None):
    pass

  @staticmethod
  def get_command_class(character):
    if BitCommand.is_convertible(character):
      return BitCommand
    elif XXCommand.is_convertible(character):
      return XXCommand
    elif YYXXCommand.is_convertible(character):
      return YYXXCommand
    else:
      return NoArgsCommand

  @staticmethod
  def get_target_character_count():
    return 0

  @staticmethod
  def get_longest_character(chars):
    bit_command_prefix = BitCommand.BASE_CHARACTER.char
    if chars[0] == bit_command_prefix:
      longest_chars = BaseCharacter.get_longest_chars(chars[1:])
      return LongCharacter([bit_command_prefix, *longest_chars])
    else:
      return BaseCharacter.get_longest_character(chars)

# ガ, dec b
class NoArgsCommand(BaseCommand):

  @staticmethod
  def from_character(character, arg_characters=None):
    return NoArgsCommand(character)

  @property
  def command_format(self):
    return COMMANDS[self.character.code]

  def __eq__(self, other):
    if not isinstance(other, NoArgsCommand):
      return False

    return self.character.code == other.character.code

# ギ, ld b,{xx}
class XXCommand(NoArgsCommand):
  xx_character = None

  def __init__(self, character, xx_character):
    super().__init__(character)
    self.xx_character = xx_character

  @staticmethod
  def from_character(character, arg_characters=None):
    return XXCommand(character, arg_characters[0])

  def __str__(self):
    return self.command_format.format(xx=self.xx_character.code)

  @property
  def description(self):
    return f'{str(self)}  ; {self.character}{self.xx_character}'

  @staticmethod
  def get_target_character_count():
    return 1

  @staticmethod
  def is_convertible(character):
    return character.status_flags & STATUS_FLAG_XX > 0

# ゲ, ld bc,{yy}{xx}
class YYXXCommand(XXCommand):
  yy_character = None

  def __init__(self, character, yy_character, xx_character):
    super().__init__(character, xx_character)
    self.yy_character = yy_character

  @staticmethod
  def from_character(character, arg_characters=None):
    return YYXXCommand(character, arg_characters[0], arg_characters[1])

  def __str__(self):
    return self.command_format.format(xx=self.xx_character.code, yy=self.yy_character.code)

  @property
  def description(self):
    return f'{str(self)}  ; {self.character}{self.yy_character}{self.xx_character}'

  @staticmethod
  def get_target_character_count():
    return 2

  @staticmethod
  def is_convertible(character):
    return character.status_flags & STATUS_FLAG_YYXX > 0

# ひガ, rlc l
class BitCommand(BaseCommand):
  BASE_CHAR = 'ひ'
  BASE_CHARACTER = Character(BASE_CHAR)

  character = None

  def __init__(self, character):
    self.character = character

  @property
  def bit_character(self):
    char_or_chars = str(self.character)[1:]
    if len(char_or_chars) == 1:
      return Character(char_or_chars[0])
    else:
      return LongCharacter(char_or_chars)

  @staticmethod
  def from_character(character, arg_characters=None):
    return BitCommand(character)
  
  @property
  def command_format(self):
    return BIT_OPERATIONS[self.bit_character.code]

  @staticmethod
  def is_convertible(character):
    if not isinstance(character, LongCharacter):
      return False

    long_character = character
    return long_character[0] == BitCommand.BASE_CHAR

TERMINAL_COMMAND = NoArgsCommand(Character('\n'))
