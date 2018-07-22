#!/usr/bin/env python

import argparse
from game import Game
from room import Room
from deck import Deck
from player import Player
import creature, ability
import os
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import json
#from exceptions import EvolutionServerException

class Server:
    self.version = "0.1.1"

    def __init__(self):
        # why can't i leave it empty?
        print("Server initiated.")

    def load_game(self, id):
        if (os.path.isfile("games/{}.json".format(id))):
            f = open('games/{}.json'.format(id))
            game = json.loads(f.read())
            return game
        else:
            return None

    def new_game(self, game, players, deck):
        g = Game('init', name=game, players=players, deck=deck)
        return g

    def new_room(self, game, admin):
        if (os.path.isfile("rooms/{}.json".format(game))):
            return False
        else:
            room = Room(game, admin)
            return True

    def join_room(self, game, new_player):
        if (os.path.isfile("rooms/{}.json".format(game))):
            f = open('rooms/{}.json'.format(game))
            room = json.loads(f.read())
            name = room["name"]
            players = []
            for player in room["players"]:
                players.append(player)
            admin = room["admin"]
            updated = Room(name, admin)
            for player in players:
                if not (updated.connect(player)):
                    return 'WRONG_USER'
            if not (updated.connect(new_player)):
                return 'WRONG_USER'
            updated.save()
            return 'JOINED'
        else:
            return 'WRONG_ROOM'

    def begin_game(self, game, admin):
        if not (os.path.isfile("rooms/{}.json".format(game))):
            return 'WRONG_ROOM'
        f = open('rooms/{}.json'.format(game))
        room = json.loads(f.read())
        if not (room["admin"] == admin):
            return 'NOT_ADMIN'
        deck = Deck()
        players = []
        for player in room["players"]:
            players.append(Player('init', name=player, deck=deck))
        print('Creating game...')
        g = game_server.new_game(game, players, deck)
        if not (os.path.isfile("games/{}.json".format(g.id))):
            g.save()
            print("Game {} begins!".format(g.id))
            return 'BEGIN'
        else:
            print('Game with same id already exists.')
            return 'WRONG_ID'

    def do_evolution(self, game, player, creature, card):
        if (game["stage"] == "evolution"):
            for p in game["players"]:
                if (p["name"] == player):
                    if not (game["turn"] == player):
                        return 'NOT_YOUR_TURN'
                    #if (creature == 999):
            return 'WRONG_USER'
        else:
            return 'WRONG_STAGE'


game_server = Server()

class RequestHandler(BaseHTTPRequestHandler):
    def set_game_server(self, server):
        self.game_server = server

    def do_GET(self):
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        data = json.loads(self.data_string)
        if not (data["version"] == self.game_server.version):
            self.send_response(405)
            self.end_headers()
            return
        action = data["action"]

        # calls after trying to fetch room state
        if (action == "ROOM_UPDATE"):
            game = data["room_update"]["game"]
            player = data["room_update"]["player"]
            if not (os.path.isfile("rooms/{}.json".format(game))):
                for file in os.listdir("games/"):
                    if file.endswith(".json"):
                        f = open(file)
                        game = json.loads(f.read())
                        if (game["name"] == game and game["players"][player] != None):
                            g = {}
                            g["status"] = "playing"
                            g["id"] = game["id"]
                            temp = 'games/{}_connect.json'.format(game["id"])
                            with open(temp, 'w') as outfile:
                                json.dump(g, outfile)
                            f = open(temp)
                            self.send_response(200)
                            self.send_header("Content-type", "application/json")
                            self.end_headers()
                            self.wfile.write(f.read())
                            os.remove(temp)
                            return
                self.send_response(404)
                self.end_headers()
                return
            else:
                f = open('rooms/{}.json'.format(game))
                room = json.loads(f.read())
                room["status"] = "waiting"
                with open('rooms/{}.json'.format(game), 'w') as outfile:
                    json.dump(room, outfile)
                f = open('rooms/{}.json'.format(game))
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(f.read())
                return


        # calls after trying to fetch game state
        if (action == "UPDATE"):
            game = data["update"]["game"]
            player = data["update"]["player"]
            if not (os.path.isfile("games/{}.json".format(game))):
                self.send_response(404)
                self.end_headers()
                return
            f = open('games/{}.json'.format(game))
            g = json.loads(f.read())
            for p in g.players:
                if (player == p.name):
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(f.read())
                    return
            self.send_response(403)
            self.end_headers()


    def do_POST(self):
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        data = json.loads(self.data_string)
        action = data["action"]

        # calls after creating new room
        if (action == "ROOM_NEW"):
            game = data["room_new"]["game"]
            player = data["room_new"]["player"]
            if (game_server.new_room(game, player)):
                self.send_response(200)
                self.end_headers()
            else:
                self.send_response(409)
                self.end_headers()

        # calls after creating new room, when connecting to existing room, or while updating current room
        if (action == "ROOM_CONNECT"):
            game = data["room_connect"]["game"]
            player = data["room_connect"]["player"]
            status = game_server.join_room(game, player)
            if (status == 'WRONG_USER'):
                self.send_response(409)
                self.end_headers()
            elif(status == 'WRONG_ROOM'):
                self.send_response(404)
                self.end_headers()
            elif(status == 'JOINED'):
                self.send_response(200)
                self.end_headers()

        # calls after beginning the game in room by room admin
        if (action == "ROOM_START"):
            game = data["room_start"]["game"]
            admin = data["room_start"]["player"]
            status = game_server.begin_game(game, admin)
            if (status == 'WRONG_ROOM'):
                self.send_response(404)
                self.end_headers()
            elif (status == 'NOT_ADMIN'):
                self.send_response(403)
                self.end_headers()
            elif (status == 'WRONG_ID'):
                self.send_response(500)
                self.end_headers()
            elif (status == 'BEGIN'):
                self.send_response(200)
                self.end_headers()


        if (action == "EVOLUTION"):
            game = data["evolution"]["game_id"]
            player = data["evolution"]["player"]
            creature = data["evolution"]["creature"]
            card = data["evolution"]["card"]
            g = game_server.load_game(game)
            if (g == None):
                self.send_response(404)
                self.end_headers()
                return
            status = game_server.do_evolution(g, player, creature, card)

            if (status == 'WRONG_USER'):
                self.send_response(403)
                self.end_headers()
                return
            for p in game.players:
                if (p.name == player):
                    player = p
            if (game_server.do_evolution(game, player, creature, card)):
                self.send_response(200)
                self.end_headers()
                return
            self.send_response(403)
            self.end_headers()

        return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='HTTP Server')
    parser.add_argument('port', type=int, help='Listening port for HTTP Server')
    parser.add_argument('ip', help='HTTP Server IP')
    args = parser.parse_args()


    print('Listening on {}:{}'.format(args.ip, args.port))
    HTTPserver = HTTPServer((args.ip, args.port), RequestHandler)
    HTTPserver.serve_forever()
