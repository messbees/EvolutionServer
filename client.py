#!/usr/bin/env python

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
    print(json)
    print("Sending your {} request...".format(json["action"]))
    response = requests.post('http://159.100.247.47:8888', json=json)
    print(response.json)
    if (response == 200):
        print("YES!!!")

def room_connect(args):
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

	else:
		raise EvolutionClientException("invalid command: {}".format(args.command))

if __name__ == "__main__":
    main()
