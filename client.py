#!/usr/bin/python3

import argparse
import requests
import logging
import argparse_helper
import os
import sys
nick = "messbees"

def room_new(args):
    name = args.name
    admin = nick
    json = {}
    json["action"] = "ROOM_NEW"
    json["room_new"] = {}
    json["room_new"]["game"] = name
    json["room_new"]["player"] = admin
    print("Sending your {} request...".format(json["action"]))
    response = requests.post('http://159.100.247.47:8888', json=json).status_code
    if (response == 200):
        print("Room created!")
        json = {}
        json["action"] = "ROOM_CONNECT"
        json["room_connect"] = {}
        json["room_connect"]["game"] = name
        json["room_connect"]["player"] = admin
        response = requests.post('http://159.100.247.47:8888', json=json).status_code
        if (response == 200):
            print("You have joined this room.")
        else:
            print("Error while joining...")
    elif (response == 409):
        print("Error. Room with the same name already exists!")

def room_connect(args):
    name = args.name
    player = args.player
    json = {}
    json["action"] = "ROOM_CONNECT"
    json["room_connect"] = {}
    json["room_connect"]["game"] = name
    json["room_connect"]["player"] = player
    print("Sending your {} request...".format(json["action"]))
    response = requests.post('http://159.100.247.47:8888', json=json).status_code
    if (response == 200):
        print("{} have joined this room.".format(player))
    elif (response == 409):
        print("{} is already in this room!".format(player))
    elif (response == 404):
        print("There is no room with name {}".format(name))

def room_start(args):
    name = args.name
    player = nick
    json = {}
    json["action"] = "ROOM_CONNECT"
    json["room_start"] = {}
    json["room_start"]["game"] = name
    json["room_start"]["player"] = player
    print("Sending your {} request...".format(json["action"]))
    response = requests.post('http://159.100.247.47:8888', json=json).status_code
    if (response == 200):
        print("Game begins!")
    elif (response == 403):
        print("Only game creator is allowed to begin this game!")
    elif (response == 404):
        print("There is no room with name {}".format(name))
    elif (response == 500):
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
	elif args.command == 'room_start':
		room_start(args)

	else:
		raise EvolutionClientException("invalid command: {}".format(args.command))

if __name__ == "__main__":
    main()
