#!/usr/bin/env pythonfrom BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

import argparse
import cgi
import game
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from optparse import OptionParser
import simplejson as json
import exceptions

class RequestHandler(BaseHTTPRequestHandler):
    def set_game_server(self, server):
        self.game_server = server

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        request_path = self.path

        print("\n----- Request Start ----->\n")
        print(request_path)
        print(self.headers)
        print("<----- Request End -----\n")

        self.send_response(200)
        self.send_header("Set-Cookie", "foo=bar")

    def do_POST(self):

        print "POST request!"
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))


        data = json.loads(self.data_string)
        action = data["action"]
        
        # calls after creating new room
        if (action == "ROOM_NEW"):
            game_name = data["room_new"]["game"]
            player_name data["room_new"]["player"]
            if (os.path.isfile("rooms/{}.json".format(game_name)):
                self._set_headers()
                self.send_response(409)
                self.end_headers()
            else:
                room = Room(game_name, player_name)
                self._set_headers()
                self.send_response(200)
                self.end_headers()

        # calls after creating new room, when connecting to existing room, or while updating current room
        if (action == "ROOM_CONNECT"):
            game_name = data["room_connect"]["game"]
            player_name = data["room_connect"]["player"]
            if (os.path.isfile("rooms/{}.json".format(game_name)):
                f = open('rooms/{}.json'.format(game_name))
                room = json.loads(f.read())
                if (room.admin == player_name):
                    room["is_admin" == "true"]
                else:
                    room["is_admin" == "false"]
                with open('rooms/{}.json'.format(game_name), 'w') as outfile:
                    json.dump(room, outfile)
                self.wfile.write(room)
            else:
                f = open('rooms/null.json')
                self.wfile.write(f.read())

        # calls after beginning the game in room by room admin
        if (action == "ROOM_START"):
            name = data["new_game"]["name"]
            deck = Deck()
            players = []
            for player in data["new_game"]["players"]:
                players.append(Player(player["name"], deck))
            game = self.game_server.new_game(name, players, deck)
            f = open('games/{}.json'.format(game.id))
            self.wfile.write(f.read())

        # calls after trying to fetch game
        if (action == "CONNECT"):
            game_name = data["connect"]["game"]
            player_name = data["connect"]["player"]
            for game in self.game_server.games:
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
            game = self.game_server.load_game(game_id)
            if (game == None):
                self._set_headers()
                self.send_response(404)
                self.end_headers()
                return
            player = None
            for p in game.players:
                if (p.name == player_name):
                    player = p
            if (self.game_server.do_evolution(game, player, creature, card)):
                self._set_headers()
                self.send_response(200)
                self.end_headers()
                return
            else:
                self._set_headers()
                self.send_response(403)
                self.end_headers()
                return
        return

    do_PUT = do_POST
    do_DELETE = do_GET

class Server:
    def __init__(self):

    def load_game(self, id):
        if (os.path.isfile("games/{}.json".format(id)):
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='HTTP Server')
    parser.add_argument('port', type=int, help='Listening port for HTTP Server')
    parser.add_argument('ip', help='HTTP Server IP')
    args = parser.parse_args()

    print 'Evolution Server Running...'
    server = Server()

    print('Listening on {}:{}}'.format(args.ip, args.port))
    HTTPserver = HTTPServer((args.ip, args.port), RequestHandler)
    HTTPserver.set_game_server(server)
    HTTPserver.serve_forever()
