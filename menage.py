from termcolor import cprint
import datetime
import time
import json
import os

SERVER_ID = 'xxxxxx'

def get_database():
    with open(SERVER_ID + '.json', 'r') as database_file:
        database = json.load(database_file)
    return database 

def search_player():
    database = get_database()

    while True:
        os.system('cls||clear')
        print("Search method:")
        print("1. SteamID")
        print("2. Name")
        print("3. Back")
        choice = input("> ")
        os.system('cls||clear')

        match choice:
            case "1":
                print("Enter SteamID:")
                steamid = input("> ")
                os.system('cls||clear')
                for player in database:
                    if player['steam_id'] == steamid:
                        print(player['steam_id'] + " | " + player['name'])
                        print("Joined: " + datetime.datetime.fromtimestamp(player['joined']).strftime('%Y-%m-%d %H:%M:%S') + " | ", end="")
                        cprint(player['status'], 'green' if player['status'] == 'online' else 'red')
                        if player['status'] == 'offline':
                            print("Left: " + datetime.datetime.fromtimestamp(player['left']).strftime('%Y-%m-%d %H:%M:%S') + "\n")
                        else:
                            print("Left: -\n")
                        input("Press enter to continue...")
                        break
                else:
                    print("No players found\n")
                    input("Press enter to continue...")
            case "2":
                print("Enter name:")
                name = input("> ")
                os.system('cls||clear')
                for player in database:
                    if player['name'].lower() == name.lower():
                        print(player['steam_id'] + " | " + player['name'])
                        print("Joined: " + datetime.datetime.fromtimestamp(player['joined']).strftime('%Y-%m-%d %H:%M:%S') + " | ", end="")
                        cprint(player['status'], 'green' if player['status'] == 'online' else 'red')
                        if player['status'] == 'offline':
                            print("Left: " + datetime.datetime.fromtimestamp(player['left']).strftime('%Y-%m-%d %H:%M:%S') + "\n")
                        else:
                            print("Left: -\n")
                        input("Press enter to continue...")
                        break
                else:
                    print("No players found\n")
                    input("Press enter to continue...")
            case "3":
                break
            case _:
                os.system('cls||clear')

def display_online_players():
    database = get_database()
    i = 0

    os.system('cls||clear')
    for player in database:
        if player['status'] == 'online':
            print(player['steam_id'] + " | " + player['name'])
            print("Joined: " + datetime.datetime.fromtimestamp(player['joined']).strftime('%Y-%m-%d %H:%M:%S') + " | ", end="")
            cprint(player['status'] + "\n", 'green')
            i += 1
    cprint("Players: " + str(i) + "\n", 'yellow')
    input("Press enter to continue...")

def display_offline_players():
    database = get_database()
    i = 0

    os.system('cls||clear')
    for player in database:
        if player['status'] == 'offline':
            print(player['steam_id'] + " | " + player['name'])
            print("Joined: " + datetime.datetime.fromtimestamp(player['joined']).strftime('%Y-%m-%d %H:%M:%S') + " | ", end="")
            cprint(player['status'], 'red')
            print("Left: " + datetime.datetime.fromtimestamp(player['left']).strftime('%Y-%m-%d %H:%M:%S') + "\n")
            i += 1
    cprint("Players: " + str(i) + "\n", 'yellow')
    input("Press enter to continue...")

def display_all_players():
    database = get_database()
    i = 0

    os.system('cls||clear')
    for player in database:
        print(player['steam_id'] + " | " + player['name'])
        print("Joined: " + datetime.datetime.fromtimestamp(player['joined']).strftime('%Y-%m-%d %H:%M:%S') + " | ", end="")
        cprint(player['status'], 'green' if player['status'] == 'online' else 'red')
        if player['status'] == 'offline':
            print("Left: " + datetime.datetime.fromtimestamp(player['left']).strftime('%Y-%m-%d %H:%M:%S') + "\n")
        else:
            print("Left: -\n")
        i += 1
    cprint("Players: " + str(i) + "\n", 'yellow')
    input("Press enter to continue...")


if __name__ == '__main__':    
    while True:
        os.system('cls||clear')
        print("Players history menager:")
        print("1. Search player")
        print("2. Display online players")
        print("3. Display offline players")
        print("4. Display all players")
        print("5. Exit")
        choice = input("> ")

        match choice:
            case "1":
                search_player()
            case "2":
                display_online_players()
            case "3":
                display_offline_players()
            case "4":
                display_all_players()
            case "5":
                os.system('cls||clear')
                exit()
            case _:
                os.system('cls||clear')