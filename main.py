from parser import Parser
from command import TERMINAL_COMMAND

def main():
  with open('samples/raw_command.txt', 'r') as raw_command_file:
    raw_command_lines = raw_command_file.readlines()
    parser = Parser(raw_command_lines)
    parser.parse()

    for command in parser.commands:
      print(command.description)
      if command == TERMINAL_COMMAND:
        print()


if __name__ == '__main__':
  main()
