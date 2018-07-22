#!/usr/bin/python3

import argparse
import requests
import logging
import argparse_helper
import os
import sys
from exceptions import EvolutionClientException

settings = {}
settings["nick"] = "Admin"
settings["version"] = '0.1.1'
with open('settings.json', 'w') as outfile:
    json.dump(settings, outfile)
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
    json = response.json()
    if (code == 404):
        print('No room with such name.')
        return
    elif(code == 200):
        status = json["status"]
        if (status == "waiting"):
            players = ''
            for player in json["players"]:
                players += player + ', '
            message = "Game is waiting for admin to begin. Players: " + players + "Admin: " + json["admin"]
            print(message)
            return
        elif(status == "playing"):
            print("Game begins!")
            print("ID: {}".format(json["id"]))


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
        print("Game begins!")
    elif (code == 403):
        print("Only game creator is allowed to begin this game!")
    elif (code == 404):
        print("There is no room with name {}".format(name))
    elif (code == 500):
        print("Game with the same id already exists! Please, try again.")

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
