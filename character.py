from abc import ABC, abstractmethod

from code.char_codes import CHAR_CODES
from code.status_flags import (
  STATUS_FLAGS,
  STATUS_FLAG_NON_EXISTING,
  STATUS_FLAG_NON_TYPABLE,
  STATUS_FLAG_CONTEXT_DEPENDENT,
  STATUS_FLAG_BUG,
)

class BaseCharacter(ABC):
  @property
  @abstractmethod
  def code(self):
    pass

  @abstractmethod
  def __str__(self):
    pass

  @abstractmethod
  def __len__(self):
    pass

  @property
  def status_flags(self):
    return STATUS_FLAGS[self.code]

  @property
  def is_non_existing_character(self):
    return STATUS_FLAGS[self.code] & STATUS_FLAG_NON_EXISTING > 0

  @property
  def is_non_typable(self):
    return STATUS_FLAGS[self.code] & STATUS_FLAG_NON_TYPABLE > 0

  @property
  def is_context_dependent(self):
    return STATUS_FLAGS[self.code] & STATUS_FLAG_CONTEXT_DEPENDENT > 0

  @property
  def is_bug(self):
    return STATUS_FLAGS[self.code] & STATUS_FLAG_BUG > 0

  @staticmethod
  def from_char_or_chars(char_or_chars):
    chars = char_or_chars
    if not isinstance(chars, list):
      chars = [chars]

    if not BaseCharacter.is_valid_chars(chars):
      return None

    if len(chars) == 1:
      return Character(chars[0])
    else:
      return LongCharacter(chars)

  @staticmethod
  def is_valid_chars(chars):
    return ''.join(chars) in CHAR_CODES

  @staticmethod
  def get_longest_chars(chars):
    char_chunk = []

    for char in chars:
      chars_candidate_str = ''.join([*char_chunk, char])
      if not BaseCharacter.is_valid_chars(chars_candidate_str):
        break

      char_chunk.append(char)

    return char_chunk

  @staticmethod
  def get_longest_character(chars):
    char_chunk = BaseCharacter.get_longest_chars(chars)

    return BaseCharacter.from_char_or_chars(char_chunk)

class Character(BaseCharacter):
  char = None

  def __init__(self, char):
    self.char = char

  @property
  def code(self):
    return CHAR_CODES[self.char]

  def __str__(self):
    if self.char == '\n':
      return '\\n'
    else:
      return self.char

  def __len__(self):
    return 1

class LongCharacter(BaseCharacter):
  xx = None

  def __init__(self, chars):
    self.chars = chars

  @property
  def code(self):
    char_str = ''.join(self.chars)
    return CHAR_CODES[char_str] if char_str in CHAR_CODES else None

  def __str__(self):
    return ''.join(['\\n' if char == '\n' else char for char in self.chars])

  def __len__(self):
    return len(self.chars)

  def __getitem__(self, item):
    return self.chars[item]
