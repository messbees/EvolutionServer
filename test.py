#!/usr/bin/env python

import argparse
import requests

nick = "messbees"

def new_room(name, admin):
    json = {}
    json["action"] = "ROOM_NEW"
    json["room_new"] = {}
    json["room_new"]["game"] = name
    json["room_new"]["player"] = admin
    print(json)
    print("Sending your {} request...".format(json["action"]))
    response = requests.post('http://159.100.247.47:8888', json=json)
    print(response)

def connect_to_room(name, player):
    json = {}
    json["action"] = "ROOM_CONNECT"
    json["room_connect"] = {}
    json["room_connect"]["game"] = name
    json["room_connect"]["player"] = player
    print(json)
    print("Sending your {} request...".format(json["action"]))
    response = requests.post('http://159.100.247.47:8888', json=json)
    print(response)

def main():
    if (args.action == "ROOM_NEW"):
        new_room(args.game, nick)
        room_connect(args.game, nick)

    if (args.action == "ROOM_СONNECT"):
        room_connect(args.game, nick)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Evolution Server Request Client')
    parser.add_argument('action',  help='Action')
    parser.add_argument('game', help='Game ID or Room name')
    parser.add_argument('creature', type=int, help='Creature ID')
    parser.add_argument('сard', type=int, help='Card id')
    args = parser.parse_args()

    main()
