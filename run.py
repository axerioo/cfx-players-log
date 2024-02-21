from termcolor import cprint
from datetime import datetime, timedelta
import random
import time
import requests
import json

SERVER_ID = "xxxxxx"
TIME_BETWEEN_UPDATES = 600
TIME_FORMAT = "%d.%m.%Y %H:%M:%S"
DB_FILE = SERVER_ID + '.json'
API_URL = "https://servers-frontend.fivem.net/api/servers/single/" + SERVER_ID
HEADERS = {'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

def live_data():
    current_time = int(time.time())
    current_time = datetime.fromtimestamp(current_time).strftime(TIME_FORMAT)
    players = []

    response = requests.get(API_URL, headers=HEADERS)

    cprint("[" + current_time + "]", 'yellow')

    if response.status_code == 200:
        print("API Response code: ", end='')
        cprint(str(response.status_code), 'green')

        raw_players_data = response.json()['Data']['players']
        players_online = response.json()['Data']['clients']

        print("Players online: ", end='')
        cprint(str(players_online) + "\n", 'yellow')

        if players_online == 0:
            return None

        for player in raw_players_data:
            sid = player['identifiers'][0].split(':')[1]
            name = player['name']
            players.append([sid, name])

        return players
    else:
        print("API Response code: ", end='')
        cprint(str(response.status_code) + "\n", 'red')

        return None
    
def live_player_index(steamid, live_players):
    for i, p in enumerate(live_players):
        if p[0] == steamid:
            return i
    return -1

def update_data():
    new_info = False
    live_players = live_data()

    with open(DB_FILE, 'r') as database_file:
        database = json.load(database_file)

    if live_players is None:
        cprint("No players online", 'yellow')
        for player in database:
            if player['status'] == 'online':
                new_info = True
                player['status'] = 'offline'
                player['left'] = int(time.time())
    else:
        for player in database:
            if player['status'] == 'online':
                index = live_player_index(player['steam_id'], live_players)
                if index > -1:
                    player['left'] = None
                    live_players.pop(index)
                else:
                    new_info = True
                    player['status'] = 'offline'
                    player['left'] = int(time.time())
                    cprint("Player left: " + player['steam_id'] + " (" + player['name'] + ")", 'red')
            else:
                index = live_player_index(player['steam_id'], live_players)
                if index > -1:
                    new_info = True
                    player['name'] = live_players[index][1]
                    player['status'] = 'online'
                    player['joined'] = int(time.time())
                    player['left'] = None
                    live_players.pop(index)
                    cprint("Player joined: " + player['steam_id'] + " (" + player['name'] + ")", 'green')

    if live_players is not None:
        for player in live_players:
            new_info = True
            database.append({
                'steam_id': player[0],
                'name': player[1],
                'status': 'online',
                'joined': int(time.time()),
                'left': None
            })
            cprint("New player: " + player[0] + " (" + player[1] + ")", 'cyan')

    with open(DB_FILE, 'w') as database_file:
        json.dump(database, database_file, indent=4)

    if not new_info:
        cprint("No new data", 'yellow')

def check_file():
    try:
        with open(DB_FILE, 'r') as database_file:
            pass
    except FileNotFoundError:
        with open(DB_FILE, 'w') as database_file:
            database = []
            json.dump(database, database_file, indent=4)
        cprint("Database created", 'yellow')


if __name__ == '__main__':
    while True:
        check_file()
        update_data()

        random_next_update = random.randint(TIME_BETWEEN_UPDATES - 10, TIME_BETWEEN_UPDATES + 10)
        next_update_date = datetime.now() + timedelta(seconds=random_next_update)
        next_update_date = next_update_date.strftime(TIME_FORMAT)

        print("\nNext update: ", end='')
        cprint(next_update_date + "\n", 'yellow')

        time.sleep(random_next_update)