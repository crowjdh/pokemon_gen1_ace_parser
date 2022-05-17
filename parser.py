from functools import reduce

from character import BaseCharacter, LongCharacter
from command import BaseCommand

class Parser:
  raw_command_lines = None
  commands = None

  def __init__(self, raw_command_lines):
    self.raw_command_lines = raw_command_lines

  def parse(self):
    self.commands = []

    chars = ''.join(self.raw_command_lines)
    while len(chars) > 0:
      command_character = BaseCommand.get_longest_character(chars)
      if command_character is None:
        return

      Command = BaseCommand.get_command_class(command_character)

      consumed_char_len = len(command_character)
      chars = chars[consumed_char_len:]

      target_character_count = Command.get_target_character_count()

      arg_characters = []
      for _ in range(0, target_character_count):
        arg_character = BaseCharacter.get_longest_character(chars)
        if arg_character is None:
          return

        arg_characters.append(arg_character)

        consumed_char_len = len(arg_character)
        chars = chars[consumed_char_len:]

      command = Command.from_character(command_character, arg_characters)
      self.commands.append(command)
