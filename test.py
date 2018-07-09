import requests

def main():
    json = {}
    json["action"] = "ROOM_NEW"
    json["room_new"]["game"] = "game"
    json["room_new"]["player"] = "messbees"
    print("Sending your {} request...".format(json[action]))
    print(requests.post('159.100.247.47:8888', json=json))

if __name__ == "__main__":
    main()
