#!/usr/bin/python3

import argparse
import ability
from ability import get_ability
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
    request = {}
    request["action"] = "ROOM_NEW"
    request["data"] = {}
    data = request["data"]
    data["game"] = name
    data["player"] = admin
    print('Creating room...')
    response = post(request)
    code = response.status_code
    if (code == 200):
        print("Room created!")
        request = {}
        request["action"] = "ROOM_CONNECT"
        request["data"] = {}
        data = request["data"]
        data["game"] = name
        data["player"] = admin
        response = post(request)
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
    request = {}
    request["action"] = "ROOM_CONNECT"
    request["data"] = {}
    data = request["data"]
    data["game"] = name
    data["player"] = player
    print('Connecting to room...')
    response = post(request)
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
    request = {}
    request["action"] = "ROOM_UPDATE"
    request["data"] = {}
    data = request["data"]
    data["game"] = name
    data["player"] = player
    print('Updating room...')
    response = get(request)
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
    request = {}
    request["action"] = "ROOM_START"
    request["data"] = {}
    data = request["data"]
    data["game"] = name
    data["player"] = player
    print('Beginning the game...')
    response = post(request)
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
    request = {}
    request["action"] = "GAME_UPDATE"
    request["data"] = {}
    data = request["data"]
    data["game"] = id
    data["player"] = player
    print("Updating the game...")
    response = get(request)
    code = response.status_code
    if (code == 200):
        game = response.json()
        name = game["name"]
        id = game["id"]
        turn = game["turn"]
        round = game["round"]
        stage = game["stage"]
        dice = game["dice"]
        food = game["food"]
        players = []
        for player in game["players"]:
            players.append(player)
        with open('saved_games/{}.json'.format(id), 'w') as outfile:
            json.dump(game, outfile)
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
    name = game["name"]
    id = game["id"]
    turn = game["turn"]
    round = game["round"]
    stage = game["stage"]
    dice = game["dice"]
    food = game["food"]
    players = []
    for player in game["players"]:
        players.append(player)
    print("Game '{}' (ID: {}). Current round: {}, stage: {}.".format(name, id, round, stage))
    if (turn == nick):
        print("It's YOUR turn!")
    else:
        print("It's {}'s turn.".format(turn))
    print("Your hand:")
    for player in players:
        if (player["name"] == nick):
            cards = ""
            for card in player["cards"]:
                cards += '[{}]: {}, '.format(card, get_card_name(str(card)))
            if (args.creatures):
                print("Your creatures: ")
                for creature in player["creatures"]:
                    print(get_creature_text(creature))

def take(args):
    id = args.id
    creature = args.creature
    card = args.card
    player = nick
    request = {}
    request["action"] = "TAKE"
    request["data"] = {}
    data = request["data"]
    data["game"] = id
    data["player"] = player
    data["creature"] = creature
    data["card"] = card
    response = post(request)
    code = response.status_code
    if (code == 200):
        print("Success!")
    elif (code == 400):
        print("Error while playing card.")
    elif (code == 404):
        print("There is no such game.")

def take_pass(args):
    id = arks.id
    player = nick
    request = {}
    request["action"] = "PASS"
    request["data"] = {}
    data = request["data"]
    data["game"] = id
    data["player"] = player
    response = post(request)
    code = response.status_code
    if (code == 200):
        print("You passes.")
    elif (code == 400):
        print("It is not right time to pass...")
    elif(code == 404):
        print("There is no such game")

def get_creature_text(creature):
    msg = '[Creature {}] Hunger:{}, Food:{}, Fat:{}. \n'.format(creature["id"], creature["hunger"], creature["food"], creature["fat"])
    msg +=  '[Creature {}] Abilities: '
    cards = 0
    for card in creature["cards"]:
        cards = cards + 1
    msg += '{} cards'.format(cards)
    for card in creature["cards"]:
        msg += ', {}'.format(get_card_name(card))
    return msg

def get_card_name(card):
    return get_ability(card).name

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
	elif args.command == 'pass':
		take_pass(args)
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
