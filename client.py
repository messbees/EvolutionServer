#!/usr/bin/env python

import argparse
import requests
import logging
import argparse_helper

nick = "messbees"

def new_room(args):
    name = args.name
    admin = nick
    json = {}
    json["action"] = "ROOM_NEW"
    json["room_new"] = {}
    json["room_new"]["game"] = name
    json["room_new"]["player"] = admin
    print(json)
    print("Sending your {} request...".format(json["action"]))
    response = requests.post('http://159.100.247.47:8888', json=json)
    print(response)

def connect_to_room(args):
    name = args.name
    player = args.player
    json = {}
    json["action"] = "ROOM_CONNECT"
    json["room_connect"] = {}
    json["room_connect"]["game"] = name
    json["room_connect"]["player"] = player
    print(json)
    print("Sending your {} request...".format(json["action"]))
    response = requests.post('http://159.100.247.47:8888', json=json)
    print(response)

def main(prog_name=os.path.basename(sys.argv[0]), args=None):
	if args is None:
		args = sys.argv[1:]
	parser = create_parser(prog_name)
	args = parser.parse_args(args)

	if args.verbose is None:
		verbose_level = 0
	else:
		verbose_level = args.verbose
	setup_loggers(verbose_level=verbose_level)

	if not args.command:
		parser.print_help()
		sys.exit(1)
	if args.command == 'room_new':
		room_new(args)
	elif args.command == 'room_connect':
		room_connect(args)

	else:
		raise EvolutionClientException("invalid command: {}".format(args.command))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Evolution Server Request Client')
    parser.add_argument('action',  help='Action')
    parser.add_argument('game', help='Game ID or Room name')
    parser.add_argument('creature', type=int, help='Creature ID')
    parser.add_argument('сard', type=int, help='Card id')
    args = parser.parse_args()

    main()
