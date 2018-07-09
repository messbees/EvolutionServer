import requests

def main():
    json = {}
    json["action"] = "ROOM_NEW"
    json["room_new"]["game"] = "game"
    json["room_new"]["player"] = "messbees"
    r = requests.post('http://159.100.247.47:8888', json)
    print(r.status_code)
