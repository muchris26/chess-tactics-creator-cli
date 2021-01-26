import main
from os import system, name
from json import loads

config_info = loads(open('CONFIG').read())

def sys_clear():
    if name == 'posix':
        system('clear')
    else:
        system('cls')

def main_loop():
    sys_clear()
    print("Player Name: " + config_info["Player"])
    print("Engine: " + config_info["Engine"])
    print("PGN File: " + config_info["PGN File"] + '\n')
    selection = input("Select an option\n" +
                      "1. Run Tactics Creator\n" + 
                      "2. Update Player Name\n")
    if selection == str('1'):
        sys_clear()
        main.main(config_info)
    elif selection == str('2'):
        new_player_name = input("Please enter correct player name: ")
        config_info["Player"] = new_player_name
        main_loop()

main_loop()