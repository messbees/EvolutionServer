import requests

def main():
    json = {}
    json["action"] = "ROOM_NEW"
    json["room_new"]["game"] = "game"
    json["room_new"]["player"] = "messbees"
    r = requests.post('localhost:8888', json=json)
    print(r.status_code)
