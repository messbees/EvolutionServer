import requests

def new_room(name, admin):
    json = {}
    json["action"] = "ROOM_NEW"
    json["room_new"] = {}
    json["room_new"]["game"] = name
    json["room_new"]["player"] = admin
    print(json)
    print("Sending your {} request...".format(json["action"]))
    print(requests.post('http://159.100.247.47:8888', json=json))

def connect_to_room(name, player):
    json = {}
    json["action"] = "ROOM_CONNECT"
    json["room_connect"] = {}
    json["room_connect"]["game"] = name
    json["room_connect"]["player"] = player
    print(json)
    print("Sending your {} request...".format(json["action"]))
    print(requests.post('http://159.100.247.47:8888', json=json))

def main():
    connect_to_room("game22", "linegel")

if __name__ == "__main__":
    main()
