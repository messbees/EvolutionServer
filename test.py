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
    game  = "game22"
    connect_to_room(game, "linegel")

if __name__ == "__main__":
    main()
