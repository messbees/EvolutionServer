#!/usr/bin/python3

import argparse
import requests
import logging
import argparse_helper
import os
import json
import sys
from exceptions import EvolutionClientException

f = open('settings.json')
settings = json.loads(f.read())
nick = settings["nick"]
version = settings["version"]

def post(json):
    json["version"] = version
    return requests.post('http://159.100.247.47:8888', json=json)

def get(json):
    json["version"] = version
    return requests.get('http://159.100.247.47:8888', json=json)

def room_new(args):
    name = args.name
    admin = nick
    json = {}
    json["action"] = "ROOM_NEW"
    json["room_new"] = {}
    data = json["room_new"]
    data["game"] = name
    data["player"] = admin
    print('Creating room...')
    response = post(json)
    code = response.status_code
    if (code == 200):
        print("Room created!")
        json = {}
        json["action"] = "ROOM_CONNECT"
        json["room_connect"] = {}
        data = json["room_connect"]
        data["game"] = name
        data["player"] = admin
        response = post(json)
        code = response.status_code
        if (code == 200):
            print("You have joined this room.")
        else:
            print("Error while joining...")
    elif (code == 409):
        print("Error. Room with the same name already exists!")

def room_connect(args):
    name = args.name
    player = nick
    json = {}
    json["action"] = "ROOM_CONNECT"
    json["room_connect"] = {}
    data = json["room_connect"]
    data["game"] = name
    data["player"] = player
    print('Connecting to room...')
    response = post(json)
    code = response.status_code
    if (code == 200):
        print("{} have joined this room.".format(player))
    elif (code == 409):
        print("{} is already in this room!".format(player))
    elif (code == 404):
        print("There is no room with name {}".format(name))
    elif (code == 403):
        print("This room was closed.")

def room_update(args):
    name = args.name
    player = nick
    json = {}
    json["action"] = "ROOM_UPDATE"
    json["room_update"] = {}
    data = json["room_update"]
    data["game"] = name
    data["player"] = player
    print('Updating room...')
    response = get(json)
    code = response.status_code
    if (code == 404):
        print('No room with such name.')
        return
    elif (code == 403):
        print('You are not in this room.')
    elif (code == 200):
        json = response.json()
        status = json["status"]
        if (status == "waiting"):
            players = ''
            for player in json["players"]:
                players += player + ', '
            message = "Game is waiting for admin to begin. Players: " + players + "Admin: " + json["admin"]
            print(message)
            return
        elif(status == "playing"):
            print("Game begins! ID: {}".format(json["id"]))
            args.id = json["id"]
            game_update(args)

def room_start(args):
    name = args.name
    player = nick
    json = {}
    json["action"] = "ROOM_START"
    json["room_start"] = {}
    data = json["room_start"]
    data["game"] = name
    data["player"] = player
    print('Beginning the game...')
    response = post(json)
    code = response.status_code
    if (code == 200):
        room_update(args)
    elif (code == 403):
        print("Only game creator is allowed to begin this game!")
    elif (code == 423):
        print("This room was closed.")
    elif (code == 404):
        print("There is no room with name {}".format(name))
    elif (code == 500):
        print("Game with the same id already exists! Please, try again.")

def game_update(args):
    id = args.id
    player = nick
    json = {}
    json["action"] = "GAME_UPDATE"
    json["update"] = {}
    data = json["update"]
    data["game"] = id
    data["player"] = player
    print("Updating the game...")
    response = get(json)
    code = response.status_code
    if (code == 200):
        j = response.json()
        name = j["name"]
        id = j["id"]
        turn = j["turn"]
        round = j["round"]
        stage = j["stage"]
        dice = j["dice"]
        food = j["food"]
        players = []
        for player in j["players"]:
            players.append(player)
        with open('saved_games/{}.json'.format(id), 'w') as outfile:
            json.dump(j, outfile)
        print("Game '{}' (ID: {}). Current round: {}, stage: {}.".format(name, id, round, stage))
        if (turn == nick):
            print("It's YOUR turn!")
        else:
            print("It's {}'s turn.".format(turn))

    elif (code == 403):
        print("You don't have access to this game.")
    elif (code == 404):
        print("There is no game with such ID.")

def game_show(args):
    id = args.id
    if not (os.path.isfile("saved_games/{}.json".format(id))):
        print("No such game found.")
        return
    f = open("saved_games/{}.json".format(id))
    game = json.loads(f.read())
    print("Your hand:")
    print(game["players"][nick]["deck"])

def take(args):
    id = args.id
    creature = args.creature
    card = args.card
    player = nick
    json = {}
    json["action"] = "TAKE"
    json["take"] = {}
    data = json["take"]
    data["game"] = id
    data["player"] = player
    data["creature"] = creature
    data["card"] = card
    response = post(json)
    code = response.status_code
    if (code == 200):
        print("Success!")
    elif (code == 400):
        print("Error while playing card.")


def main(prog_name=os.path.basename(sys.argv[0]), args=None):
	if args is None:
		args = sys.argv[1:]
	parser = argparse_helper.create_parser(prog_name)
	args = parser.parse_args(args)

	if args.verbose is None:
		verbose_level = 0
	else:
		verbose_level = args.verbose
	argparse_helper.setup_loggers(verbose_level=verbose_level)

	if not args.command:
		parser.print_help()
		sys.exit(1)
	if args.command == 'room_new':
		room_new(args)
	elif args.command == 'room_connect':
		room_connect(args)
	elif args.command == 'room_update':
		room_update(args)
	elif args.command == 'room_start':
		room_start(args)
	elif args.command == 'update':
		game_update(args)
	elif args.command == 'show':
		game_show(args)
 	elif args.command == 'take':
		take(args)
	else:
		raise EvolutionClientException("invalid command: {}".format(args.command))

def main_wrapper():
    # pylint: disable=bare-except
    try:
        main()
    except (EvolutionClientException) as err:
        print("Error: {}".format(err), file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        pass
    except SystemExit as e:
        raise e
    except:
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main_wrapper()
