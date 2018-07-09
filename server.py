#!/usr/bin/env python

import argparse
import game
from room import Room
from deck import Deck
from player import Player
import creature, ability
import os
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import json
import exceptions
class Server:
    def __init__(self):
        # why can't i leave it empty?
        print("Server initiated.")

    def load_game(self, id):
        if (os.path.isfile("games/{}.json".format(id))):
            f = open('games/{}.json'.format(id))
            game = json.loads(f.read())
        else:
            return None

    def new_game(self, name, players, deck):
        game = Game(name, players, deck)
        save_game(game)
        return game

    def do_evolution(self, game, player, creature, card):
        if (game.stage == "evolution" and game.turn == player_name):
            if (game.do_evolution(player, creature, card)):
                return true
        return false

    def save_game(self, game):
        game_json = game.json()
        with open('games/{}.json'.format(game.id), 'w') as outfile:
            json.dump(game_json, outfile)
            print("Game {} is saved.".format(game.name))

game_server = Server()

class RequestHandler(BaseHTTPRequestHandler):
    def set_game_server(self, server):
        self.game_server = server

    def do_POST(self):

        print("POST request!")
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        data = json.loads(self.data_string)
        action = data["action"]

        #self.send_header('Content-type', 'application/json')
        # calls after creating new room
        if (action == "ROOM_NEW"):
            game_name = data["room_new"]["game"]
            player_name = data["room_new"]["player"]
            if (os.path.isfile("rooms/{}.json".format(game_name))):
                self.send_response(409)
                self.end_headers()
            else:
                room = Room(game_name, player_name)
                self.send_response(200)
                self.end_headers()

        # calls after creating new room, when connecting to existing room, or while updating current room
        if (action == "ROOM_CONNECT"):
            game_name = data["room_connect"]["game"]
            player_name = data["room_connect"]["player"]
            if (os.path.isfile("rooms/{}.json".format(game_name))):
                f = open('rooms/{}.json'.format(game_name))
                room = json.loads(f.read())
                name = room["name"]
                players = []
                for player in room["players"]:
                    players.append(player)
                admin = room["admin"]
                updated = Room(name, admin)
                for player in players:
                    if not (updated.connect(player)):
                        self.send_response(409)
                        self.end_headers()
                        return
                if not (updated.connect(player_name)):
                    self.send_response(409)
                    self.end_headers()
                    return
                updated.save()
                self.send_response(200)
                self.end_headers()
            else:
                self.send_response(404)
                self.end_headers()

        # calls after beginning the game in room by room admin
        if (action == "ROOM_START"):
            name = data["room_start"]["game"]
            admin = data["room_start"]["player"]
            if not (os.path.isfile("rooms/{}.json".format(name))):
                self.send_response(404)
                self.end_headers()
                return
            f = open('rooms/{}.json'.format(name))
            room = json.loads(f.read())
            if not (room["admin"] == admin):
                self.send_response(403)
                self.end_headers()
            deck = Deck()
            players = []
            index = 0
            for player in room["players"]:
                players.append(Player(player[0], deck))
                index = index + 1 
            game = game_server.new_game(name, players, deck)
            if (os.path.isfile("games/{}.json".format(game.id))):
                self.send_response(500)
                self.end_headers()
            else:
                game.save()
                self.send_response(200)
                self.end_headers()


            f = open('games/{}.json'.format(game.id))
            self.wfile.write(f.read())

        # calls after trying to fetch game
        if (action == "CONNECT"):
            game_name = data["connect"]["game"]
            player_name = data["connect"]["player"]
            for game in game_server.games:
                for player in game.players:
                    if (player_name == player.name):
                        f = open('games/{}.json'.format(game.id))
                        self.wfile.write(f.read())
                        return

            f = open('games/null.json')
            self.wfile.write(f.read())

        if (action == "EVOLUTION"):
            game_id = data["evolution"]["game_id"]
            player_name = data["evolution"]["player"]
            creature = data["evolution"]["creature"]
            card = data["evolution"]["card"]
            game = game_server.load_game(game_id)
            if (game == None):
                self.send_response(404)
                self.end_headers()
                return
            player = None
            for p in game.players:
                if (p.name == player_name):
                    player = p
            if (game_server.do_evolution(game, player, creature, card)):
                self.send_response(200)
                self.end_headers()
                return
            else:
                self.send_response(403)
                self.end_headers()
                return
        return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='HTTP Server')
    parser.add_argument('port', type=int, help='Listening port for HTTP Server')
    parser.add_argument('ip', help='HTTP Server IP')
    args = parser.parse_args()


    print('Listening on {}:{}'.format(args.ip, args.port))
    HTTPserver = HTTPServer((args.ip, args.port), RequestHandler)
    HTTPserver.serve_forever()
