import sys
from parser import Parser
from command import TERMINAL_COMMAND

def main(cmd_file_path):
  with open(cmd_file_path, 'r') as raw_command_file:
    raw_command_lines = raw_command_file.readlines()
    parser = Parser(raw_command_lines)
    parser.parse()

    for command in parser.commands:
      print_command(command)

def print_command(command):
  description = command.description
  if command == TERMINAL_COMMAND:
    description = f'({description})\n'

  print(description)


if __name__ == '__main__':
  if len(sys.argv) < 2:
    print("Usage: python main.py PATH_TO_RAW_CMD_FILE")
    exit(-1)

  cmd_file_path = sys.argv[1]
  main(cmd_file_path)
